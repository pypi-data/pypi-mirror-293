from importlib.resources import files
from pathlib import Path
import numpy as np
from PIL import Image
from embdata.coordinate import Pose
from embdata.sense.depth import Depth, Plane
from embdata.sense.camera import Camera
from embdata.sense.image import Image as MBImage
from embdata.utils.geometry_utils import rotation_between_two_points as align_plane_normal_to_axis


camera = Camera()

import pytest
@pytest.fixture
def image_path():
    path = files("embdata") / "resources"
    return path / "color_image.png"
@pytest.fixture
def depth_path():
    path: Path = files("embdata") / "resources"
    return path / "depth_image.png"

camera = Camera()

def test_depth_initialization():
    depth = Depth(mode="I", points=None, array=None, camera_params=camera)
    assert depth.mode == "I"
    assert depth.points is None
    assert depth.array is None


def test_depth_from_pil():
    pil_image = Image.new("RGB", (100, 100))
    depth = Depth.from_pil(pil_image, mode="I", camera_params=camera)
    assert depth.mode == "I"
    assert depth.points is None
    assert depth.array is not None
    assert isinstance(depth.array, np.ndarray)
    assert depth.array.dtype == np.uint16


def test_depth_cluster_points():
    depth = Depth(camera_params=camera)
    depth.points = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    labels = depth.cluster_points(n_clusters=2)
    assert len(labels) == 3
    assert set(labels) == {0, 1}


# def test_depth_segment_plane():
#     depth = Depth(camera_params=camera)
#     depth.points = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
#     plane: Plane = depth.segment_plane()
#     assert plane.plane_model.shape == (4,)


def test_depth_show(depth_path):
    depth = Depth(path=depth_path, size=(100, 100), camera_params=camera)
    # depth.array = np.zeros((100, 100, 3), dtype=np.uint8)
    # print("depth.array:", depth.array)
    depth.show()  # Just checking if the function runs without errors


def test_depth_segment_cylinder():
    depth = Depth(camera_params=camera)
    depth.points = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    inlier_points, inlier_indices = depth.segment_cylinder()

    # Ensure that inlier_points and inlier_indices have the correct shapes
    assert len(inlier_points.shape) == 2
    assert inlier_points.shape[1] == 3  # Each point should have 3 coordinates

    assert len(inlier_indices.shape) == 1
    assert inlier_indices.shape[0] == inlier_points.shape[0]  # Number of inliers should matchtests\test_depth.py


def test_rgb(depth_path, image_path):
    depth = Depth(path=depth_path,
                  mode="I", 
                  encoding="png", 
                  size=(1280, 720),
                  camera_params=camera, 
                  rgb=MBImage(path=image_path, mode="RGB", encoding="png"))
    
    print("depth.rgb:", depth.rgb.mode)
    assert depth.rgb is not None
    assert depth.rgb.path is not None
    assert depth.rgb.mode == "RGB"
    assert depth.rgb.encoding == "png"
    
def test_load_from_path(depth_path):

    depth = Depth(path=depth_path, mode="I", encoding="png", camera_params=camera)
    assert depth.mode == "I"
    assert depth.points is None
    assert depth.array is not None
    assert isinstance(depth.array, np.ndarray)



def main():
    # Test pose subtraction vs rotation matrix
    pose = Pose(x=1, y=2, z=3, roll=0.1, pitch=0.2, yaw=0.3)
    pose2 = Pose(x=2, y=3, z=4, roll=0.2, pitch=0.3, yaw=0.4)
    relative_pose = pose2.relative_to(pose)

    # Extract position vectors from poses
    pose_position = np.array([pose.x, pose.y, pose.z])
    pose2_position = np.array([pose2.x, pose2.y, pose2.z])

    rotation = align_plane_normal_to_axis(pose_position, pose2_position)

    print("Relative pose rotation matrix:")
    print(relative_pose.rotation_matrix())
    print("\nComputed rotation matrix:")
    print(rotation)

    if np.allclose(relative_pose.rotation_matrix(), rotation, atol=1e-6):
        print("\nTest passed: Rotation matrices are close")
    else:
        print("\nTest failed: Rotation matrices are not close")

