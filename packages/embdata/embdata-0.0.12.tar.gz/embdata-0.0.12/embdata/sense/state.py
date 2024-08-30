from typing import Any

import numpy as np
from pydantic import ConfigDict

from embdata.coordinate import CoordsField, PlanarPose, Pose
from embdata.motion import AbsoluteMotionField, Motion, MotionField, RelativeMotionField
from embdata.ndarray import NumpyArray
from embdata.sample import Sample


class State(Sample):
    """A class for storing the state of an environment."""
    is_first: bool = False
    is_terminal: bool = False
    """Whether the state is terminal for any reason; error, or otherwise."""

class AnyBody(State):
    """Motion Control with arbitrary fields but minimal validation. Should not be subclassed. Subclass Motion instead for validation.

    Pass in names, joints, and any other fields to create a motion control.

    Example:
        >>> class ArmControl(MotionControl):
        ...     names: list[str] = MotionField(default_factory=list, description="Names of the joints.")
        ...     joints: list[float] = MotionField(
        ...         default_factory=lambda: np.zeros(3), bounds=[-1.0, 1.0], shape=(3,), description="Values of the joints."
        ...     )
        >>> arm_control = ArmControl(names=["shoulder", "elbow", "wrist"], joints=[0.1, 0.2])
        Traceback (most recent call last):
            ...
        ValueError: Number of joints 2 does not match number of names 3
        >>> arm_control = ArmControl(names=["shoulder", "elbow", "wrist"], joints=[3.0, 2.0, 1.0])
        Traceback (most recent call last):
            ...
        ValueError: joints item 0 (3.0) is out of bounds [-1.0, 1.0]
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="allow", populate_by_name=True)

    names: list[str] | None = None
    joints: list[float] | NumpyArray | Any = None


class Hand(Motion):
    """Action for a 7D space representing x, y, z, roll, pitch, yaw, and openness of the hand.

    This class represents the control for a robot hand, including its pose and grasp state.

    Attributes:
        pose (Pose): The pose of the robot hand, including position and orientation.
        grasp (float): The openness of the robot hand, ranging from 0 (closed) to 1 (open).

    Example:
        ```python
        from embdata.coordinate import Pose
        from embdata.motion.control import HandControl

        # Create a HandControl instance
        hand_control = HandControl(pose=Pose(position=[0.1, 0.2, 0.3], orientation=[0, 0, 0, 1]), grasp=0.5)

        # Access and modify the hand control
        hand_control.grasp = 0.8
        ```
    """

    pose: Pose = CoordsField(default_factory=Pose, description="Pose of the robot hand.")
    grasp: float = CoordsField(
        default=0,
        bounds=[-1, 1],
        description="Openness of the robot hand. 0 is closed, 1 is open.",
    )


class AbsoluteHand(Motion):
    pose: Pose = AbsoluteMotionField(default_factory=Pose, description="Pose of the robot hand.")
    grasp: float = AbsoluteMotionField(
        default=0,
        bounds=[-1, 1],
        description="Openness of the robot hand. 0 is closed, 1 is open.",
    )


class RelativePoseHand(Motion):
    pose: Pose = RelativeMotionField(default_factory=Pose, description="Pose of the robot hand.")
    grasp: float = AbsoluteMotionField(
        0,
        bounds=[-1, 1],  # [-1,1] so that 0 is a no-op.
        description="Openness of the robot hand. 0 is closed, 1 is open.",
    )


class Head(Motion):
    tilt: float = MotionField(0.0, description="Tilt of the robot head in radians (down is negative).")
    pan: float = MotionField(0.0, description="Pan of the robot head in radians (left is negative).")


class MobileSingleHand(Motion):
    """Control for a robot that can move its base in 2D space with a 6D EEF control + grasp."""

    # Location of the robot on the ground.
    base: PlanarPose | None = MotionField(
        default_factory=PlanarPose,
        description="Location of the robot on the ground.",
    )
    hand: Hand | NumpyArray[7, float] = MotionField(
        default_factory=Hand,
        description="Control for the robot hand.",
    )
    head: Head | NumpyArray[2, float] | None = MotionField(
        default=None,
        description="Control for the robot head.",
    )


class MobileSingleArmControl(Motion):
    """Control for a robot that can move in 2D space with a single arm."""

    base: PlanarPose | None = MotionField(
        default_factory=PlanarPose,
        description="Location of the robot on the ground.",
    )
    arm: NumpyArray | None = MotionField(
        default_factory=lambda: np.zeros(7),
        description="Control for the robot arm.",
    )
    head: Head | None = MotionField(default=None, description="Control for the robot head.")


class MobileBimanualArm(Motion):
    """Control for a robot that can move in 2D space with two arms."""

    base: PlanarPose | None = MotionField(
        default_factory=PlanarPose,
        description="Location of the robot on the ground.",
    )
    left_arm: NumpyArray | None = MotionField(
        default_factory=lambda: np.zeros(7),
        description="Control for the left robot arm.",
    )
    right_arm: NumpyArray | None = MotionField(
        default_factory=lambda: np.zeros(7),
        description="Control for the right robot arm.",
    )
    head: Head | None = MotionField(default=None, description="Control for the robot head.")


class Humanoid(Motion):
    """Control for a humanoid robot."""

    left_arm: NumpyArray | None = MotionField(
        default_factory=lambda: np.zeros(7),
        description="Control for the left robot arm.",
    )
    right_arm: NumpyArray | None = MotionField(
        default_factory=lambda: np.zeros(7),
        description="Control for the right robot arm.",
    )
    left_leg: NumpyArray | None = MotionField(
        default_factory=lambda: np.zeros(6),
        description="Control for the left robot leg.",
    )
    right_leg: NumpyArray | None = MotionField(
        default_factory=lambda: np.zeros(6),
        description="Control for the right robot leg.",
    )
    head: Head | None = MotionField(default=None, description="Control for the robot head.")

class HandTerminalState(Motion):
    """Terminal state for a hand control task."""

    hand: Hand | None = MotionField(
        default=None,
        description="State of the robot hand.",
    )
    done: bool | None = None
    """Whether the state is estimated to be terminal."""
    is_first: bool | None = None
    """Whether the state is first in a sequence."""
    is_last: bool | None = None
    """Whether the state is last in a sequence."""
