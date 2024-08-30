from functools import wraps
from importlib.resources import files
from typing import Any, Generic, Iterator, List, TypeVar

import numpy as np
from aiocache import cached
from lager import log
from multidict import MultiDict
from pydantic import Field, model_validator
import requires

from embdata.sense.state import State
from embdata.coordinate import Coordinate, Pose6D
from embdata.geometry import Transform3D
from embdata.ndarray import NumpyArray
from embdata.sample import Sample
from embdata.sense.camera import Camera
from embdata.sense.depth import Depth, Plane
from embdata.sense.image import Image
from embdata.utils.geometry_utils import rotation_from_z


class BBox2D(Coordinate):
    """Model for 2D Bounding Box."""

    x1: float
    y1: float
    x2: float
    y2: float

    @classmethod
    def from_list(cls, bbox_list: list[float]) -> "BBox2D":
        return cls(x1=bbox_list[0], y1=bbox_list[1], x2=bbox_list[2], y2=bbox_list[3])


class BBox3D(Coordinate):
    """Model for 3D Bounding Box."""

    x1: float
    y1: float
    z1: float
    x2: float
    y2: float
    z2: float

    @classmethod
    def from_list(cls, bbox_list: list[float]) -> "BBox3D":
        return cls(x1=bbox_list[0], y1=bbox_list[1], z1=bbox_list[2], x2=bbox_list[3], y2=bbox_list[4], z2=bbox_list[5])

class PixelCoords(Coordinate):
    """Model for Pixel Coordinates."""

    u: int
    v: int

    @classmethod
    def from_list(cls, coords_list: list[int]) -> "PixelCoords":
        return cls(u=coords_list[0], v=coords_list[1])

T= TypeVar("T")
class Collection(MultiDict, Generic[T]):
    """Model for Collection Data."""
    def __getitem__(self, item: int | str) -> T:
        if isinstance(item, int):
            return self[list(self.keys())[item]]
        return super().__getitem__(item)

    def __iter__(self) -> Iterator[T]:
        yield from (i if isinstance(i, list) else v for v in self.values() for i in v)

    def __len__(self) -> int:
        return len(list(iter(self)))

    def __getattr__(self, item: str) -> T | List[T]:
        if "__" in item or "pydantic" in item:
            return super().__getattr__(item)
        return self[item]

    def __contains__(self, item: T) -> bool:
        return item in self.values()

    def append(self, item: T) -> "Collection[T]":
        self[item.name] = item
        return self

    @staticmethod
    def concat(collections: List["Collection[T]"]) -> "Collection[T]":
        return sum(collections, Collection[T]())

    @staticmethod
    def from_list(data: List[T]) -> "Collection[T]":
        return Collection[T]({item.name if hasattr(item, __name__) else item.__class__.__name__: item for item in data})



class RealObject(Sample):
    """Model for world Object. It describes the objects in the scene.

    Attributes:
        name (str): The name of the object.
        bbox_2d (BBox2D | None): The 2D bounding box of the object.
        bbox_3d (BBox3D | None): The 3D bounding box of the object.
        pose (Pose | None): The pose of the object.
        pixel_coords (PixelCoords | None): The pixel coordinates of the object.
        mask (NumpyArray | None): The mask of the object.
    """

    name: str = ""
    bbox_2d: BBox2D | None = None
    bbox_3d: BBox3D | None = None
    volume: float | None = None
    pose: Pose6D | None = None
    pixel_coords: PixelCoords | None = None
    mask: NumpyArray | None = None


