import numpy as np
import pytest
from embdata.utils.geometry_utils import pose_to_transformation_matrix, rotation_between_two_points
from embdata.coordinate import Pose, Pose6D, PlanarPose
from embdata.motion import Motion
from embdata.geometry import Transform2D, Transform3D
from embdata.sense.depth import Depth

def test_pose_to_transformation_matrix():
    # Test with Pose object
    pose = Pose6D(x=1, y=2, z=3, roll=0, pitch=0, yaw=0)
    result = pose_to_transformation_matrix([1, 2, 3, 0, 0, 0])
    expected = np.array([[1, 0, 0, 1], [0, 1, 0, 2], [0, 0, 1, 3], [0, 0, 0, 1]])
    np.testing.assert_array_almost_equal(result, expected)

    # Test with numpy array
    pose_array = np.array([1, 2, 3, 0, 0, 0])
    result = pose_to_transformation_matrix(pose_array)
    np.testing.assert_array_almost_equal(result, expected)


def test_transfrom2D():
    # Test with Pose object
    pose = np.array([1, 2, 0])
    result = Transform2D.from_pose(pose)
    expected = Transform2D(rotation=np.array([[1, 0], [0, 1]]), translation=np.array([1, 2]))
    assert np.allclose(result.rotation, expected.rotation)


def test_tranform3d():
    # Test with Pose object
    pose = np.array([1, 2, 3, np.pi/2, np.pi/2, np.pi/2])
    result = Transform3D.from_pose(pose)
    expected = Transform3D(rotation=np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]]), translation=np.array([1, 2, 3]))
    print(f"Result: {result}")
    assert np.allclose(result.rotation, expected.rotation)


# def test_canonicalize_world():
#     url = "https://raw.githubusercontent.com/mbodiai/embodied-agents/main/resources/depth_image.png?raw=true"
#     plane_coeffs =  Depth(url).segment()

if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
