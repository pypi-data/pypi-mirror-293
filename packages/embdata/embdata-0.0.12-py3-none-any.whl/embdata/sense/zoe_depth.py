import torch
import numpy as np
from PIL import Image as PILImage
from io import BytesIO
from transformers import AutoImageProcessor, ZoeDepthForDepthEstimation

from typing import Union

from mbodied.types.sense.vision import Image
from mbodied.agents.sense.sensory_agent import SensoryAgent


class ZoeDepthAgent(SensoryAgent):
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.image_processor = AutoImageProcessor.from_pretrained(
            "Intel/zoedepth-nyu-kitti"
        )
        self.model = ZoeDepthForDepthEstimation.from_pretrained(
            "Intel/zoedepth-nyu-kitti"
        ).to(self.device)
        self.init_call()

    def init_call(self):
        # Speed up by running a dummy prediction
        self.act(Image("embodied-agents/resources/bridge_example.jpeg"))

    def act(self, image: Image) -> np.ndarray:
        inputs = self.image_processor(images=image.pil, return_tensors="pt").to(
            self.device
        )

        with torch.no_grad():
            outputs = self.model(**inputs)
            predicted_depth = outputs.predicted_depth

        # interpolate to original size
        prediction = torch.nn.functional.interpolate(
            predicted_depth.unsqueeze(1),
            size=image.size[::-1],
            mode="bicubic",
            align_corners=False,
        )

        # visualize the prediction
        output = prediction.squeeze().cpu().numpy()
        # formatted = (output * 255 / np.max(output)).astype("uint8")
        # depth = Image.fromarray(formatted)
        return output


if __name__ == "__main__":
    agent = ZoeDepthAgent()
    import time

    start_time = time.time()
    depth_image1 = agent.act(image=Image("resources/example.jpg"))
    print("Time taken:", time.time() - start_time)