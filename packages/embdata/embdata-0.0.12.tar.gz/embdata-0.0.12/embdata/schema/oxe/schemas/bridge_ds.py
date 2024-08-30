from typing import List

from pydantic import BaseModel, Field

from embdata.episode import ImageTask, VisionMotorStep
from embdata.geometry import CoordinateField
from embdata.image import Image
from embdata.motion import AbsoluteMotionField
from embdata.motion.control import AbsoluteHandControl, Pose, RelativePoseHandControl
from embdata.ndarray import NumpyArray
from embdata.sample import Sample


class Action(BaseModel):
    open_gripper: bool
    rotation_delta: List[float] = Field(..., max_items=3, min_items=3)
    terminate_episode: float
    world_vector: List[float] = Field(..., max_items=3, min_items=3)


class Observation(ImageTask):
    pass


class State(Sample):
    end_effector_pose: Pose = AbsoluteMotionField(
        default_factory=Pose, description="Absolute End Effector pose of the robot.",
    )
    is_first: int
    is_last: int
    is_terminal: int
    language_embedding: NumpyArray


class Step(VisionMotorStep):
    episode_idx: int
    step_idx: int
    image: Image
    action: RelativePoseHandControl
    absolute_action: AbsoluteHandControl
    state: State
    supervision: float
    timestamp: float = CoordinateField(default=0.0, description="Timestamp of the step in seconds.", unit="s")
