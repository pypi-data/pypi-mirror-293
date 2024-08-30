# Copyright (c) 2024 Mbodi AI
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


import logging
import os
from typing import Any, Dict, Generator

import numpy as np
from datasets import Dataset, DatasetInfo, Features
from datasets import Image as HFImage

from embdata.describe import describe
from embdata.ds.oxe.load import get_hf_dataset
from embdata.ds.oxe.oxe import Metadata
from embdata.ds.oxe.schemas.bridge_ds import (
    Observation,
    State,
    Step,
)
from embdata.episode import VisionMotorEpisode
from embdata.geometry import Pose
from embdata.image import Image
from embdata.motion.control import AbsoluteHandControl, RelativePoseHandControl
from embdata.sample import Sample


def get_absolute_action(step, action_is_relative=False):
    if action_is_relative:
        state = np.array(step["observation"]["state"][:-1] + [0])  # Gripper is not relative.
        action = np.array(
            step["action"]["world_vector"] + step["action"]["rotation_delta"] + [int(step["action"]["open_gripper"])],
        )
        return AbsoluteHandControl(state + action)
    return AbsoluteHandControl(
        step["action"]["world_vector"] + step["action"]["rotation_delta"] + [int(step["action"]["open_gripper"])],
    )


global metadata
metadata = None
info = None
feat = None


def to_vision_motor_episodes(item: Dict) -> Dict:
    episodes = [
        VisionMotorEpisode(
            steps=[
                Step(
                    image=Image(step["observation"]["image"]["bytes"]),
                    task=step["observation"]["natural_language_instruction"],
                    action=RelativePoseHandControl(
                        step["action"]["world_vector"]
                        + step["action"]["rotation_delta"]
                        + [int(step["action"]["open_gripper"])],
                    ),
                    episode_idx=episode_idx,
                    step_idx=step_idx,
                    timestamp=step_idx / float(metadata.control_frequency),
                    observation=Observation(
                        image=Image(step["observation"]["image"]["bytes"]),
                        task=step["observation"]["natural_language_instruction"],
                    ),
                    absolute_action=get_absolute_action(step, action_is_relative=True),
                    supervision=step["reward"],
                    state=State(
                        end_effector_pose=Pose(step["observation"]["state"]),
                        is_first=step["is_first"],
                        is_last=step["is_last"],
                        is_terminal=step["is_terminal"],
                        language_embedding=np.array(step["observation"]["natural_language_embedding"]),
                    ),
                    metadata=metadata,
                )
                for step_idx, step in enumerate(episode["steps"])
            ],
        )
        for episode_idx, episode in enumerate(item["episode"])
    ]
    return Sample.unpack_from([step for episode in episodes for step in episode.steps]).dump(as_field="pil")


# logging.basicConfig(level=logging.DEBUG, force=True)

ds = list(get_hf_dataset(dataset_name="bridge", streaming=True).take(2))

describe(ds, compact=True, show=True)
metadata = Metadata(ds[0]["metadata"])
step = ds[0]["episode"]["steps"][0]
feat = Step(
    image=Image(step["observation"]["image"]["bytes"]),
    task=step["observation"]["natural_language_instruction"],
    episode_idx=0,
    step_idx=0,
    observation=Observation(
        image=Image(step["observation"]["image"]["bytes"]),
        task=step["observation"]["natural_language_instruction"],
    ),
    absolute_action=get_absolute_action(step, action_is_relative=True),
    action=RelativePoseHandControl(
        step["action"]["world_vector"] + step["action"]["rotation_delta"] + [int(step["action"]["open_gripper"])],
    ),
    supervision=step["reward"],
    state=State(
        end_effector_pose=Pose(step["observation"]["state"]),
        is_first=step["is_first"],
        is_last=step["is_last"],
        is_terminal=step["is_terminal"],
        language_embedding=np.array(step["observation"]["natural_language_embedding"]),
    ),
    timestamp=float(metadata.control_frequency) * 0,
).infer_features_dict()
feat = {
    "image": HFImage(),
    **{k: v for k, v in feat.items() if k != "image"},
    "metadata": metadata.infer_features_dict(),
}
feat = Features(feat)
ds = list(get_hf_dataset(dataset_name="bridge", streaming=True).skip(10).take(10))
ds: Dataset = (
    Dataset.from_list(ds)
    .map(
        to_vision_motor_episodes,
        num_proc=4,
        batched=True,
        batch_size=500,
        features=feat,
        remove_columns=["episode", "__key__"],
    )
    .to_list()
)
ds = Dataset.from_list(
    ds,
    info=DatasetInfo(
        citation='Padalkar, Abhishek, et al. "Open x-embodiment: Robotic learning datasets and rt-x models." arXiv preprint arXiv:2310.08864 (2023).',
        supervised_keys={
            "input": "observation",
            "output": "action",
        },
        features=feat,
        license="MIT",
        description="Open-X-Embodiment: Bridge V2",
        homepage="https://robotics-transformer-x.github.io/",
    ),
    features=feat,
)
ds.push_to_hub(
    "mbodiai/oxe_bridge_v2",
    config_name="default",
    private=False,
    split=f"shard_{0}",
    token=os.getenv("HF_WRITE"),
)

