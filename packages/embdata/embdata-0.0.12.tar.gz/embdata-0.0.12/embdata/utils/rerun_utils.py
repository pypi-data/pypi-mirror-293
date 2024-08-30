from typing import TYPE_CHECKING, Tuple

import cv2
import numpy as np
import requires
from embdata.motion.control import Pose
from embdata.sense.camera import Camera
from embdata.utils.import_utils import smart_import

if TYPE_CHECKING:
    from embdata.ndarray import NumpyArray
    import rerun as rr
    import rerun.blueprint as rrb


def get_blueprint() -> "rrb.Blueprint":
    rrb = smart_import("rerun.blueprint", mode="lazy")
    return rrb.Blueprint(
        rrb.Vertical(
            rrb.Horizontal(
                rrb.Spatial2DView(
                    name="Scene",
                    background=[0.0, 0.0, 0.0, 0.0],
                    origin="scene",
                    visible=True,
                ),
                rrb.Spatial2DView(
                    name="Augmented",
                    background=[0.0, 0.0, 0.0, 0.0],
                    origin="augmented",
                    visible=True,
                ),
            ),
            rrb.Horizontal(
                rrb.TimeSeriesView(
                    name="Actions",
                    origin="action",
                    visible=True,
                    axis_y=rrb.ScalarAxis(range=(-0.5, 0.5), zoom_lock=True),
                    plot_legend=rrb.PlotLegend(visible=True),
                    time_ranges=[
                        rrb.VisibleTimeRange(
                            "timeline0",
                            start=rrb.TimeRangeBoundary.cursor_relative(seq=-100),
                            end=rrb.TimeRangeBoundary.cursor_relative(),
                        ),
                    ],
                ),
            ),
            row_shares=[2, 1],
        ),
        rrb.BlueprintPanel(state="collapsed"),
        rrb.TimePanel(state="collapsed"),
        rrb.SelectionPanel(state="collapsed"),
    )

@requires("rerun")
def log_scalar(name: str, value: float) -> None:
    rr = smart_import("rerun", mode="lazy")
    rr.log(name, rr.Scalar(value))


def project_points_to_2d(camera_params: Camera, start_pose: Pose, end_pose: Pose) -> Tuple[np.ndarray, np.ndarray]:
    intrinsic = camera_params.intrinsic.matrix
    distortion = camera_params.distortion.numpy().reshape(5, 1)

    translation = np.array(camera_params.extrinsic.translation_vector).reshape(3, 1)
    rotation = cv2.Rodrigues(np.array(camera_params.extrinsic.rotation_vector).reshape(3, 1))[0]
    end_effector_offset = 0.175

    # Switch x and z coordinates for the 3D points
    start_position_3d: NumpyArray[3, 1] = np.array([start_pose.z - end_effector_offset, -start_pose.y, start_pose.x]).reshape(3, 1)
    end_position_3d: NumpyArray[3, 1] = np.array([end_pose.z - end_effector_offset, -end_pose.y, end_pose.x]).reshape(3, 1)

    # Transform the 3D point to the camera frame
    start_position_3d_camera_frame: NumpyArray[3, 1] = np.dot(rotation, start_position_3d) + translation
    end_position_3d_camera_frame: NumpyArray[3, 1] = np.dot(rotation, end_position_3d) + translation

    # Project the transformed 3D point to 2D
    start_point_2d, _ = cv2.projectPoints(
        objectPoints=start_position_3d_camera_frame,
        rvec=np.zeros((3, 1)),
        tvec=np.zeros((3, 1)),
        cameraMatrix=intrinsic,
        distCoeffs=distortion,
    )

    end_point_2d, _ = cv2.projectPoints(
        objectPoints=end_position_3d_camera_frame,
        rvec=np.zeros((3, 1)),
        tvec=np.zeros((3, 1)),
        cameraMatrix=intrinsic,
        distCoeffs=distortion,
    )

    return start_point_2d[0][0], end_point_2d[0][0]
