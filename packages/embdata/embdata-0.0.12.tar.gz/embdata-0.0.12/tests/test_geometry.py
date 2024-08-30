import math
import pytest
import numpy as np
from math import isclose
from embdata.coordinate import Coordinate, Pose6D, CoordinateField, PlanarPose
import math
from embdata.sense.image import Image

@pytest.fixture
def pose():
    class Pose(Pose6D):
        x: float = CoordinateField(0.0, unit="m", bounds=(0, 10))

    return Pose


def test_coordinate_creation():
    coord = Coordinate()
    assert coord is not None


def test_coordinate_fields():
    coord = PlanarPose()
    assert coord.x == 0.0
    assert coord.y == 0.0
    assert coord.theta == 0.0


def test_coordinate_bounds():
    coord = PlanarPose()
    coord.x = 5.0
    coord.y = 10.0
    coord.theta = 1.57
    assert coord.x == 5.0
    assert coord.y == 10.0
    assert isclose(coord.theta, 1.57, abs_tol=1e-6)


def test_pose6d_fields(pose):
    pose = pose()
    assert pose.x == 0.0
    assert pose.y == 0.0
    assert pose.z == 0.0
    assert pose.roll == 0.0
    assert pose.pitch == 0.0
    assert pose.yaw == 0.0


def test_pose6d_bounds(pose):
    pose = pose()
    pose.x = 5.0
    pose.y = 10.0
    pose.z = 2.5
    pose.roll = 0.5
    pose.pitch = 0.3
    pose.yaw = 1.57
    assert pose.x == 5.0
    assert pose.y == 10.0
    assert pose.z == 2.5
    assert pytest.approx(pose.roll, abs=1e-6) == 0.5
    assert pytest.approx(pose.pitch, abs=1e-6) == 0.3
    assert pytest.approx(pose.yaw, abs=1e-6) == 1.57


def test_pose6d_bounds_validation(pose):
    pose_instance = pose(x=10)
    with pytest.raises(ValueError):
        pose_instance = pose(x=11)


def test_pose6d_to_conversion():
    pose = Pose6D(x=1, y=2, z=3, roll=np.pi / 4, pitch=np.pi / 3, yaw=np.pi / 2)

    # Test unit conversion
    pose_cm = pose.to(unit="cm")
    assert pose_cm.x == 100
    assert pose_cm.y == 200
    assert pose_cm.z == 300

    # Convert to degrees
    pose_deg = pose.to(angular_unit="deg")
    assert np.allclose(pose_deg.roll, 45.0)
    assert np.allclose(pose_deg.pitch, 60.0)
    assert np.allclose(pose_deg.yaw, 90.0)
    assert pose_deg.x == 1.0  # Linear units should remain unchanged
    assert pose_deg.y == 2.0
    assert pose_deg.z == 3.0

    # Test quaternion conversion
    quat = pose.to("quaternion", sequence="xyz")
    expected_quat = np.array([0.70105738, 0.09229596, 0.56098553, 0.43045933])
    assert np.allclose(quat, expected_quat, atol=1e-6)

    # Test rotation matrix conversion
    rot_matrix = pose.to("rotation_matrix")
    expected_matrix = np.array(
        [[0.35355339, -0.35355339, 0.8660254], [0.61237244, -0.61237244, -0.5], [0.70710678, 0.70710678, 0.0]]
    )
    assert np.allclose(rot_matrix, expected_matrix, atol=1e-6)


def test_planar_pose_to_conversion():
    pose = PlanarPose(x=1, y=2, theta=np.pi / 2)

    # Test unit conversion
    pose_cm = pose.to(unit="cm")
    assert pose_cm.x == 100
    assert pose_cm.y == 200

    # Test angular unit conversion
    pose_deg = pose.to(angular_unit="deg")
    assert isclose(pose_deg.theta, 90, abs_tol=1e-6)