class World(State):
    """Model for World Data.

    To keep things simple, always keep the objects in the camera frame. Perform transformations during access.
    """

    image: Image | None = None
    depth: Depth | None = None
    annotated: Image | None = None
    objects: Collection[RealObject] = Field(default_factory=Collection, description="List of scene objects")
    camera_params: Camera = Field(default_factory=Camera, description="Camera parameters of the scene")


    def __getitem__(self, item):
        # Access the underlying dictionary directly to avoid recursion
        if item in self.objects:
            return self.objects[item]
        return getattr(self, item)


    def object_names(self) -> List[str]:
        return list({obj.name for obj in self.objects} | {"plane", "camera"})

    def add_object(self, obj: RealObject) -> None:
        self.objects.append(obj)

    @model_validator(mode="before")
    @classmethod
    def validate(cls, v: Any) -> Any:
        if isinstance(v.get("objects"), list):
            for obj in v["objects"]:
                if isinstance(obj["bbox_2d"], list):
                    obj["bbox_2d"] = BBox2D.from_list(obj["bbox_2d"])
                if isinstance(obj["pixel_coords"], list):
                    obj["pixel_coords"] = PixelCoords.from_list(obj["pixel_coords"])
            v["objects"] = Collection[RealObject](**{obj["name"]: RealObject(**obj) if isinstance(obj, dict) else obj for obj in v["objects"]})
            return v
        return None
    

    @wraps("World.get_object")
    @cached(ttl=10)
    def aget_object(self, name: str, reference: str | RealObject | Pose6D | np.ndarray = "camera") -> RealObject | None:
        return self.get_object(name, reference)

    def get_object(self, name: str, reference: str | RealObject | Pose6D | np.ndarray = "camera") -> RealObject | List[RealObject] | None:
        """Get the object(s) from the scene in the specified reference frame.

        If name is "all", returns all objects in the specified reference frame.
        If reference is another object name, return the pose relative to that object.

        Args:
            name (str): The name of the object. Use "all" to get all objects.
            reference (str | RealObject | Pose6D | np.ndarray): The reference frame or object of the object(s).

        Returns:
            RealObject | List[RealObject] | None: The object(s) in the specified reference frame or None if the object does not exist.

        Example:
            >>> world.get_object("object1", reference="camera")
            RealObject(name="object1", pose=Pose(x=0.0, y=0.2032, z=0.0, roll=-1.5707963267948966, pitch=0.0, yaw=-1.57), pixel_coords=PixelCoords(u=320, v=240))

            >>> world.get_object("all", reference="plane")
            [RealObject(name="object1", pose=Pose(x=0.0, y=0.2032, z=0.0, roll=0.0, pitch=0.0, yaw=0.0), pixel_coords=PixelCoords(u=320, v=240)),
            RealObject(name="object2", pose=Pose(x=0.1, y=0.2032, z=0.1, roll=0.0, pitch=0.0, yaw=0.0), pixel_coords=PixelCoords(u=400, v=300))]
        """
        if name == "all":
            return [self.get_object(obj.name, reference) for obj in self.objects]

        # Get the target object
        target = self.objects[name]
        new_target = target.model_copy()

        if not hasattr(self, "plane"):
            # Ensure the plane is segmented
            self.plane: Plane = self.depth.segment_plane(threshold=0.01, min_samples=3, max_trials=1000)
            normal = self.plane.normal(self.plane.coefficients)
            rotation_matrix = rotation_from_z(-normal)
            self.transform = Transform3D(rotation=rotation_matrix)

        # Obtain the reference object
        if isinstance(reference, str):
            if reference == "camera":
                reference_obj = RealObject(name="camera", pose=Pose6D())
            elif reference == "plane":
                reference_obj = RealObject(name="plane", pose=Pose6D())  # Placeholder for the plane pose
            else:
                reference_obj = self.objects.get(reference)
                if reference_obj is None:
                    raise ValueError(f"Reference object '{reference}' not found.")
        elif isinstance(reference, RealObject):
            reference_obj = reference
        elif isinstance(reference, (Pose6D, np.ndarray)):
            reference_obj = RealObject(name="custom_reference", pose=Pose6D(*reference) if isinstance(reference, np.ndarray) else reference)
        else:
            raise TypeError("Reference must be a string, RealObject, Pose6D, or numpy array.")
        
        # If the target or reference does not have a pose, compute it
        if target.pose is None:
            point_3d = self.depth.camera_params.deproject(target.pixel_coords, depth_image=self.depth.array)
            target.pose = Pose6D(*point_3d, roll=0, pitch=0, yaw=0)
        
        if reference_obj.pose is None:
            point_3d = self.depth.camera_params.deproject(reference_obj.pixel_coords, depth_image=self.depth.array)
            reference_obj.pose = Pose6D(*point_3d, roll=0, pitch=0, yaw=0)

        if reference_obj.name != "camera":
            target_pose = self.transform.transform(target.pose.numpy()[:3])
            reference_pose = self.transform.transform(reference_obj.pose.numpy()[:3])

        else:
            target_pose, reference_pose = target.pose, reference_obj.pose

        new_target.pose = Pose6D(*(target_pose - reference_pose), roll=0, pitch=0, yaw=0)

        return new_target

    @requires("open3d")
    def show(self):
        import open3d as o3d
        import open3d.visualization as vis
        """Display the world state."""

        self.plane.point_cloud.transform(self.transform.matrix())
        self.objects = self.get_object("all", reference="plane")
        inlier_cloud = self.plane.point_cloud.select_by_index(self.plane.inliers)
        outlier_cloud = self.plane.point_cloud.select_by_index(self.plane.inliers, invert=True)

        # Color the inliers red
        inlier_cloud.paint_uniform_color([1, 0, 0])

        geometries = [self.plane.point_cloud] + [o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.1, origin=obj.pose.numpy()[:3]) for obj in self.objects] + [inlier_cloud, outlier_cloud] + [o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.1, origin=Pose6D(x=0, y=0, z=0, roll=0, pitch=0, yaw=0).numpy()[:3])]
        vis.draw_geometries(geometries)

if __name__ == "__main__":

    from embdata.sense.camera import Camera, Intrinsics, Distortion, Extrinsics 
    from mbodied.agents.sense.object_detection_agent import ObjectDetectionAgent

    object_detection_agent = ObjectDetectionAgent()

    rgb_image = Image(path="embodied-agents/resources/color_image.png", encoding="png", mode="RGB")

    object_names = ["Remote Control, Spoon, Basket, Red Marker"]

    world: World = object_detection_agent.act(image=rgb_image, objects=object_names)

    depth = Depth(path="embodied-agents/resources/depth_image.png", encoding="png", mode="I", size=(1280, 720),
                  rgb=Image(path="embodied-agents/resources/color_image.png", encoding="png", mode="RGB"), 
                  camera_params=Camera(intrinsic=Intrinsics(fx=911.0, fy=911.0, cx=653.0, cy=371.0), 
                                       distortion=Distortion(k1=0.0, k2=0.0, p1=0.0, p2=0.0, k3=0.0),
                                       extrinsic=Extrinsics(),
                                       depth_scale=0.001),
                    depth_unit="mm",
                )
    
    world.depth = depth
    world.camera_params = depth.camera_params
    world.image = rgb_image

    relative_pose = world.get_object("Spoon", reference="Remote Control")

    # world.show()