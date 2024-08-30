from functools import partial
from typing import Any, Dict, Iterable, List, Tuple

import numpy as np
from pydantic import PrivateAttr

from embdata.motion import Motion
from embdata.motion.control import (
    AnyMotionControl,
    HandControl,
    MobileSingleHandControl,
    MotionField,
    RelativePoseHandControl,
)
from embdata.sample import Sample
from embdata.sense.image import Image
from embdata.utils.iter_utils import map_nested_with_keys

_image_keys_actual = set()

supports_image_key = lambda k: any(c in k for c in ["image", "img", "rgb", "rgbd", "depth", "pixel", "byte", "array", "view", "camera"])
supports_depth_key = lambda k: any(c in k for c in ["depth", "depthmap", "depthview", "deptharray", "rgbd"])
def is_image(k, v, image_keys) -> bool:
    if not k:
        return False, None
    k = [k for k in list(k) if k]

    is_image_key =  k is not None and v is not None and image_keys and hasattr(k, "__len__") and len(k) >= 1 and\
         (k[-1] in image_keys or supports_image_key(k[-1]))
    return is_image_key and Image.supports(v), k[-1] if is_image_key else None

def map_image_candidates(k, v, image_keys=None) -> Any:
    global _image_keys_actual
    if image_keys is None:
        image_keys = ["image"]
    is_image_bool, actual_key = is_image(k, v, image_keys)
    # print(f"Image key: {actual_key}")
    if not actual_key:
        return v
    if actual_key and supports_depth_key(actual_key):
        mode = "I"
        encoding = "PNG"
    else:
        mode = "RGB"
        encoding = "JPEG"
    out =  Image(v, mode=mode, encoding=encoding) if is_image_bool else v
    if isinstance(out, Image):
        if actual_key:
            _image_keys_actual.add(actual_key)
        else:
            msg = f"Image key not found in {k}"
            raise ValueError(msg)
    return out

def convert_images(d, image_keys=None) -> Dict:
    if image_keys is None:
        image_keys = ["image"]
    def leaf_predicate(k, v):
        return is_image(k, v, image_keys)[0]
    fn = partial(map_image_candidates, image_keys=image_keys)
    return map_nested_with_keys(fn, d, leaf_predicate=leaf_predicate)



