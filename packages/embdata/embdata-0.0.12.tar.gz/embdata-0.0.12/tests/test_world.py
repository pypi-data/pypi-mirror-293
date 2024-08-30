import time
import time
from embdata.sense.depth import Depth, Plane
from embdata.sense.world import World, RealObject, PixelCoords
from embdata.sense.image import Image
from embdata.sense.camera import Camera, Distortion, Intrinsics
from embdata.geometry import Transform3D
from embdata.utils.geometry_utils import rotation_between_two_points
from embdata.coordinate import Coordinate, Point, Pose6D
from lager import log
import numpy as np
import pytest
from embdata.coordinate import Pose
from importlib_resources import files

import open3d as o3d

WORLD_POSE = Pose(x=0.0, y=0.2032, z=0.0, roll=-np.pi/2, pitch=0.0, yaw=-np.pi/2)
CAMERA_PARAMS = Camera(
    intrinsic=Intrinsics(fx=911, fy=911, cx=653, cy=371), 
    distortion=Distortion(k1=0.0, k2=0.0, p1=0.0, p2=0.0, k3=0.0),
    depth_scale=0.001
)

DEFAULT_WORLD = World(
    objects=[RealObject(name="object1", pose=Pose(), pixel_coords=PixelCoords(u=320, v=240))],
    image=Image(array=np.zeros([480, 640, 3], dtype=np.uint8), mode="RGB", encoding="png"), 
    depth=Depth(path=files("embdata") / "resources/depth_image.png",
              mode="I", 
              encoding="png", 
              size=(1280, 720),
              camera_params=CAMERA_PARAMS, 
              rgb=Image(path=files("embdata") / "resources/color_image.png", mode="RGB", encoding="png"),
              depth_unit="mm"),
    camera_params=CAMERA_PARAMS
)

@pytest.fixture
def setup_world_pose() -> Pose:
    return Pose(x=0.0, y=0.2032, z=0.0, roll=-np.pi/2, pitch=0.0, yaw=-np.pi/2)

@pytest.fixture
def setup_camera_params() -> Camera:
    return Camera(
        intrinsic=Intrinsics(fx=911, fy=911, cx=653, cy=371), 
        distortion=Distortion(k1=0.0, k2=0.0, p1=0.0, p2=0.0, k3=0.0),
        depth_scale=0.001
    )

@pytest.fixture
def depth_image_path() -> Image:
    return files("embdata") / "resources/depth_image.png"

@pytest.fixture
def color_image_path():
    return  files("embdata") / "resources/color_image.png"

@pytest.fixture
def setup_example_scene(setup_camera_params: Camera, depth_image_path, color_image_path) -> World:
    return World(
        objects=[RealObject(name="object1", pose=Pose(), pixel_coords=PixelCoords(u=320, v=240))],
        image=Image(array=np.zeros([480, 640, 3], dtype=np.uint8), mode="RGB", encoding="png"), 
        depth=Depth(path=depth_image_path,
                  mode="I", 
                  encoding="png", 
                  size=(1280, 720),
                  camera_params=setup_camera_params, 
                  rgb=Image(path=color_image_path, mode="RGB", encoding="png"),
                  depth_unit="mm"),
        camera_params=setup_camera_params
    )


def test_get_object(setup_example_scene: World):
    example_scene = setup_example_scene
    depth = example_scene.depth

    # Perform plane segmentation
    plane_normal: Coordinate = depth.segment_plane(threshold=0.01, min_samples=3, max_trials=1000)
    normal = plane_normal.normal(plane_normal.coefficients)
    np.allclose(normal, Point(**{'x': 0.017803989474007905, 'y': 0.9977034758324792, 'z': 0.06535129892051982}).numpy())
    # Define the origin and z-axis
    result = example_scene.get_object("object1", reference="plane")
    assert result is not None

    # result = example_scene.get_object("all", reference="plane")
    # assert result is not None
    # result = example_scene.get_object("all", reference="plane")
    # assert result is not None

    # result = example_scene.get_object("object1", reference="object1")
    # assert result is not None
    # result = example_scene.get_object("object1", reference="object1")
    # assert result is not None