describe(feat, compact=True, show=True)
for i in range(30):
    ds = list(get_hf_dataset(dataset_name="bridge", streaming=True).skip(i * 1000).take(1000))
    ds: Dataset = Dataset.from_list(ds).map(
        to_vision_motor_episodes,
        num_proc=4,
        batched=True,
        batch_size=1000,
        features=feat,
        remove_columns=["episode", "__key__"],
    )
    # ds = Dataset.from_list(
    #             ds,
    #             info=DatasetInfo(
    #             citation='Padalkar, Abhishek, et al. "Open x-embodiment: Robotic learning datasets and rt-x models." arXiv preprint arXiv:2310.08864 (2023).',
    #             supervised_keys={
    #                 'input': "observation",
    #                 'output': "action",
    #             },
    #             features=feat,
    #             license="MIT",
    #             description="Open-X-Embodiment: Bridge V2",
    #             homepage="https://robotics-transformer-x.github.io/",
    #             ),
    #             features=feat,
    # )
    ds.push_to_hub(
        "mbodiai/oxe_bridge_v2",
        config_name="default",
        private=False,
        split=f"shard_{i}",
        token=os.getenv("HF_WRITE"),
    )
    ds.save_to_disk(f"bridge_v2/shard_{i}")


def loop() -> Generator[Dict, Any, None]:
    for i in range(6):
        ds = Dataset.load_from_disk(f"bridge/shard_{i}")
        global metadata
        metadata = Metadata(**ds[0]["metadata"])
        global feat
        ds: Dataset = ds.map(to_vision_motor_episodes, batched=True, batch_size=None).to_list()
        feat = Features(feat)
        ds = Dataset.from_list(
            ds,
            info=DatasetInfo(
                citation='Padalkar, Abhishek, et al. "Open x-embodiment: Robotic learning datasets and rt-x models." arXiv preprint arXiv:2310.08864 (2023).',
                supervised_keys={
                    "input": "observation",
                    "output": "action",
                },
                features=feat,
                license="MIT",
                description="Open-X-Embodiment: Bridge V2",
                homepage="https://robotics-transformer-x.github.io/",
            ),
            features=feat,
        )
        ds.push_to_hub(
            "mbodiai/oxe_bridge_v2",
            config_name="default",
            private=False,
            split=f"shard_{i}",
            token=os.getenv("HF_WRITE"),
        )
        ds.save_to_disk(f"bridge_v2/shard_{i}")


loop()
# for i in range(7):
#   hf = get_hf_dataset(dataset_name="bridge",streaming=True).skip(i*5000).take(5000)
#   ds = Dataset.from_list(list(hf),features=hf.features)
#   ds.save_to_disk(f"bridge/shard_{i}")

#   ds.push_to_hub("mbodiai/oxe_bridge", token=os.getenv("HF_WRITE"))

# for i in range(20):
#   ds = Dataset.load_from_disk(f"bridge/shard_{i}")
#   print("Saved", i)

# print([a["action"]["open_gripper"] for a in ds[0]["episode"]["steps"]])


# import pandas as pd

# feat = ds.episodes[0].infer_features_dict()
# feat["episode_idx"] = Value("int32")
# feat["step_idx"] = Value("int32")
# feat = Features(feat)
# print(feat)
# print(ds.episodes[0].steps)
# print(ds.dump()["episodes"][0]["steps"])
# eps = ds.dump(exclude_none=False)["episodes"]

# print(ds.episodes[0].steps[10].dump().keys())
# print(type(ds.episodes[0].steps[0].observation.image.dump()))
# print(ds.dump(as_field="pil")["episodes"][0]["steps"][0]["observation"]["image"])
# print(ds.episodes[0].steps[0].model_info())
# print(ds.episodes[0].steps[0].dump()["action"])
# print(ds.episodes[0].steps[0].dump()["relative_action"])
