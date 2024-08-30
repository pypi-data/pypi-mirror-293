import pytest
import numpy as np
from embdata.coordinate import Coordinate, Pose, Pose6D
from embdata.geometry import rpy_to_rotation_matrix, rotation_matrix_to_rpy, Transform3D
from math import isclose
from embdata.coordinate import Coordinate, Pose6D, CoordinateField, PlanarPose

def test_rotation_matrix():
    pose = Pose(x=0, y=0, z=0, roll=0, pitch=0, yaw=np.pi / 2)

    xyz_matrix = pose.rotation_matrix(sequence="xyz")
    zyx_matrix = pose.rotation_matrix(sequence="zyx")

    assert np.allclose(xyz_matrix, np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]]))
    assert np.allclose(zyx_matrix, np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]]))


def test_rpy_to_rotation_matrix():
    pose = Pose(x=0, y=0, z=0, roll=0, pitch=0, yaw=np.pi / 2)

    rpy = np.array([0, 0, np.pi / 2])

    zyx_matrix = rpy_to_rotation_matrix(rpy, sequence="zyx")
    xyz_matrix = rpy_to_rotation_matrix(rpy, sequence="xyz")

    assert np.allclose(zyx_matrix, np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]]))
    assert np.allclose(zyx_matrix, xyz_matrix)


def test_rotation_matrix_to_rpy():
    # Test case 1: Standard orientations
    rpy_init = np.array([0, 0, np.pi / 2])
    rpy2_init = np.array([np.pi / 4, np.pi / 6, -np.pi / 4])

    zyx_matrix = rpy_to_rotation_matrix(rpy_init, sequence="zyx")
    zyx_matrix2 = rpy_to_rotation_matrix(rpy2_init, sequence="zyx")

    rpy = rotation_matrix_to_rpy(zyx_matrix, sequence="zyx")
    rpy2 = rotation_matrix_to_rpy(zyx_matrix2, sequence="zyx")

    if rpy_init[1] == 0:
        rpy[1] = abs(rpy[1])
    if rpy2_init[1] == 0:
        rpy2[1] = abs(rpy2[1])

    assert np.allclose(rpy, rpy_init)
    assert np.allclose(rpy2, rpy2_init)

    # Edge case 1: Rotation of 0 degrees (identity matrix)
    identity_matrix = np.eye(3)
    rpy_identity = rotation_matrix_to_rpy(identity_matrix, sequence="zyx")
    assert np.allclose(rpy_identity, np.array([0.0, 0.0, 0.0]))

    # Edge case 2: Gimbal lock (pitch = ±π/2)
    gimbal_lock_matrix_positive = rpy_to_rotation_matrix(np.array([0, np.pi / 2, 0]), sequence="zyx")
    gimbal_lock_matrix_negative = rpy_to_rotation_matrix(np.array([0, -np.pi / 2, 0]), sequence="zyx")

    rpy_gimbal_lock_positive = rotation_matrix_to_rpy(gimbal_lock_matrix_positive, sequence="zyx")
    rpy_gimbal_lock_negative = rotation_matrix_to_rpy(gimbal_lock_matrix_negative, sequence="zyx")

    assert np.allclose(rpy_gimbal_lock_positive, np.array([0.0, np.pi / 2, 0.0]))
    assert np.allclose(rpy_gimbal_lock_negative, np.array([0.0, -np.pi / 2, 0.0]))

    # Edge case 3: Rotation matrix with very small angles (testing numerical stability)
    small_angle = 1e-10
    small_angle_matrix = rpy_to_rotation_matrix(np.array([small_angle, small_angle, small_angle]), sequence="zyx")
    rpy_small_angle = rotation_matrix_to_rpy(small_angle_matrix, sequence="zyx")
    assert np.allclose(rpy_small_angle, np.array([small_angle, small_angle, small_angle]))

    # Edge case 4: Negative angles
    negative_rpy_init = np.array([-np.pi / 4, -np.pi / 6, np.pi / 4])
    negative_zyx_matrix = rpy_to_rotation_matrix(negative_rpy_init, sequence="zyx")
    rpy_negative = rotation_matrix_to_rpy(negative_zyx_matrix, sequence="zyx")
    assert np.allclose(rpy_negative, negative_rpy_init)

    # Edge case 5: Matrix with non-standard rotation sequence
    non_standard_matrix = rpy_to_rotation_matrix(np.array([np.pi / 3, np.pi / 4, -np.pi / 6]), sequence="zyx")
    rpy_non_standard = rotation_matrix_to_rpy(non_standard_matrix, sequence="zyx")
    assert np.allclose(rpy_non_standard, np.array([np.pi / 3, np.pi / 4, -np.pi / 6]))


def test_transform_3d_matmul():
    # Define a transformation with a rotation and translation
    translation = np.array([1, 2, 3])
    rotation = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
    transform = Transform3D(translation=translation, rotation=rotation)

    # Define a single point to transform
    point = np.array([1, 0, 0])

    # Apply the transformation using the @ operator (__matmul__) for a single point
    transformed_point = transform @ point

    # Expected result for the single point:
    # The rotation matrix rotates the point [1, 0, 0] 90 degrees counterclockwise around the z-axis,
    # resulting in [0, 1, 0]. After translation, the result should be [1, 3, 3].
    expected_point = np.array([1, 3, 3])

    # Assert that the transformed point is as expected
    assert np.allclose(transformed_point, expected_point), f"Expected {expected_point}, but got {transformed_point}"

    # Define a list of points to transform
    points = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

    # Apply the transformation to the list of points
    transformed_points = transform.transform(points)

    # Expected results for the list of points:
    # - Point [1, 0, 0] -> [1, 3, 3]
    # - Point [0, 1, 0] -> [0, 2, 3]
    # - Point [0, 0, 1] -> [1, 2, 4]
    expected_points = np.array([[1, 3, 3], [0, 2, 3], [1, 2, 4]])

    # Assert that the transformed points are as expected
    assert np.allclose(transformed_points, expected_points), f"Expected {expected_points}, but got {transformed_points}"


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


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