def test_rotation_between_two_vectors():
    from embdata.utils.geometry_utils import rotation_between_two_points, rotation_between_two_poses, rotation_from_z

    def is_rotation_matrix(R):
        # Check if matrix is orthogonal and has determinant 1
        orthogonal = np.allclose(np.dot(R.T, R), np.eye(3), atol=1e-6)
        det = np.allclose(np.linalg.det(R), 1, atol=1e-6)
        return orthogonal and det

    def check_rotation(R, v1, v2):
        v1_normalized = v1 / np.linalg.norm(v1)
        v2_normalized = v2 / np.linalg.norm(v2)
        return np.allclose(np.dot(R, v1_normalized), v2_normalized, atol=1e-6)

    # Test with arbitrary vectors
    v1 = np.random.rand(3)
    v2 = np.random.rand(3)
    
    print("Input vectors:")
    print("v1:", v1)
    print("v2:", v2)

    result1 = rotation_between_two_points(v1, v2)
    result2 = rotation_from_z(v1 - v2)

    print("\nrotation_between_two_points result:")
    print(result1)
    print("Is valid rotation matrix:", is_rotation_matrix(result1))
    print("Determinant:", np.linalg.det(result1))
    print("Orthogonality check:", np.allclose(np.dot(result1.T, result1), np.eye(3), atol=1e-6))

    print("\nget_rotation_matrix_from_two_points result:")
    print(result2)
    print("Is valid rotation matrix:", is_rotation_matrix(result2))
    print("Determinant:", np.linalg.det(result2))
    print("Orthogonality check:", np.allclose(np.dot(result2.T, result2), np.eye(3), atol=1e-6))

    if not is_rotation_matrix(result1):
        print("\nWarning: rotation_between_two_points did not produce a valid rotation matrix")
    if not is_rotation_matrix(result2):
        print("\nWarning: get_rotation_matrix_from_two_points did not produce a valid rotation matrix")

    print("\nChecking if rotations correctly transform v1 to v2:")
    print("rotation_between_two_points:", check_rotation(result1, v1, v2))
    print("get_rotation_matrix_from_two_points:", check_rotation(result2, v1, v2))

    if np.allclose(result1, result2, atol=1e-6):
        print("\nBoth implementations produce the same result.")
    else:
        print("\nWarning: Results are not close. Consider reviewing both implementations for consistency.")

    print("Test completed")



def quaternion_between_vectors(v1, v2):
    """Compute the quaternion that rotates v1 to v2."""
    v1 = v1 / np.linalg.norm(v1)
    v2 = v2 / np.linalg.norm(v2)
    cross = np.cross(v1, v2)
    dot = np.dot(v1, v2)
    if np.linalg.norm(cross) < 1e-8:  # Vectors are already aligned
        return np.array([1, 0, 0, 0])  # Identity quaternion
    q = np.concatenate(([1 + dot], cross))
    return q / np.linalg.norm(q)

def align_pose(pose_from, pose_to):
    """Align the full 6D pose (translation + rotation).

    Args:
        pose_from: The initial pose as a 6D vector [x, y, z, roll, pitch, yaw].
        pose_to: The target pose as a 6D vector [x, y, z, roll, pitch, yaw].

    Returns:
        Aligned translation and rotation.
    """
    # Align translation (x, y, z)
    translation_from = pose_from[:3]
    translation_to = pose_to[:3]

    # Align rotation using quaternions
    rotation_from = R.from_euler('xyz', pose_from[3:]) # type: ignore
    rotation_to = R.from_euler('xyz', pose_to[3:]) # type: ignore

    # Compute the relative rotation
    relative_rotation = rotation_to * rotation_from.inv()

    # Apply the rotation
    aligned_translation = translation_to  # Assuming you want to move pose_from to pose_to's position
    aligned_rotation = relative_rotation.as_matrix()

    return aligned_translation, aligned_rotation

if __name__ == "__main__":
    test_rotation_between_two_vectors()
    main()
