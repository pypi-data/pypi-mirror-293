import io
import os
import torch
from typing import List
from PIL import Image as PILModule
from embdata.coordinate import Pose
import numpy as np
from pydantic import Field
import pytest
from embdata.episode import Episode, TimeStep, VisionMotorStep, ImageTask, VisionMotorEpisode, VisionMotorHandEpisode
from embdata.sample import Sample
from datasets import load_dataset
from embdata.sense.image import Image
from embdata.motion.control import AnyMotionControl, RelativePoseHandControl, HandControl
from embdata.trajectory import Trajectory
from rich.pretty import pprint
from datasets import Dataset


@pytest.fixture
def time_step():
    return TimeStep(observation=Sample("observation"), action=Sample(1), supervision=Sample("supervision"))


@pytest.fixture
def dataset():
    return Dataset.from_list(
        [
            {
                "observation": ImageTask(
                    image=Image(np.zeros((224, 224, 3), dtype=np.uint8)), task=f"Do something {10-i}"
                ).dump(as_field="pil"),
                "action": HandControl(pose=Pose(x=i, y=2, z=3, roll=i, pitch=0, yaw=np.pi / 2), grasp=0.0).dict(),
                "episode_idx": 0,
                "step_idx": i,
                "image_keys": "image",
                "timestamp": i,
            }
            for i in range(5)
        ]
    )


def test_episode_initialization(time_step):
    episode = Episode(steps=[time_step])
    assert len(episode) == 1
    assert episode[0] == time_step


def test_episode_length(time_step):
    episode = Episode(steps=[time_step, time_step, time_step])
    assert len(episode) == 3


def test_episode_get_item(time_step):
    episode = Episode(steps=[time_step])
    assert episode[0] == time_step


def test_episode_set_item(time_step):
    time_step2 = TimeStep(observation=Sample("observation"), action=Sample("action"), supervision=Sample("supervision"))
    episode = Episode(steps=[time_step])
    episode[0] = time_step2
    assert episode[0] == time_step2


def test_episode_iteration(time_step):
    episode = Episode(steps=[time_step, time_step])
    for i, step in enumerate(episode.iter()):
        assert step == episode[i]


def test_episode_addition(time_step):
    episode1 = Episode(steps=[time_step])
    episode2 = Episode(steps=[time_step, time_step])
    combined_episode = episode1 + episode2
    assert len(combined_episode) == 3


def test_episode_append(time_step):
    episode = Episode(steps=[])
    episode.append(time_step)
    assert len(episode) == 1
    assert episode[0] == time_step


def test_episode_split(time_step):
    episode = Episode(steps=[time_step, time_step, time_step])
    episodes = episode.split(lambda step: False)
    assert len(episodes) == 2
    assert len(episodes[0]) == 0
    assert len(episodes[1]) == 3


def test_unpacked_episode(time_step):
    steps = [time_step, time_step, time_step]
    episode = Sample.unpack_from(steps)
    observations, actions, supervisions = episode.observation, episode.action, episode.supervision
    assert len(observations) == 3
    assert len(actions) == 3
    assert len(supervisions) == 3
    assert all(isinstance(observation, Sample) for observation in observations)
    assert all(isinstance(action, Sample) for action in actions)
    # assert all(isinstance(supervision, Sample) for supervision in supervisions)


def test_episode_concatenate(time_step):
    episode1 = Episode(steps=[time_step, time_step])
    episode2 = Episode(steps=[time_step, time_step])
    episode3 = Episode(steps=[time_step, time_step])
    concatenated_episode = Episode.concat([episode1, episode2, episode3])
    assert len(concatenated_episode) == 6


def test_episode_from_lists(time_step):
    observations = [Sample("observation1"), Sample("observation2")]
    actions = [Sample("action1"), Sample("action2")]
    episode = Episode.from_lists(observations, actions)
    assert len(episode) == 2
    assert episode[0].observation == observations[0]
    assert episode[0].action == actions[0]
    assert episode[1].observation == observations[1]
    assert episode[1].action == actions[1]


def test_episode_from_list(time_step):
    steps = [
        {"observation": Sample("observation1"), "action": Sample("action1"), "supervision": Sample("supervision1")},
        {"observation": Sample("observation2"), "action": Sample("action2"), "supervision": Sample("supervision2")},
    ]
    episode = Episode.from_list(steps, "observation", "action", "supervision")
    assert len(episode) == 2
    assert episode[0].observation == steps[0]["observation"]
    assert episode[0].action == steps[0]["action"]
    # assert episode[0].supervision == steps[0]["supervision"]
    assert episode[1].observation == steps[1]["observation"]
    assert episode[1].action == steps[1]["action"]
    # assert episode[1].supervision == steps[1]["supervision"]


def test_episode_trajectory(time_step):
    episode = Episode(steps=[time_step, time_step, time_step])
    trajectory = episode.trajectory("action", freq_hz=1)
    assert len(trajectory) == 3


