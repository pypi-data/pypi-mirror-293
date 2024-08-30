from lager import log
from pydantic import ConfigDict, Field, model_validator

from embdata.sample import Sample


def numeric(x):
    if isinstance(x, str):
        x = x.replace(",", "")
        if x.isnumeric():
            return int(x)
    return x
class Metadata(Sample):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    num_depth_cams: int = Field(0, alias="# Depth Cams")
    num_episodes: int = Field(0, alias="# Episodes")
    num_rgb_cams: int = Field(0, alias="# RGB Cams")
    num_wrist_cams: int = Field(0, alias="# Wrist Cams")
    action_space: str = Field("", alias="Action Space")
    control_frequency: int = Field("", alias="Control Frequency")
    data_collect_method: str = Field("", alias="Data Collect Method")
    dataset_name: str = Field("", alias="Dataset")
    description: str = Field("", alias="Description")
    file_size_gb: float = Field(0.0, alias="File Size (GB)")
    gripper: str | float = Field("", alias="Gripper")
    has_camera_calibration: str | float | bool = Field("", alias="Has Camera Calibration?")
    has_proprioception: str | bool = Field("", alias="Has Proprioception?")
    has_suboptimal: str | bool = Field("", alias="Has Suboptimal?")
    language_annotations: float | str = Field(0.0, alias="Language Annotations")
    registered_dataset_name: str = Field("", alias="Registered Dataset Name")
    robot: str = Field("", alias="Robot")
    robot_morphology: str = Field("", alias="Robot Morphology")
    scene_type: str = Field("", alias="Scene Type")
    misc: str | None = Field("", alias="Misc")

    @model_validator(mode="before")
    @classmethod
    def validate_metadata(cls, v) -> dict:
        for k, val in v.copy().items():
            # print(f"Checking {k}={val}")
            if isinstance(val, str) and ("num" in k or "file" in k.lower() or "#" in k or "frequency" in k.lower()):
                    try:
                        v[k] = numeric(val)
                    except Exception as e:
                        log.warning(f"Could not convert {k}={val} to int {e}")
                    finally:
                        v[k] = -1
                        v["misc"] = f"{v.get('misc', '')} {k}={val}"

        return v
