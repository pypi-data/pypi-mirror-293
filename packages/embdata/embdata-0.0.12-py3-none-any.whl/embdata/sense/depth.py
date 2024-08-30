# Copyright 2024 mbodi ai
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Wrap any common image representation in an Image class to convert to any other common format.

The following image representations are supported:
- NumPy array
- PIL Image
- Base64 encoded string
- File path
- URL
- Bytes object

The image can be resized to and from any size, compressed, and converted to and from any supported format:

```python
image = Image("path/to/image.png", size=new_size_tuple).save("path/to/new/image.jpg")
image.save("path/to/new/image.jpg", quality=5)

TODO: Implement Lazy attribute loading for the image data.
"""

import tempfile
from functools import cached_property, wraps
from pathlib import Path
from typing import Any, ClassVar, Dict, List, SupportsBytes, Tuple, Union

import cv2
import numpy as np
import requires
from lager import log
from PIL.Image import Image as PILImage
from pydantic import (
    AnyUrl,
    Base64Str,
    FilePath,
    PrivateAttr,
    computed_field,
)
from typing_extensions import Literal

from embdata.coordinate import Plane
from embdata.ndarray import NumpyArray
from embdata.sample import Sample
from embdata.sense.camera import Camera
from embdata.sense.image import Image
from embdata.utils.import_utils import smart_import
from embdata.units import LinearUnit

SupportsImage = Union[np.ndarray, PILImage, Base64Str, AnyUrl, FilePath]  # noqa: UP007

DepthImageLike = NumpyArray[1, Any, Any, np.uint16] | NumpyArray[Any, Any, np.uint16]

PointCloudLike = NumpyArray[Any, 3, np.float32]

class Depth(Sample):
    """A class for representing depth images and points."""

    DEFAULT_MODE: ClassVar[str] = "I"
    SOURCE_TYPES: ClassVar[List[str]] = ["path", "array", "base64", "bytes", "url", "pil", "points"]
    mode: Literal["RGB", "RGBA", "L", "P", "CMYK", "YCbCr", "I", "F"] = DEFAULT_MODE
    points: NumpyArray[Any, 3, np.float32] | None = None
    encoding: Literal["png"] = "png"
    size: Tuple[int, int] | None = None
    camera_params: Camera | None = None
    path: str | Path | FilePath | None = None

    _url: AnyUrl | None = PrivateAttr(default=None)
    _array: NumpyArray[Any, Any, np.uint16] | None = PrivateAttr(default=None)
    _rgb: Image | None = PrivateAttr(default=None)

    @computed_field(return_type=NumpyArray[Any, Any, 3, np.uint16])
    @property
    def array(self) -> NumpyArray[Any, Any, 3, np.uint16]:
        """The raw depth image represented as a NumPy array."""
        return self._array if self._array is not None else None

    @computed_field(return_type=AnyUrl)
    @property
    def url(self) -> AnyUrl:
        """The raw depth image represented as a NumPy array."""
        if self._url is None:
            return f"data:image/{self.encoding};base64,{self.base64}"
        return None

    @url.setter
    def url(self, value: AnyUrl) -> AnyUrl:
        self._url = value
        return self._url

    @array.setter
    def array(self, value: NumpyArray[Any, Any, np.uint16] | None) -> NumpyArray[Any, Any, 3, np.uint16]:
        self._array = value
        if self._array is not None:
            self.size = (self._array.shape[1], self._array.shape[0])
        return self._array if value is not None else None

    @computed_field(return_type=Image)
    @property
    def rgb(self) -> Image:
        """Convert the depth image to an RGB image."""
        if self._rgb is None:
            if self.array is None:
                msg = "The depth array must be set to convert to an RGB image."
                raise ValueError(msg)
            normalized_array = cv2.normalize(self.array, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            rgb_image = Image(normalized_array, mode="RGB")
            self._rgb = rgb_image
        return self._rgb

    @rgb.setter
    def rgb(self, value: Image) -> Image:
        if not isinstance(value, Image):
            raise TypeError("rgb must be an instance of Image")
        if self.array is not None and value.size != (self.array.shape[1], self.array.shape[0]):
            raise ValueError("The size of the RGB image must match the size of the depth image.")
        self._rgb = value
        return self._rgb

    @classmethod
    def supports_pointcloud(cls, arg: Any) -> bool:
        """Check if the argument is a point cloud."""
        return isinstance(arg, np.ndarray) and arg.ndim == 2 and arg.shape[1] == 3

    @computed_field(return_type=NumpyArray[Any, 3, np.uint16])
    @cached_property
    def pil(self) -> PILImage:
        """The PIL image object."""
        if self.array is None:
            msg = "The array must be set to convert to a PIL image."
            raise ValueError(msg)
        return Image(self.array, mode="I").pil

    @computed_field(return_type=Base64Str)
    @cached_property
    def base64(self) -> Base64Str:
        """The base64 encoded string of the image."""
        if self.array is None:
            msg = "The array must be set to convert to a base64 string."
            raise ValueError(msg)
        return Image(self.array, mode="I").base64

    @computed_field
    @cached_property
    def url(self) -> str:
        """The URL of the image."""
        return f"data:image/{self.encoding};base64,{self.base64}"

    def __init__(  # noqa
        self,
        arg: SupportsImage | DepthImageLike | None = None,
        points: DepthImageLike | None = None,
        path: str | Path | FilePath| None = None,
        array: np.ndarray | None = None,
        base64: Base64Str | None = None,
        rgb: Image | None = None,
        camera_params: Camera | None = None,
        encoding: str = "png",
        size: Tuple[int, ...] | None = None,
        bytes: SupportsBytes | None = None,  # noqa
        unit: LinearUnit | None = None,
        mode: Literal["RGB", "RGBA", "L", "P", "CMYK", "YCbCr", "I", "F"] | None = "I",
        **kwargs,
    ):
        """Initializes a Depth representation. Unlike the Image class, an empty array is used as the default image.

        Args:
            arg (SupportsImage, optional): The primary image source.
            url (Optional[str], optional): The URL of the image.
            path (Optional[str], optional): The file path of the image.
            base64 (Optional[str], optional): The base64 encoded string of the image.
            array (Optional[np.ndarray], optional): The numpy array of the image.
            pil (Optional[PILImage], optional): The PIL image object.
            encoding (Optional[str], optional): The encoding format of the image. Defaults to 'jpeg'.
            size (Optional[Tuple[int, int]], optional): The size of the image as a (width, height) tuple.
            bytes (Optional[bytes], optional): The bytes object of the image.
            mode (Optional[str], optional): The mode to use for the image. Defaults to 'RGB'.
            **kwargs: Additional keyword arguments.
        """
        kwargs["path"] = path
        kwargs["array"] = array
        kwargs["base64"] = base64
        kwargs["bytes"] = bytes
        kwargs["encoding"] = encoding
        kwargs["size"] = size
        kwargs["mode"] = mode
        kwargs["points"] = points
        kwargs["camera_params"] = camera_params
        kwargs["unit"] = unit
        if not self.supports_pointcloud(arg):
            points = kwargs.pop("points", None)

            kwargs["mode"] = "I"
            kwargs["encoding"] = "png"
            num_keys = 0

            for (
                k,
                v,
            ) in kwargs.items():
                if v is not None and k in self.SOURCE_TYPES:
                    num_keys += 1
            if num_keys > 1:
                msg = "Only one of the following arguments can be provided: path, array, base64, bytes, url, pil, points."
                raise ValueError(msg)

            if rgb or isinstance(arg, Image) and arg.mode == "RGB":
                # case 1: arg is an RGB image
                rgb = arg if isinstance(arg, Image) else rgb
            elif isinstance(arg, Image | PILImage):
                # case 2: arg is a depth image
                if arg.mode == "RGB":
                    msg = "The RGB image must be provided as the 'rgb' argument."
                    raise ValueError(msg)
                points = kwargs.pop("points", None)
                rgb = Image(arg, **kwargs)
                kwargs["points"] = points

        super().__init__(**kwargs)
        # Set self.array directly if array is provided as the source
        if array is not None:
            self._array = array
        elif any(kwargs.get(k) is not None for k in self.SOURCE_TYPES):
            # Otherwise, initialize from another source type if provided
            self._array = Image(arg, **kwargs).array
        else:
            self._array = None

        if rgb is not None:
            self.rgb = rgb
        self.camera_params = camera_params
        self._url = kwargs.get("url")

    @classmethod
    def from_pil(cls, pil: PILImage, **kwargs) -> "Depth":
        """Create an image from a PIL image."""
        array = np.array(pil.convert("I"), dtype=np.uint16)
        kwargs.update({"encoding": "png", "size": pil.size, "mode": cls.DEFAULT_MODE})
        return cls(array=array, **kwargs)

    def segment_plane(
        self,
        threshold: float = 0.01,
        min_samples: int = 3,
        max_trials: int = 1000,
    ) -> Plane:
        """Segments a plane from the point cloud generated from RGB and depth images.

        Args:
            rgb_image_path (str): Path to the RGB image.
            instrisic (Intrinsics): Camera intrinsic parameters.
            threshold (float, optional): Distance threshold for plane segmentation. Defaults to 0.01.
            min_samples (int, optional): Minimum samples for RANSAC. Defaults to 3.
            max_trials (int, optional): Maximum trials for RANSAC. Defaults to 1000.
            canonicalize (bool, optional): Whether to canonicalize the point cloud. Defaults to False.

        Returns:
            tuple: Contains the plane model, inliers, inlier cloud, outlier cloud, and the point cloud.
        """
        o3d = smart_import("open3d", mode="eager")
        
        if self.unit == "m":
            self.array = (self.array * 1000).astype(np.uint16)
        else:
            self.array = self.array.astype(np.uint16)

        width, height = self.size
        rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(
            o3d.geometry.Image(self.rgb.array),
            o3d.geometry.Image(self.array),
            depth_scale=1000.0,
            depth_trunc=2.0,
            convert_rgb_to_intensity=False,
        )

        intrinsics = o3d.camera.PinholeCameraIntrinsic(
            width,
            height,
            self.camera_params.intrinsic.fx,
            self.camera_params.intrinsic.fy,
            self.camera_params.intrinsic.cx,
            self.camera_params.intrinsic.cy,
        )

        pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image, intrinsics)

        plane_model, inliers = pcd.segment_plane(
            distance_threshold=threshold,
            ransac_n=min_samples,
            num_iterations=max_trials,
        )

        return Plane(coefficients=plane_model, inliers=inliers, point_cloud=pcd)

    def colormap(self, **kwargs) -> Image:
        """Postprocess the depth array and convert it to an RGB image with a colormap applied."""
        if self.array is None and self.rgb is None:
            msg = "The depth array or RGB image must be set to convert to a colormap image."
            raise ValueError(msg)
        plt = smart_import("matplotlib.pyplot", mode="lazy")

        if plt.__name__ == "matplotlib.pyplot":
            import torch

            # Normalize the depth array to [0, 255] range and convert to uint8
            depth_normalized = cv2.normalize(self.array, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

            # Ensure the depth_normalized has the shape (H, W)
            if len(depth_normalized.shape) == 3 and depth_normalized.shape[2] == 1:
                depth_normalized = depth_normalized.squeeze(2)  # Convert shape from (H, W, 1) to (H, W)

            # Convert the depth array to a torch tensor and add a batch and channel dimension
            depth_tensor = torch.tensor(depth_normalized).unsqueeze(0).unsqueeze(0).float()  # Shape: (1, 1, H, W)

            # Interpolate to the original size using bicubic interpolation
            depth_8bit = (
                torch.nn.functional.interpolate(
                    depth_tensor,
                    size=self.size,
                    mode="bicubic",
                    align_corners=False,
                )
                .squeeze(0)
                .squeeze(0)
            )  # Shape: (H, W)

            # Convert tensor back to numpy array for colormap application
            output = depth_8bit.cpu().numpy()

            # Apply a colormap (e.g., inferno) to the normalized depth image
            colormap_image = plt.cm.inferno(output / 255.0)  # Normalize to [0, 1] for colormap

            # Convert to RGB format and save to a temporary file
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
                plt.imsave(f.name, colormap_image, format="png", **kwargs)
                saved_image_path = f.name
                log.info("Saved colormap image to %s", saved_image_path)

            # Open the saved image file as an RGB Image object
            image = Image.open(saved_image_path).convert("RGB")

            return Image(image)
        # Fallback to creating an Image using the depth array if matplotlib is unavailable
        return Image(self.array, mode="I", encoding="png")

    def show(self) -> None:
        Image(self.colormap()).show()

    @wraps(Image.save, assigned=("__doc__"))
    def save(self, *args, **kwargs) -> None:
        """Save the image to a file."""
        self.colormap().save(*args, **kwargs)

    @requires("sklearn")
    def segment_cylinder(
        self,
        min_samples=3,
        threshold: float = 0.01,
        max_trials: int = 1000,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Segment the largest cylinder using RANSAC.

        Args:
            min_samples (int): The minimum number of data points to fit a model.
            threshold (float): The maximum distance for a point to be considered as an inlier.
            max_trials (int): The maximum number of iterations for RANSAC.

        Returns:
            Tuple[np.ndarray, np.ndarray]: The inlier points and their indices.
        """
        from sklearn.linear_model import RANSACRegressor
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import PolynomialFeatures
        poly = PolynomialFeatures(degree=2)
        ransac = make_pipeline(
            poly,
            RANSACRegressor(min_samples=min_samples, residual_threshold=threshold, max_trials=max_trials),
        )

        X = self.points[:, :2]  # Assuming self.points is of shape (n_points, 3)
        y = self.points[:, 2]

        ransac.fit(X, y)

        inlier_mask = ransac.named_steps["ransacregressor"].inlier_mask_
        inlier_points = self.points[inlier_mask]
        inlier_indices = np.where(inlier_mask)[0]

        return inlier_points, inlier_indices


    def cluster_points(self, n_clusters: int = 3) -> List[int]:
        """Cluster the points using KMeans.

        Args:
            n_clusters (int): The number of clusters to form.

        Returns:
            List[int]: The cluster labels for each point.
        """
        smart_import("sklearn.cluster")
        from sklearn.cluster import KMeans
        kmeans = KMeans(n_clusters=n_clusters)
        return kmeans.fit_predict(self.points.T)
    