def test_episode_append(time_step):
    episode = Episode(steps=[])
    episode.append(time_step)
    assert len(episode) == 1
    assert episode[0] == time_step


def test_episode_split(time_step):
    episode = Episode(steps=[time_step, time_step, time_step])
    episodes = episode.split(lambda step: False)
    assert len(episodes) == 2
    assert len(episodes[0]) == 0
    assert len(episodes[1]) == 3


def test_episode_iteration(time_step):
    episode = Episode(steps=[time_step, time_step])
    for i, step in enumerate(episode.steps):
        assert step == episode[i]


def test_episode_addition(time_step):
    episode1 = Episode(steps=[time_step])
    episode2 = Episode(steps=[time_step, time_step])
    combined_episode = episode1 + episode2
    assert len(combined_episode) == 3


def test_episode_get_item(time_step):
    episode = Episode(steps=[time_step])
    assert episode[0] == time_step


def test_episode_set_item(time_step):
    time_step2 = TimeStep(observation=Sample("observation"), action=Sample("action"), supervision=Sample("supervision"))
    episode = Episode(steps=[time_step])
    episode[0] = time_step2
    assert episode[0] == time_step2


def test_episode_from_ds(time_step):
    ds = load_dataset("mbodiai/test_dataset", split="train").to_list()
    episode = Episode(steps=ds)
    assert len(episode.steps) == len(ds)


def test_episode_from_zipped_ds(time_step):
    obs = [Sample("observation1"), Sample("observation2")]
    act = [Sample("action1"), Sample("action2")]
    sup = [Sample("supervision1"), Sample("supervision2")]

    episode = Episode(zip(obs, act, sup))
    assert len(episode.steps) == len(obs)


def test_episode_flatten(time_step):
    episode = Episode(steps=[time_step, time_step, time_step])
    flattened = episode.flatten("lists", "action", non_numerical="ignore")
    assert len(flattened) == 3
    assert all(isinstance(step, List) for step in flattened)
    pprint(f"flattened: {flattened}")

    assert np.allclose(flattened, [[1], [1], [1]])

    flattened = episode.flatten("lists", "observation")
    assert len(flattened) == 3
    for step in flattened:
        assert isinstance(step, List)
        assert step[0] == "observation"


def test_trajectory(time_step):
    episode = Episode(steps=[time_step, time_step, time_step])
    trajectory = episode.trajectory("action", freq_hz=1)
    assert len(trajectory) == 3
    # print(trajectory.array)
    # print(episode.steps)
    steps = episode.flatten("lists", "action")
    from rich.pretty import pprint

    pprint(f"steps: {steps}")
    assert np.allclose(trajectory.array, episode.flatten("lists", "action"))


@pytest.mark.network
def test_episode_again():
    from datasets import load_dataset

    ds = load_dataset("mbodiai/test_dataset", split="train").to_list()
    ds = ds[:10]
    episode = Episode(steps=ds)
    episode.describe()
    traj = episode.trajectory().plot()
    traj = episode.trajectory("action", freq_hz=1).resample(10)
    assert len(traj) == (10 * len(episode)) - 9


def test_episode_from_ds(dataset):
    episode = Episode(steps=dataset)
    assert len(episode.steps) == len(dataset)
    for step, expected in zip(episode.steps, dataset):
        assert step.observation.task == expected["observation"]["task"]
        assert step.action.dict() == expected["action"]
        assert step.action.dict().keys() == expected["action"].keys()
        assert step.observation.dict().keys() == expected["observation"].keys()


def test_episode_from_list_of_episodes(dataset):
    episode = Episode(steps=dataset.to_list())

    episode2 = Episode(steps=dataset[:2])
    episode3 = Episode(steps=dataset[:2])
    episode4 = Episode(steps=dataset.to_list())
    episodes = Sample(something=[episode, episode2, episode3, episode4])
    # from embdata.describe import describe

    # describe(episodes.flatten("dicts", include=["observation", "action"]))
    ds = Dataset.from_dict(episodes.dict())
    episode = Episode(ds)
    # describe(episode, check_full=True)
    assert len(episode.steps) == len([step for ep in episodes.something for step in ep.steps])


def test_episode_resample():
    steps = []
    for i in range(5):
        steps.append(
            VisionMotorStep(
                observation=ImageTask(image=Image(size=(224, 224)), task="Do something"),
                action=HandControl(pose=Pose(x=1, y=2, z=3, roll=0, pitch=0, yaw=np.pi / 2), grasp=0.0),
            )
        )

    episode = VisionMotorEpisode(steps=steps)

    traj = episode.trajectory("action").resample(20)
    assert len(traj) == 81

    from embdata.sense.video import Video
    Video([step.observation.image for step in episode.steps]).save("out.mp4")


if __name__ == "__main__":
    pytest.main(["-vv", __file__])
