
from typing import TYPE_CHECKING, List, Union

import numpy as np
import requires
from lager import log
from pydantic import Field, computed_field

from embdata.sample import Sample
from embdata.sense.image import Image

if TYPE_CHECKING:
  import contextlib
  with contextlib.suppress(ImportError):
    import cv2

class Video(Sample):
    frames: List[Image] = Field(default_factory=list)
    fps: float | None = None
    duration: float | None = None
    path: str | None = None

    @computed_field
    @classmethod
    def num_frames(cls) -> int:
        return len(cls.frames)

    @computed_field
    @classmethod
    def shape(cls) -> tuple[int, int, int]:
        if not cls.frames:
            return (0, 0, 0)
        return cls.frames[0].shape

    @requires("cv2")
    def save(self, path: str, encoding: Union["cv2.VideoCaptureAPIs", None] = None) -> None:
        """Save the video as an mp4 file. Optionally specify the path."""
        import cv2
        encoding = encoding or cv2.CAP_FFMPEG
        height, width, _ = self.frames[0].array.shape
        self.path = path or self.path

        # Debugging information
        print(f"Saving video to {self.path}")
        print(f"Video dimensions: {width}x{height}")
        print(f"FPS: {self.fps}")

        # Ensure the FourCC code is correct
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        video = cv2.VideoWriter(self.path, fourcc, self.fps, (width, height))

        if not video.isOpened():
            raise ValueError("Error: Could not open video writer.")

        for i, frame in enumerate(self.frames):
            frame_array = np.array(frame.pil)
            if frame_array.shape[2] == 4:  # Check if the frame has an alpha channel
                frame_array = frame_array[:, :, :3]  # Remove alpha channel
            if frame_array.shape[2] == 3:  # Ensure frame is in BGR format
                frame_array = cv2.cvtColor(frame_array, cv2.COLOR_RGB2BGR)
            else:
                msg = f"Unexpected frame shape: {frame_array.shape}"
                raise ValueError(msg)
            
            print(f"Writing frame {i+1}/{len(self.frames)}")
            video.write(frame_array)

        video.release()
        print("Video saved successfully.")

    @requires("cv2")
    @classmethod
    def capture(cls, url: str, encoding: "cv2.VideoCaptureAPIs" = "cv2.CAP_GSTREAMER", batch_size: int = 1) -> None:
        """Capture video frames from a GStreamer pipeline with an adjustable batch size.

        Args:
            url (str): The GStreamer pipeline URL or description.
            encoding (str): The backend to use for capturing. Defaults to GStreamer.
            batch_size (int): Number of frames to capture at a time. Defaults to 1.

        Example:
            To capture video from a GStreamer pipeline, you can use the following command:

            ```python
            video = Video()
            gstreamer_pipeline = (
                "rtspsrc location=rtsp://your_camera_ip ! "
                "rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink"
            )
            video.capture(gstreamer_pipeline, batch_size=10)
            print(f"Captured {len(video.frames)} frames.")
            ```
        """
        import cv2
        try:
            cap = cv2.VideoCapture(url, encoding)

            if not cap.isOpened():
                msg = "Error: Could not open video stream with GStreamer."
                raise ValueError(msg)

            while True:
                batch = []
                for _ in range(batch_size):
                    ret, frame = cap.read()
                    if not ret:
                        break
                    batch.append(frame)

                if not batch:
                    break

                # Assuming Image has an appropriate constructor
                [Image(array=frame) for frame in batch]
                yield cls(frames=batch)
        except KeyboardInterrupt:
            log.info("Video capture interrupted by user.")
        finally:
            cap.release()

    def __init__(self, frames: List[Image], fps: float=5, duration: float=None, path: str=None):
        return super().__init__(frames=frames, fps=fps, duration=duration, path=path)