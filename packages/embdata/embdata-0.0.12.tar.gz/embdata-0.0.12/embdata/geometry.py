import numpy as np
from pydantic import Field
from typing_extensions import Literal

from embdata.ndarray import NumpyArray
from embdata.sample import Sample
from embdata.utils.geometry_utils import rotation_matrix_to_rpy, rpy_to_rotation_matrix


class Transform2D(Sample):
    """Represents a general 2D transformation including rotation and translation."""

    rotation: NumpyArray[2, 2, float] = Field(
        default_factory=lambda: np.eye(2),
        description="Rotation matrix (2x2) representing orientation.",
    )
    translation: NumpyArray[2, float] = Field(
        default_factory=lambda: np.zeros(2),
        description="Translation vector (2x1) representing position.",
    )

    def matrix(self) -> NumpyArray[3, 3, float]:
        """Convert the transformation to a 3x3 homogeneous transformation matrix."""
        matrix = np.eye(3)
        matrix[:2, :2] = self.rotation
        matrix[:2, 2] = self.translation
        return matrix

    def __mul__(self, other: "Transform2D") -> "Transform2D":
        """Combine this transformation with another."""
        rotation = np.dot(self.rotation, other.rotation)
        translation = np.dot(self.rotation, other.translation) + self.translation
        return Transform2D(rotation=rotation, translation=translation)

    def __matmul__(self, point: NumpyArray[2, float]) -> NumpyArray[2, float]:
        """Apply the transformation to a 2D point."""
        return self.transform(point)

    def inverse(self) -> "Transform2D":
        """Compute the inverse of the transformation."""
        inverse_rotation = self.rotation.T
        inverse_translation = -np.dot(inverse_rotation, self.translation)
        return Transform2D(rotation=inverse_rotation, translation=inverse_translation)

    def transform(self, points: NumpyArray[2, float] | NumpyArray[..., 2, float]) -> NumpyArray[..., 2, float]:
        """Transform a single point or a list of points using this transformation.

        Args:
            points: A single point (shape: [2]) or a list of points (shape: [N, 2])

        Returns:
            Transformed point(s) with the same shape as the input.
        """
        if points.ndim == 1:
            # Single point
            return np.dot(self.rotation, points) + self.translation
        if points.ndim == 2:
            # List of points
            return np.dot(points, self.rotation.T) + self.translation

        msg = "Input must be a 1D or 2D array representing point(s)."
        raise ValueError(msg)

    @classmethod
    def from_pose(cls, pose: NumpyArray[3, float]) -> "Transform2D":
        """Create a 2D transformation from a planar pose."""
        x, y, theta = pose
        rotation = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
        translation = np.array([x, y])
        return cls(rotation=rotation, translation=translation)


class Transform3D(Sample):
    """Represents a general 3D transformation including rotation and translation."""

    rotation: NumpyArray[3, 3, float] = Field(
        default_factory=lambda: np.eye(3),
        description="Rotation matrix (3x3) representing orientation.",
    )
    translation: NumpyArray[3, float] = Field(
        default_factory=lambda: np.zeros(3),
        description="Translation vector (3x1) representing position.",
    )

    def matrix(self) -> NumpyArray[4, 4, float]:
        """Convert the transformation to a 4x4 homogeneous transformation matrix."""
        matrix = np.eye(4)
        matrix[:3, :3] = self.rotation
        matrix[:3, 3] = self.translation
        return matrix

    def __mul__(self, other: "Transform3D") -> "Transform3D":
        """Combine this transformation with another."""
        rotation = np.dot(self.rotation, other.rotation)
        translation = np.dot(self.rotation, other.translation) + self.translation
        return Transform3D(rotation=rotation, translation=translation)

    def __matmul__(self, point: NumpyArray[3, float]) -> NumpyArray[3, float]:
        """Apply the transformation to a 3D point."""
        return self.transform(point)

    def inverse(self) -> "Transform3D":
        """Compute the inverse of the transformation."""
        inverse_rotation = self.rotation.T
        inverse_translation = -np.dot(inverse_rotation, self.translation)
        return Transform3D(rotation=inverse_rotation, translation=inverse_translation)

    @classmethod
    def from_pose(cls, pose: NumpyArray[6, float]) -> "Transform3D":
        """Create a 3D transformation from a pose."""
        x, y, z, roll, pitch, yaw = pose
        rotation = rpy_to_rotation_matrix([roll, pitch, yaw])
        translation = np.array([x, y, z])
        return cls(rotation=rotation, translation=translation)

    def transform(self, points: NumpyArray[3, float] | NumpyArray[..., 3, float]) -> NumpyArray[..., 3, float]:
        """Transform a single point or a list of points using this transformation.

        Args:
            points: A single point (shape: [3]) or a list of points (shape: [N, 3])

        Returns:
            Transformed point(s) with the same shape as the input.
        """
        if points.ndim == 1:
            # Single point
            return np.dot(self.rotation, points) + self.translation
        if points.ndim == 2:
            # List of points
            return np.dot(points, self.rotation.T) + self.translation

        msg = "Input must be a 1D or 2D array representing point(s)."
        raise ValueError(msg)

    def rpy(self, sequence: Literal["zyx", "xyz"] = "zyx") -> NumpyArray[3, float]:
        """Convert the rotation matrix to roll, pitch, yaw angles using the specified sequence."""
        return rotation_matrix_to_rpy(self.rotation, sequence)

    @classmethod
    def from_rpy(cls, rpy: NumpyArray[3, float], sequence: Literal["zyx", "xyz"] = "zyx") -> "Transform3D":
        """Create a 3D transformation from roll, pitch, and yaw angles."""
        rotation = rpy_to_rotation_matrix(rpy, sequence)
        return cls(rotation=rotation)
