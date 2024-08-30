import numpy as np
from pydantic import Field, computed_field

from embdata.coordinate import Coordinate
from embdata.geometry import Transform3D as Extrinsics
from embdata.ndarray import NumpyArray
from embdata.sample import Sample


class Intrinsics(Coordinate):
    """Transformation from 3D to 2D coordinates for a pinhole camera model."""

    fx: float = 0.0
    """Focal length in x direction."""
    fy: float = 0.0
    """Focal length in y direction."""
    cx: float = 0.0
    """Optical center in x direction."""
    cy: float = 0.0
    """Optical center in y direction."""

    @computed_field
    def matrix(self) -> NumpyArray[3, 3, float]:
        """Convert the intrinsic parameters to a 3x3 matrix."""
        return np.array(
            [
                [self.fx, 0.0, self.cx],
                [0.0, self.fy, self.cy],
                [0.0, 0.0, 1.0],
            ],
        )


class Distortion(Coordinate):
    """Model for Camera Distortion Parameters."""

    k1: float = 0.0
    """Radial distortion coefficient k1."""
    k2: float = 0.0
    """Radial distortion coefficient k2."""
    p1: float = 0.0
    """Tangential distortion coefficient p1."""
    p2: float = 0.0
    """Tangential distortion coefficient p2."""
    k3: float = 0.0
    """Radial distortion coefficient k3."""


class Camera(Sample):
    """Model for Camera Parameters."""

    intrinsic: Intrinsics = Field(default_factory=Intrinsics, description="Intrinsic parameters of the camera")
    distortion: Distortion = Field(default_factory=Distortion, description="Distortion parameters of the camera")
    extrinsic: Extrinsics = Field(default_factory=Extrinsics, description="Extrinsic parameters of the camera")
    depth_scale: float = 1.0

    def project(self, xyz: NumpyArray[3, float]) -> NumpyArray[2, float]:
        """Project 3D world coordinates to 2D pixel coordinates."""
        xyz_camera = self.extrinsic.transform(xyz)
        x_pixel = (self.intrinsic.fx * xyz_camera[0] / xyz_camera[2]) + self.intrinsic.cx
        y_pixel = (self.intrinsic.fy * xyz_camera[1] / xyz_camera[2]) + self.intrinsic.cy
        return np.array([x_pixel, y_pixel])

    def deproject(self, uv: NumpyArray[2, int], depth_image: np.ndarray) -> NumpyArray[3, float]:
        """Deproject 2D pixel coordinates from the depth image to 3D world coordinates.

        Args:
            uv (NumpyArray[2, float]): The (u, v) coordinates of the pixel.
            depth_image (np.ndarray): The depth image.
            depth_scale (float): The depth scale factor for the RealSense camera.

        Returns:
            NumpyArray[3, float]: The (x, y, z) coordinates in 3D space.

        Example:
            >>> estimator = ArucoMarkerBasedObjectPoseEstimation(color_image, depth_image, intrinsic_matrix)
            >>> uv = np.array([320, 240])
            >>> point_3d = estimator.deproject(uv, depth_image, 0.001)
            >>> print(point_3d)
        """
        u, v = uv
        depth = depth_image[int(v), int(u)] * self.depth_scale
        x = (u - self.intrinsic.cx) * depth / self.intrinsic.fx
        y = (v - self.intrinsic.cy) * depth / self.intrinsic.fy
        z = depth
        return np.array([x, y, z])

