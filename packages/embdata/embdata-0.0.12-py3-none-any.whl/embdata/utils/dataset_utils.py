from itertools import zip_longest
from typing import Any, Dict, List

from datasets import Dataset, DatasetDict

from embdata.sample import Sample
from embdata.time import TimeStep


def list_to_steps(
    steps: List[Dict[str, Any]],
    observation_key: str | None = None,
    action_key: str | None = None,
    state_key: str | None = None,
    supervision_key: str | None = None,
    freq_hz: float | None = None,
    image_keys: List[str] | None = None,
    time_step_cls: type[TimeStep] = TimeStep,
    **step_kwargs,
) -> List[TimeStep]:
    """Convert a list of dictionaries to a list of TimeSteps."""
    Step: type[TimeStep] = time_step_cls  # noqa
    observation_key = observation_key or "observation"
    action_key = action_key or "action"
    state_key = state_key or "state"
    supervision_key = supervision_key or "supervision"
    freq_hz = 1
    return [
        Step(
            observation=step.get(observation_key),
            action=step.get(action_key),
            state=step.get(state_key),
            supervision=step.get(supervision_key),
            timestamp=i / freq_hz,
            image_keys=image_keys,
            **step_kwargs,
        )
        for i, step in enumerate(steps)
    ]


def lists_to_steps(  # noqa
    observations: list[Sample | Dict | TimeStep] | None = None,
    actions: list[Sample | Dict | TimeStep] | None = None,
    states: list[Sample | Dict | TimeStep] | None = None,
    supervisions: list[Sample | Dict | TimeStep] | None = None,
    freq_hz: float | None = None,
    image_keys: str | list[str] = "image",
    time_step_cls: type[TimeStep] = TimeStep,
    **step_kwargs,
) -> List[TimeStep]:
    """Convert observations, actions, states, and supervisions to a list of TimeSteps."""
    Step: type[TimeStep] = time_step_cls  # noqa
    freq_hz = freq_hz or 1.0
    step_kwargs.update({"freq_hz": freq_hz})
    observations = observations or []
    actions = actions or []
    states = states or []
    supervisions = supervisions or []
    length = max(len(observations), len(actions), len(states), len(supervisions))
    return [
        Step(o, a, s, sup, i / freq_hz, image_keys=image_keys, **step_kwargs)
        for i, o, a, s, sup in zip_longest(
            range(length),
            observations,
            actions,
            states,
            supervisions,
            fillvalue=Sample(),
        )
    ]


def dataset_to_steps(  # noqa
    dataset: Dataset,
    split: str | None = None,
    observation_key: str = "observation",
    action_key: str = "action",
    state_key: str | None = None,
    supervision_key: str | None = None,
    freq_hz: str | float | None = None,
    image_keys: str | list[str] = "image",
    time_step_cls: type[TimeStep] = TimeStep,
    **step_kwargs,
) -> List[TimeStep]:
    """Create an episode from a dataset."""
    list_keys = [key for key in (observation_key, action_key, state_key, supervision_key) if key is not None]
    if isinstance(dataset, DatasetDict):
        split = split or "train"
        dataset = dataset.get(split, dataset)
        if isinstance(dataset, DatasetDict):
            freq_hz = freq_hz if isinstance(freq_hz, float | int) else dataset.get(freq_hz, 1)
            list_keys.extend(
                [key for key in dataset.column_names if key not in list_keys and isinstance(dataset[key], list)],
            )
    ds = Sample(dataset).flatten("dicts", include=list_keys)

    return list_to_steps(
        ds,
        observation_key=observation_key,
        action_key=action_key,
        image_keys=image_keys,
        freq_hz=freq_hz,
        state_key=state_key,
        supervision_key=supervision_key,
        time_step_cls=time_step_cls,
        **step_kwargs,
    )
