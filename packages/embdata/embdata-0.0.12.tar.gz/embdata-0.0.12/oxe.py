import inspect
import logging
import os
import sys
import traceback
from functools import partial
from logging import FileHandler
from pathlib import Path
from typing import Callable

import pandas as pd
import rich
from datasets import Dataset, IterableDataset, get_dataset_config_names, load_dataset
from huggingface_hub import HfApi
from lager import log
from rich.console import Console
from rich.logging import RichHandler
from rich.pretty import pprint, pretty_repr
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn
from rich.prompt import Confirm, Prompt

from embdata import describe
from embdata.episode import Episode
from embdata.motion import control
from embdata.schema.metadata import Metadata

console = Console()
log.add(sink="outs.oxe.log", level=logging.DEBUG)
log.add(RichHandler(console=console), level=logging.INFO)

def get_oxe_metadata(dataset_name: str = "utokyo_xarm_pick_and_place_converted_externally_to_rlds") -> Metadata:
    path = "/home/user/seb/embodied-data/oxe_metadata.csv"
    oxe_dataset_metadata = pd.read_csv(path)

    if dataset_name not in oxe_dataset_metadata["Registered Dataset Name"].values:  # noqa: PD011
        raise ValueError(f"Dataset {dataset_name} not found in OXE Overview metadata.")  # noqa

    return Metadata(oxe_dataset_metadata[oxe_dataset_metadata["Registered Dataset Name"] == dataset_name].to_dict(
        orient="records",
    )[0])



repo = "jxu124/OpenX-Embodiment"
config_names = get_dataset_config_names(repo)

def numeric(x):
    if isinstance(x, str):
        x = x.replace(",", "")
        if x.isnumeric():
            return int(x)
    return x
for m in sorted(config_names, key=lambda x: numeric(get_oxe_metadata(x)["num_episodes"]), reverse=True)[:10]:
    rich.print(get_oxe_metadata(m))


def next_chunk(ds: IterableDataset, i, chunk_len=500):
    return  ds.skip(i*chunk_len).take(chunk_len)

def prelude_ds(ds: Dataset, n):
    name = ds.config_name
    api = HfApi(token=os.getenv("HF_MBODI"))
    rich.print(f"Processing {name}")
    try:
            if api.repo_exists("mbodiai/OpenX-Embodiment",repo_type="dataset"):
                info = api.dataset_info("mbodiai/OpenX-Embodiment")
                rich.print(info)
                if Confirm.ask("Delete existing repo?"):
                    api.delete_repo("mbodiai/OpenX-Embodiment", repo_type="dataset")
            members = inspect.getmembers(control, inspect.isclass)
            classes = {}
            for k, v in members:
                classes[k] = v
                rich.print(k)
                if not hasattr(v, "model_fields"):
                    continue
                rich.print("Model fields:")
                for field in v.model_fields:
                    rich.print(field)
                    rich.print(v)
                describe(v())
            describe(ds)
            e = Episode(ds, metadata=get_oxe_metadata(name))
            e.describe()
            t = e.trajectory()
            rich.print(t.stats())
            t.plot().show()
            action_class = Prompt.ask("Action classes?", choices=classes.keys(), default="HandControl")
            action_key = Prompt.ask("Action key?", default="action")
            e = Episode(ds, metadata=get_oxe_metadata(name), action_class=classes[action_class], action_key=action_key)
            rich.print("Uploading ")
            e.dataset().push_to_hub(
                "mbodiai/OpenX-Embodiment", name, 
                split="e0-" + str(n),
                private=True,
                token=os.getenv("HF_WRITE"),
            )
            Path("plots").mkdir(exist_ok=True)
            e.trajectory().plot().save(f"plots/{name}-{n}.png").show()
            return partial(Episode,  metadata=get_oxe_metadata(name)), name, n
    except Exception as e:
        print(traceback.format_exc())

        if isinstance(e, KeyboardInterrupt):
            log.error(e)
            raise e
        return partial(Episode, metadata=get_oxe_metadata(name)), name, n

def loop_chunk(apply_episode_kwargs: Callable[[], Episode], name, i):
    try:
        e: Episode = apply_episode_kwargs()
        rich.print("Uploading ")
        e.dataset().push_to_hub(
            "mbodiai/OpenX-Embodiment", name, 
            split="e" + str(i) + "-" + str(i+1),
            private=True,
            token=os.getenv("HF_WRITE"),
        )
        Path("plots").mkdir(exist_ok=True)
        e.trajectory().plot().save(f"plots/{name}-{i}.png").show()
        return len(e.group_by("episode_idx"))
    except Exception as e:
        print(traceback.format_exc())
        if isinstance(e, KeyboardInterrupt):
            log.error(e)
            raise e
        return 0

def load_plot_upload(repo, name, split=None, chunk_len=500):
    m = get_oxe_metadata(name)
    print(m["num_episodes"])
    num_episodes = numeric(m["num_episodes"])

    rich.print(m)
    n = 0
    j = 2 
    apply_episode_kargs, name, i = prelude_ds(load_dataset(repo, name, streaming=False, split=f"{split}[{j*chunk_len}:{min((j+1)*chunk_len, num_episodes)}]"), j)

    with Progress(
        SpinnerColumn(),
        *Progress.get_default_columns(),
        TimeElapsedColumn(),
        console=console,
        transient=False,
    ) as progress:
        task = progress.add_task("[green]Processing", total=num_episodes)
        
        while n < num_episodes:
            ds: Dataset = load_dataset(repo, name, streaming=False, split=f"{split}[{i*chunk_len}:{min((i+1)*chunk_len, num_episodes)}]")
            loop_chunk(partial(apply_episode_kargs, steps=ds), name, i)
            processed_episodes = min(chunk_len, num_episodes - n)
            n += processed_episodes
            i += 1
            progress.update(task, completed=n, advance=n/float(num_episodes)) 
    


def loop_config_names(repo, config_names, split=None, bar=None):
    for name in config_names:
        if name in ["taco_play", "bridge"]:
            pass
        m = get_oxe_metadata(name)
        pprint(f"Loading {name}")   
        pprint(m)
        load_plot_upload(repo, name, 0, split, bar=bar)

def main():
    from dotenv import load_dotenv
    load_dotenv(".env")
    MAX_SAMPLES = 500
    load_plot_upload(repo, "bridge", split="train")
    load_plot_upload(repo, "kuka", split="train")
    loop_config_names(repo, split="train")

if __name__ == "__main__":
    main()