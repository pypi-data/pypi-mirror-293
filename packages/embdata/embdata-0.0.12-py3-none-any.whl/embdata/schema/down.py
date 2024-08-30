import os
from embdata.describe import describe_keys, describe
from datasets import load_dataset, Dataset, get_dataset_infos, get_dataset_config_names
from huggingface_hub import HfApi, list_datasets
import logging
from embdata.episode import VisionMotorHandEpisode
from schema.oxe.oxe import get_oxe_metadata

def get_hf_dataset(
    dataset_path: str = "jxu124/OpenX-Embodiment",
    # dataset_name: str = "utokyo_xarm_pick_and_place_converted_externally_to_rlds",
    streaming: bool = False,  # noqa
    download_mode: str | None = None,
) -> Dataset:
    logging.info(f"Fetching dataset {dataset_path}")
    for name in get_dataset_config_names(path=dataset_path):
    ds = load_dataset(dataset_path, streaming=streaming, download_mode=download_mode)
    ds = ds.map(
          lambda example: {
              "metadata": get_oxe_metadata(name),
              "episode": example["data.pickle"],
          },
          remove_columns=["__url__", "data.pickle"],
      )
    metadata = get_oxe_metadata(name)
    metadata["keys"] = set(describe_keys(metadata).values())
    describe(metadata)
    ds = VisionMotorHandEpisode.from_dataset(ds, metadata=metadata)

if __name__ == "__main__":
    os.environ["OPENAI_API_KEY"] = "mbodi-demo-1"
    os.environ["OPENAI_BASE_URL"] = "http://localhost:3389/v1"
    get_hf_dataset()
    from aider.main import main