class TimeStep(Sample):
    """Time step for a task."""

    observation: Sample | None = None
    action: Sample | None = None
    state: Sample | None = None
    supervision: Any = None
    timestamp: float | None = None
    episode_idx: int | None = 0
    step_idx: int | None = 0
    image_keys: str | set[str] | None = "image"
    _observation_class: type[Sample] = PrivateAttr(default=Sample)
    _action_class: type[Sample] = PrivateAttr(default=Sample)
    _state_class: type[Sample] = PrivateAttr(default=Sample)
    _supervision_class: type[Sample] = PrivateAttr(default=Sample)
    _episode: Any = PrivateAttr(default=None)
    @property
    def observation_class(self) -> type[Sample]:
        return self._observation_class

    @property
    def action_class(self) -> type[Sample]:
        return self._action_class

    @property
    def state_class(self) -> type[Sample]:
        return self._state_class

    @property
    def supervision_class(self) -> type[Sample]:
        return self._supervision_class

    @classmethod
    def from_dict(  # noqa: PLR0913
        cls,
        values: Dict[str, Any],
        image_keys: str | set | None = "image",
        observation_key: str | None = "observation",
        action_key: str | None = "action",
        supervision_key: str | None = "supervision",
        state_key: str | None = "state",
    ) -> "TimeStep":
        obs = values.pop(observation_key, None)
        act = values.pop(action_key, None)
        sta = values.pop(state_key, None)
        sup = values.pop(supervision_key, None)
        timestamp = values.pop("timestamp", 0)
        step_idx = values.pop("step_idx", 0)
        episode_idx = values.pop("episode_idx", 0)

        Obs = cls._observation_class.get_default()  # noqa: N806
        Act = cls._action_class.get_default()  # noqa: N806
        Sta = cls._state_class.get_default()  # noqa: N806
        Sup = cls._supervision_class.get_default()  # noqa: N806
        obs = Obs(**convert_images(obs, image_keys)) if obs is not None else None
        act = Act(**convert_images(act, image_keys)) if act is not None else None
        sta = Sta(**convert_images(sta, image_keys)) if sta is not None else None
        sup = Sup(**convert_images(sup, image_keys)) if sup is not None else None
        field_names = cls.model_fields.keys()
        global _image_keys_actual
        image_keys = _image_keys_actual.copy()
        _image_keys_actual.clear()
        return cls(
            observation=obs,
            action=act,
            state=sta,
            supervision=sup,
            episode_idx=episode_idx,
            step_idx=step_idx,
            timestamp=timestamp,
            **{k: v for k, v in values.items() if k not in field_names},
        )

    @classmethod
    def from_iterable(cls, step: tuple, image_keys="image", **kwargs) -> "TimeStep":
        return cls(*step, image_keys=image_keys, **kwargs)

    def __init__(  # noqa: PLR0913
        self,
        observation: Sample | Dict | np.ndarray | None = None,
        action: Sample | Dict | np.ndarray | None = None,
        state: Sample | Dict | np.ndarray | None = None,
        supervision: Any | None = None,
        episode_idx: int | None = 0,
        step_idx: int | None = 0,
        timestamp: float | None = None,
        image_keys: str | set[str] | None = "image",
        **kwargs,
    ) -> None:
        obs = observation
        act = action
        sta = state
        sup = supervision

        Obs = TimeStep._observation_class.get_default() if not isinstance(obs, Sample) else lambda x: x  # noqa: N806
        Act = TimeStep._action_class.get_default() if not isinstance(act, Sample) else lambda x: x  # noqa: N806
        Sta = TimeStep._state_class.get_default() if not isinstance(sta, Sample) else lambda x: x  # noqa: N806
        Sup = TimeStep._supervision_class.get_default() if not isinstance(sup, Sample) else lambda x: x  # noqa: N806
        obs: Sample = Obs(convert_images(obs, image_keys)) if obs is not None else None
        act = Act(convert_images(act, image_keys)) if act is not None else None
        sta = Sta(convert_images(sta, image_keys)) if sta is not None else None
        sup = Sup(convert_images(supervision)) if supervision is not None else None

        if kwargs.get("_action_class"):
            act = kwargs["_action_class"](act)
        if kwargs.get("_observation_class"):
            obs = kwargs["_observation_class"](obs)
        if kwargs.get("_state_class"):
            sta = kwargs["_state_class"](sta)
        if kwargs.get("_supervision_class"):
            sup = kwargs["_supervision_class"](sup)
        if "natural_language_instruction" in obs.keys():  # noqa: SIM118
            obs["instruction"] = obs.pop("natural_language_instruction")
        super().__init__(
            observation=obs,
            action=act,
            state=sta,
            supervision=sup,
            episode_idx=episode_idx,
            step_idx=step_idx,
            timestamp=timestamp,
            **kwargs,
        )

    def window(
        self,
        steps: List["TimeStep"] | None = None,
        nforward: int = 1,
        nbackward: int = 1,
        pad_value: Any = None,
    ) -> Iterable["TimeStep"]:
        """Create a sliding window over the episode.

        Args:
            steps (List[TimeStep]): The steps in the episode.
            nforward (int): The number of steps to look forward.
            nbackward (int, optional): The number of steps to look backward. Defaults to 0.
            current_n (int, optional): The current step index. Defaults to 0.
            pad_value (Any, optional): The value to pad the window with. Defaults to None.

        Yields:
            Iterable: An iterable of steps in the window.
        """
        for i in range(self.step_idx - nbackward, self.step_idx + nforward):
            if i < 0 or i >= len(self):
                yield pad_value
            else:
                yield steps[i]

    def match_action(self, action: Dict) -> type[Sample]:
        """Match the action to the control.

        Args:
            action (Any): The action to match.

        Returns:
            type[Sample]: The type of the action.
        """
        for k, v in action.items():
            if "rel" in k:
                return RelativePoseHandControl
            if hasattr(v, "shape") and len(v.shape) == 7:
                return HandControl
            if "action" in k:
                return AnyMotionControl
        return None


class ImageTask(Sample):
    """Canonical Observation."""

    image: Image
    task: str


class VisionMotorStep(TimeStep):
    """Time step for vision-motor tasks."""

    _observation_class: type[ImageTask] = PrivateAttr(default=ImageTask)
    observation: ImageTask | None = None
    action: Motion | None = None
    supervision: Any | None = None