def test_coordinate_conversion():
    coord = Pose6D(x=1.0, y=2.0, yaw=0.5)

    # Test linear unit conversion
    coord_cm = coord.to(unit="cm")
    assert coord_cm.x == 100.0
    assert coord_cm.y == 200.0
    assert isclose(coord_cm.z, 0.0, abs_tol=1e-6)

    # Test angular unit conversion
    coord_deg = coord.to(angular_unit="deg")
    assert isclose(coord_deg.roll, 0.0, abs_tol=1e-6)

    # # Test invalid unit conversion
    # with pytest.raises(ValueError, KeyError):
    #     coord_invalid = coord.to(unit="invalid")


def test_coordinate_array_initialization():
    coord = Pose6D(x=1.0, y=2.0, yaw=0.5)

    # Test array initialization
    coord_array = Pose6D([1.0, 2.0, 0.0, 0.0, 0.0, 0.5])
    assert coord == coord_array


def test_coordinate_relative():
    coord1 = Pose6D(x=1.0, y=2.0, yaw=0.5)
    coord2 = Pose6D(x=0.5, y=1.0, yaw=0.25)

    # Test relative pose calculation
    relative_coord = coord1.relative_to(coord2)
    assert relative_coord.x == 0.5
    assert relative_coord.y == 1.0
    assert isclose(relative_coord.yaw, 0.25, abs_tol=1e-6)


def test_coordinate_absolute():
    coord1 = Pose6D(x=1.0, y=2.0, yaw=0.5)
    coord2 = Pose6D(x=0.5, y=1.0, yaw=0.25)

    # Test absolute pose calculation
    absolute_coord = coord1.absolute_from(coord2)
    assert absolute_coord.x == 1.5
    assert absolute_coord.y == 3.0
    assert isclose(absolute_coord.yaw, 0.75, abs_tol=1e-6)


def test_relative_to_equals_rotation():
    coord1 = Pose6D(x=1.0, y=2.0, yaw=0.5)
    coord2 = Pose6D(x=0.5, y=1.0, yaw=0.25)

    # Test relative pose calculation
    relative_coord = coord1.relative_to(coord2)
    assert relative_coord == Pose6D(x=0.5, y=1.0, yaw=0.25)
    absolute_coord = relative_coord.absolute_from(coord2)
    assert coord1 == absolute_coord

    import embdata.utils.geometry_utils as geometry_utils
    rotation_from_pose = relative_coord.rotation_matrix()
    rotation = geometry_utils.rotation_between_two_poses(coord2, coord1)

    assert np.allclose(rotation_from_pose, rotation, atol=1e-6)


    
# def test_world_canonicalization():
#     url = "https://raw.githubusercontent.com/mbodiai/embodied-agents/main/resources/depth_image.png?raw=true"
#     from embdata.sense.depth import Depth
#     from embdata.sense.camera import Camera, Intrinsics, Extrinsics, Distortion
#     depth = Depth(url)
#     camera = Camera(intrinsic=Intrinsics(fx=911.0, fy=911.0, cx=653.0, cy=371.0), 
#                     distortion=Distortion(), 
#                     extrinsic=Extrinsics(), 
#                     depth_scale=0.001)
#     depth.save("depth.png")
#     pcd, canonical_frame = depth.segment_plane_o3d(
#         rgb_image_path="depth.png",
#         instrisic=camera.instrinsic,
#         threshold=0.01,
#         min_samples=3,
#         max_trials=1000,
#         canonicalize=True,
#     )
#     url = "https://raw.githubusercontent.com/mbodiai/embodied-agents/main/resources/depth_image.png?raw=true"
#     rgb_image = Image(url=url)
#     detection_results = object_detection_agent.act(image=rgb_image, objects=["Remote Control, Basket, Red Marker, Spoon, Fork"])
    
#     points_3d = []
#     for obj in detection_results.objects:
#         print(f"Detected Object: {obj.name} at {obj.pixel_coords}")

#         points_3d.append(camera.deproject(obj.pixel_coords, depth= depth.array[*obj.pixel_coords] * camera.depth_scale))

#     pose_camera_plane = -math.pi/4
#     r_camera_plane = 1

#     x,y,z = math.sqrt(2)/2, 0, -math.sqrt(2)/2

if __name__ == "__main__":
    test_relative_to_equals_rotation()