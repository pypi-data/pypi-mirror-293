# Copyright (c) 2024 Mbodi AI
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


import logging
from pathlib import Path

import pandas as pd
from datasets import Dataset, load_dataset
from importlib_resources import files


def get_oxe_metadata(dataset_name: str = "utokyo_xarm_pick_and_place_converted_externally_to_rlds") -> dict:
    path = files("embdata") / Path("ds/oxe/oxe_metadata.csv")
    oxe_dataset_metadata = pd.read_csv(path)

    if dataset_name not in oxe_dataset_metadata["Registered Dataset Name"].values:  # noqa: PD011
        msg = f"Dataset {dataset_name} not found in OXE Overview metadata."
        raise ValueError(msg)

    return oxe_dataset_metadata[oxe_dataset_metadata["Registered Dataset Name"] == dataset_name].to_dict(
        orient="records",
    )[0]


def get_hf_dataset(
    dataset_path: str = "jxu124/OpenX-Embodiment",
    dataset_name: str = "utokyo_xarm_pick_and_place_converted_externally_to_rlds",
    split: str = "train",
    streaming: bool = True,
    download_mode: str | None = None,
) -> Dataset:
    logging.info(f"Fetching dataset {dataset_path}/{dataset_name}")
    ds = load_dataset(dataset_path, dataset_name, streaming=streaming, split=split, download_mode=download_mode)
    return ds.map(
        lambda example: {
            "metadata": get_oxe_metadata(dataset_name),
            "episode": example["data.pickle"],
        },
        remove_columns=["__url__", "data.pickle"],
    )
