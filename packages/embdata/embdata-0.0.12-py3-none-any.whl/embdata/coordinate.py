# Copyright (c) 2024 Mbodi AI
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
"""NamedTuple-Like class for representing geometric data in cartesian and polar coordinates.

A 3D pose represents the planar x, y, and theta, while a 6D pose represents the volumetric x, y, z, roll, pitch, and yaw.

Example:
    >>> import math
    >>> pose_3d = Pose3D(x=1, y=2, theta=math.pi / 2)
    >>> pose_3d.to("cm")
    Pose3D(x=100.0, y=200.0, theta=1.5707963267948966)
    >>> pose_3d.to("deg")
    Pose3D(x=1.0, y=2.0, theta=90.0)
    >>> class BoundedPose6D(Pose6D):
    ...     x: float = CoordinateField(bounds=(0, 5))
    >>> pose_6d = BoundedPose6D(x=10, y=2, z=3, roll=0, pitch=0, yaw=0)
    Traceback (most recent call last):
    ...
    ValueError: x value 10 is not within bounds (0, 5)
"""

from functools import wraps
from typing import TYPE_CHECKING, Any, Dict, List, Self, TypeAlias, TypeVar, Union, cast, overload

import numpy as np
import requires
from lager import log
from numpy.typing import ArrayLike, NDArray
from pydantic import ConfigDict, Field, PrivateAttr, computed_field, create_model, model_validator
from pydantic_core import PydanticUndefined
from scipy.spatial.transform import Rotation
from typing_extensions import Literal

from embdata.ndarray import NumpyArray
from embdata.sample import Sample
from embdata.units import AngularLabel, AngularUnit, LinearLabel, LinearUnit, TemporalUnit
if TYPE_CHECKING:
    from pydantic.fields import FieldInfo


InfoUndefinedType = Literal["unset"]
InfoUndefined = "unset"

EuelerSequence = Literal["zyx", "xyz"]
"""The order in which the rotation matrices are multiplied. ZYX means intrinsic rotations about X first, then Y,
 then Z aka roll, pitch, yaw.
"""


def CoordinateField(  # noqa
    default=0.0,
    default_factory=None,
    reference_frame: str | InfoUndefinedType = InfoUndefined,
    origin: np.ndarray | List[float] | InfoUndefinedType = InfoUndefined,
    unit: LinearUnit | AngularUnit | TemporalUnit = "m",
    bounds: tuple | InfoUndefinedType = InfoUndefined,
    description: str | None = None,
    visibility: Literal["public", "private"] = "public",
    **kwargs,
):
    """Create a Pydantic Field with extra metadata for coordinates.

    This function extends Pydantic's Field with additional metadata specific to coordinate systems,
    including reference frame, unit, and bounds information.

    Args:
        default: Default value for the field.
        default_factory: Factory for creating the default value.
        reference_frame: Reference frame for the coordinates.
        origin: Origin of the coordinate system.
        unit: Unit of the coordinate (LinearUnit, AngularUnit, or TemporalUnit).
        bounds: Tuple representing the allowed range for the coordinate value.
        description: Description of the field.
        **kwargs: Additional keyword arguments for field configuration.

    Returns:
        Field: Pydantic Field with extra metadata.

    Examples:
        >>> from pydantic import BaseModel
        >>> class Robot(BaseModel):
        ...     x: float = CoordinateField(unit="m", bounds=(0, 10))
        ...     angle: float = CoordinateField(unit="rad", bounds=(0, 6.28))
        >>> robot = Robot(x=5, angle=3.14)
        >>> robot.dict()
        {'x': 5.0, 'angle': 3.14}
        >>> Robot(x=15, angle=3.14)
        Traceback (most recent call last):
        ...
        ValueError: x value 15.0 is not within bounds (0, 10)
    """
    json_schema_extra = {
        "_info": {
            "reference_frame": reference_frame,
            "unit": unit,
            "bounds": bounds,
            "origin": origin,
            **kwargs,
        },
    }

    return (
        Field(
            default=default if default_factory is None else PydanticUndefined,
            json_schema_extra=json_schema_extra,
            description=description,
            default_factory=default_factory,
        )
        if visibility == "public"
        else PrivateAttr(
            default_factory=lambda: json_schema_extra["_info"],
        )
    )


CoordField = CoordinateField
"""Alias for CoordinateField."""
wraps(CoordField, CoordinateField)
CoordField.__doc__ = "Alias for CoordinateField." + CoordinateField.__doc__
CoordsField = CoordinateField
wraps(CoordsField, CoordinateField)
CoordsField.__doc__ = "Alias for CoordinateField." + CoordinateField.__doc__

T = TypeVar("T", bound="Coordinate")

class Coordinate(Sample):
    """A list of numbers representing a coordinate in the world frame for an arbitrary space."""

    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True, populate_by_name=True)
    _info: Dict[str, Any] = CoordinateField(visibility="private")

    def info(self) -> dict:
        """Get the metadata of the coordinate."""
        return self._info

    def model_info(self) -> dict:
        _info = super().model_info()
        _info.update({"self": self._info})
        return _info

    def set_info(self, key: str, value: Any) -> None:
        """Set the metadata of the coordinate."""
        self._info[key] = value

    def magnitude(self) -> float:
        """Compute the magnitude of the coordinate."""
        return np.linalg.norm(self.numpy())

    def direction(self) -> np.ndarray:
        """Compute the direction of the coordinate."""
        return self.numpy() / self.magnitude

    def angle(self) -> float:
        """Compute the angle of the first two dimensions of the coordinate."""
        return np.arctan2(*self[:2]) if len(self) >= 2 else 0.0  # noqa

    def reference_frame(self) -> str:
        """Get the reference frame of the coordinate."""
        return self._info.get("reference_frame", InfoUndefined)

    def set_reference_frame(self, reference_frame: str) -> None:
        """Set the reference frame of the coordinate."""
        self.set_info("reference_frame", reference_frame)

    def origin(self) -> np.ndarray:
        """Get the origin of the coordinate."""
        return self._info.get("origin", np.zeros_like(self.numpy()))

    @staticmethod
    def convert_linear_unit(value: float, from_unit: str, to_unit: str) -> float:
        """Convert a value from one linear unit to another.

        This method supports conversion between meters (m), centimeters (cm),
        millimeters (mm), inches (in), and feet (ft).

        Args:
            value (float): The value to convert.
            from_unit (str): The unit to convert from.
            to_unit (str): The unit to convert to.

        Returns:
            float: The converted value.

        Examples:
            >>> Coordinate.convert_linear_unit(1.0, "m", "cm")
            100.0
            >>> Coordinate.convert_linear_unit(100.0, "cm", "m")
            1.0
            >>> Coordinate.convert_linear_unit(1.0, "m", "ft")
            3.280839895013123
            >>> Coordinate.convert_linear_unit(12.0, "in", "cm")
            30.48
        """
        conversion_from_factors = {
            "m": 1.0,
            "cm": 0.01,
            "mm": 0.001,
            "in": 0.0254,
            "ft": 0.3048,
        }
        conversion_to_factors = {
            "m": 1.0,
            "cm": 100.0,
            "mm": 1000.0,
            "in": 1.0 / 0.0254,
            "ft": 1.0 / 0.3048,
        }
        from_unit_factor = conversion_from_factors[from_unit]
        to_unit_factor = conversion_to_factors[to_unit]
        if from_unit == to_unit:
            return value
        return value * from_unit_factor * to_unit_factor

    @staticmethod
    def convert_angular_unit(value: float, to: AngularUnit | str) -> float:
        """Convert radians to degrees or vice versa.

        Args:
            value (float): The angular value to convert.
            to (AngularUnit): The target angular unit ("deg" or "rad").

        Returns:
            float: The converted angular value.
        """
        return np.degrees(value) if to == "deg" else np.radians(value)

    def relative_to(self, other: np.ndarray | List) -> Self:
        """Compute the coordinate relative to another coordinate."""
        other_coords = np.array(other)
        transformed: Self = self.__class__(self.numpy() - other_coords)
        transformed.set_info("origin", other_coords)
        other_reference_frame = other.reference_frame() if hasattr(other, "reference_frame") else str(other_coords)
        transformed.set_info("reference_frame", self.reference_frame() + "-" + other_reference_frame)
        return transformed

    def absolute(self) -> "Coordinate":
        """Compute the absolute coordinate from the origin."""
        return self.__class__(self.numpy() + self.info().get("origin", np.zeros_like(self.numpy())))

    def absolute_from(self, origin: Any | List | np.ndarray) -> "Coordinate":
        """Compute the absolute coordinate from another coordinate."""
        origin_coords = np.array(list(origin))
        transformed = self.__class__(self.numpy() + origin_coords)
        transformed.set_info("origin", origin_coords)
        origin_reference_frame = origin.info().get("reference_frame") if hasattr(origin, "info") else str(origin_coords)
        transformed.set_info("reference_frame", self.reference_frame() + "+" + origin_reference_frame)
        return transformed

    def __eq__(self, other: object) -> bool:
        """Check if two coordinates are equal."""
        if isinstance(other, Coordinate):
            other_array = other.numpy().astype(float)
            other_reference_frame = other.reference_frame()
        elif isinstance(other, list | tuple | np.ndarray):
            other_array = np.array(other, dtype=float)
            other_reference_frame = str(other_array)
        else:
            return NotImplemented

        return (
            np.allclose(self.numpy().astype(float), other_array) and self.reference_frame() == other_reference_frame
        )

    def __add__(self, other: "Coordinate") -> "Coordinate":
        """Add two motions together."""
        return self.absolute_from(other)

    def __sub__(self, other: Union["Coordinate", None, ArrayLike] = None) -> "Coordinate":
        """Subtract two motions."""
        if other is None:
            return self.__class__(-self.numpy())
        return self.relative_to(other)

    def __array__(self):
        """Return a numpy array representation of the pose."""
        return np.array(list(self.values()))

    def numpy(self) -> np.ndarray:
        return super().numpy().astype(float)

    def __slice__(self, start: int = 0, stop: int = -1, step: int = 1) -> ArrayLike:
        return self.numpy()[start:stop:step]

    def __getitem__(self, item: int | str) -> float:
        if isinstance(item, str):
            return getattr(self, item)
        return self.numpy()[item]

    def __neg__(self) -> "Coordinate":
        """Negate the coordinate."""
        return self.__class__(-self.numpy())

    @requires("torch") # type: ignore  # noqa: PGH003
    def __tensor__(self) -> "torch.Tensor":
        """Return a torch tensor representation of the pose."""
        import torch

        return torch.tensor(self.values())

    def __iter__(self):
        """Iterate over the coordinate values."""
        yield from self.__dict__.values()

    @model_validator(mode="after")
    def ensure_shape_and_bounds(self) -> Any:  # noqa
        """Validate the bounds of the coordinate."""
        for key, value in super().__iter__():
            if key.startswith("_"):
                continue
            bounds = self.field_info(key).get("bounds")
            shape = self.field_info(key).get("shape")
            if bounds and bounds is not InfoUndefined:
                if len(bounds) != 2 or not all(isinstance(b, int | float) for b in bounds):
                    msg = f"{key} bounds must consist of two numbers"
                    raise ValueError(msg)

                if shape and shape is not InfoUndefined:
                    shape = [shape] if isinstance(shape, int) else shape
                    shape_processed = []
                    value_processed = value
                    while len(shape_processed) < len(shape):
                        shape_processed.append(len(value_processed))
                        if shape_processed[-1] != len(value_processed):
                            msg = f"{key} value {value} of length {len(value_processed)} at dimension {len(shape_processed)-1} does not have the correct shape {shape}"
                            raise ValueError(msg)
                        value_processed = value_processed[0]

                    if hasattr(value, "shape") or isinstance(value, list | tuple):
                        for i, v in enumerate(value):
                            if not bounds[0] <= v <= bounds[1]:
                                msg = f"{key} item {i} ({v}) is out of bounds {bounds}"
                                raise ValueError(msg)
                elif not bounds[0] <= value <= bounds[1]:
                    msg = f"{key} value {value} is not within bounds {bounds}"
                    raise ValueError(msg)
        return self

    def to(self, container_or_unit: Any | str | None = None, unit=None, angular_unit=None, **kwargs) -> Any:
        """Convert the coordinate to a different unit or container.

        To see the available units, see the embdata.units module.

        Args:
            container_or_unit (Any, optional): The target container type or unit.
            unit (str, optional): The target linear unit. Defaults to "m".
            angular_unit (str, optional): The target angular unit. Defaults to "rad".
            **kwargs: Additional keyword arguments for field configuration.

        Returns:
            Any: The converted pose, either as a new Pose3D object with different units
                 or as a different container type.

        Examples:
            >>> import math
            >>> pose = Pose3D(x=1, y=2, theta=math.pi / 2)
            >>> pose.to("cm")
            Pose3D(x=100.0, y=200.0, theta=1.5707963267948966)
            >>> pose.to("deg")
            Pose3D(x=1.0, y=2.0, theta=90.0)
            >>> pose.to("list")
            [1.0, 2.0, 1.5707963267948966]
            >>> pose.to("dict")
            {'x': 1.0, 'y': 2.0, 'theta': 1.5707963267948966}
        """
        if container_or_unit is not None and container_or_unit not in str(LinearUnit) + str(AngularUnit):
            return super().to(container_or_unit)

        if container_or_unit and container_or_unit in str(LinearUnit):
            unit = container_or_unit
        if container_or_unit and container_or_unit in str(AngularUnit):
            angular_unit = container_or_unit

        converted_fields: dict[str, tuple[Any,FieldInfo]] = {}
        # Convert the labels to lists of strings
        angular_labels = list(AngularLabel.__args__)
        linear_labels = list(LinearLabel.__args__)

        for key, value in self.dict().items():
            if key in linear_labels and unit is not None and unit != self.field_info(key)["unit"]:
                converted_field = self.convert_linear_unit(value, self.field_info(key)["unit"], unit)
                converted_fields[key] = (converted_field, CoordinateField(converted_field, unit=unit, **kwargs))
            elif key in angular_labels and angular_unit is not None and angular_unit != self.field_info(key)["unit"]:
                converted_field = self.convert_angular_unit(value, angular_unit)
                converted_fields[key] = (converted_field, CoordinateField(converted_field, unit=angular_unit, **kwargs))
            else:
                # If no conversion, wrap the original value and field info in a tuple
                original_field_info = self.field_info(key)
                converted_fields[key] = (value, CoordinateField(value, **original_field_info))

        # Create new dynamic model with the same fields as the current model
        return create_model(
            self.__class__.__name__,
            __base__=type(self),
            **{k: (float, v[1]) for k, v in converted_fields.items()},
        )(**{k: v[0] for k, v in converted_fields.items()})


Coord: TypeAlias = Coordinate
"""Alias for Coordinate."""
Coords: TypeAlias = Coordinate
"""Alias for Coordinate."""

class Point(Coord):
    x: float = CoordinateField(unit="m", default=0.0)
    y: float = CoordinateField(unit="m", default=0.0)
    z: float = CoordinateField(unit="m", default=0.0)

class Pose3D(Coord):
    """Absolute coordinates for a 3D space representing x, y, and theta.

    This class represents a pose in 3D space with x and y coordinates for position
    and theta for orientation.

    Attributes:
        x (float): X-coordinate in meters.
        y (float): Y-coordinate in meters.
        theta (float): Orientation angle in radians.

    Examples:
        >>> import math
        >>> pose = Pose3D(x=1, y=2, theta=math.pi / 2)
        >>> pose
        Pose3D(x=1.0, y=2.0, theta=1.5707963267948966)
        >>> pose.to("cm")
        Pose3D(x=100.0, y=200.0, theta=1.5707963267948966)
    """

    x: float = CoordinateField(unit="m", default=0.0)
    y: float = CoordinateField(unit="m", default=0.0)
    theta: float = CoordinateField(unit="rad", default=0.0)

    def rotation_matrix(self) -> np.ndarray:
        """Compute the rotation matrix from the orientation angle."""
        return np.array([[np.cos(self.theta), -np.sin(self.theta)], [np.sin(self.theta), np.cos(self.theta)]])

    def translation_vector(self) -> np.ndarray:
        """Compute the translation vector from the position."""
        return np.array([self.x, self.y])


PlanarPose: TypeAlias = Pose3D


class Pose6D(Coord):
    """Absolute coordinates for a 6D space representing x, y, z, roll, pitch, and yaw.

    Examples:
        >>> pose = Pose6D(x=1, y=2, z=3, roll=0, pitch=0, yaw=np.pi / 2)
        >>> pose.to("cm")

        Pose6D(x=100.0, y=200.0, z=300.0, roll=0.0, pitch=0.0, yaw=1.5707963267948966)
        >>> pose.to("deg")

        Pose6D(x=1.0, y=2.0, z=3.0, roll=0.0, pitch=0.0, yaw=90.0)
        >>> pose.to("rotation_matrix")
        array([[ 0., -1.,  0.],
               [ 1.,  0.,  0.],
               [ 0.,  0.,  1.]])

    """

    x: float = CoordinateField(unit="m", default=0.0)
    y: float = CoordinateField(unit="m", default=0.0)
    z: float = CoordinateField(unit="m", default=0.0)
    roll: float = CoordinateField(unit="rad", default=0.0)
    pitch: float = CoordinateField(unit="rad", default=0.0)
    yaw: float = CoordinateField(unit="rad", default=0.0)

    @classmethod
    def from_position_orientation(
        cls,
        position: NumpyArray[3, float],
        orientation: NumpyArray[3, float] | NumpyArray[4, float],
        sequence: Literal["xyz", "zyx"] = "zyx",
    ) -> "Pose6D":
        if len(position) != 3 or len(orientation) not in (3, 4):
            msg = "Invalid position or orientation format"
            raise ValueError(msg)
        x, y, z = position
        if len(orientation) == 4:
            # Quaternion qw, qx, qy, qz is expected
            qw, qx, qy, qz = orientation
            rotation = Rotation.from_quat([qw, qx, qy, qz])
            roll, pitch, yaw = rotation.as_euler(sequence)
        else:
            # Euler angles roll, pitch, yaw in ZYX convention
            roll, pitch, yaw = orientation
            if sequence != "zyx":
                # Convert from the provided sequence to ZYX first
                rotation = Rotation.from_euler(sequence, [roll, pitch, yaw])
                # Scipy uses ZYX convention for as_euler
                roll, pitch, yaw = rotation.as_euler("xyz")
        return cls(x=x, y=y, z=z, roll=roll, pitch=pitch, yaw=yaw)

    @overload
    def __init__(self, x: float, y: float, z: float, roll: float, pitch: float, yaw: float): ...

    @overload
    def __init__(self, position: list[float], orientation: list[float]): ...

    @overload
    def __init__(self, xyzrpy: NDArray | list[float]): ...

    def __init__(self, *args, **data) -> None:
        """Create a new Pose6D object. As a coordinate subclass it has a NamedTuple-like interface.

        Unpacking will iterate over the field values unlike Dict-like interface which will iterate over the field names
        and values.

        Args:
            x (float): X-coordinate in meters.
            y (float): Y-coordinate in meters.
            z (float): Z-coordinate in meters.
            roll (float): Roll angle in radians.
            pitch (float): Pitch angle in radians.
            yaw (float): Yaw angle in radians.

        Args:
            position (list[float]): A list of 3 numbers representing the position.
            orientation (list[float]): A list of 4 numbers representing the orientation as a quaternion.

        Args:
            args (Any): The arguments to initialize the pose.
            data (List[float] | Dict[str, float] | np.ndarray | Any): The data to initialize the pose.
        """
        if len(args) == 1 and isinstance(args[0], list | np.ndarray):
            if len(args[0]) == 6:
                data = dict(zip(["x", "y", "z", "roll", "pitch", "yaw"], args[0], strict=False))
            elif len(args[0]) == 7:
                data = dict(zip(["x", "y", "z", "qw", "qx", "qy", "qz"], args[0], strict=False))
        elif len(args) > 2:
            data.update(
                dict(zip([k for k in ["x", "y", "z", "roll", "pitch", "yaw"] if k not in data], args, strict=False)),
            )
        elif len(args) == 2 and not data:
            data = self.from_position_orientation(data["position"], data["orientation"]).model_dump()
        super().__init__(**data)

    def to(
        self,
        container_or_unit: Any | str | None = None,
        sequence="zyx",
        unit=None,
        angular_unit=None,
        **kwargs,
    ) -> Any:
        """Convert the pose to a different unit, container, or representation.

        This method provides a versatile way to transform the Pose6D object into various
        forms, including different units, rotation representations, or container types.

        Args:
            container_or_unit (str, optional): Target container, unit, or representation.
                Special values: "quaternion"/"quat"/"q", "rotation_matrix"/"rotation"/"R".
            sequence (str, optional): Sequence for Euler angles. Defaults to "zyx".
            unit (str, optional): Target linear unit. Defaults to "m".
            angular_unit (str, optional): Target angular unit. Defaults to "rad".
            **kwargs: Additional keyword arguments for field configuration.

        Returns:
            Any: The converted pose, which could be:
                - A new Pose6D object with different units
                - A quaternion (as numpy array)
                - A rotation matrix (as numpy array)
                - A different container type (e.g., list, dict)

        Examples:
            >>> pose = Pose6D(x=1, y=2, z=3, roll=0, pitch=0, yaw=np.pi / 2)
            >>> pose.to("cm")
            Pose6D(x=100.0, y=200.0, z=300.0, roll=0.0, pitch=0.0, yaw=1.5707963267948966)
            >>> pose.to("deg")
            Pose6D(x=1.0, y=2.0, z=3.0, roll=0.0, pitch=0.0, yaw=90.0)
            >>> np.round(pose.to("quaternion"), 3)
            array([0.   , 0.   , 0.707, 0.707])
            >>> pose.to("rotation_matrix")
            array([[ 0., -1.,  0.],
                   [ 1.,  0.,  0.],
                   [ 0.,  0.,  1.]])
            >>> pose.to("list")
            [1.0, 2.0, 3.0, 0.0, 0.0, 1.5707963267948966]
        """
        if container_or_unit in ("quaternion", "quat", "q"):
            return self.quaternion(sequence=sequence)
        if container_or_unit in ("rotation_matrix", "R"):
            return self.rotation_matrix(sequence=sequence)
        if container_or_unit in ("rpy", "euler"):
            return self.roll, self.pitch, self.yaw
        if container_or_unit in ("position", "pos"):
            return self.x, self.y, self.z
        return super().to(container_or_unit, unit=unit, angular_unit=angular_unit, **kwargs)

    def quaternion(self, sequence="zyx") -> np.ndarray:
        """Convert roll, pitch, yaw to a quaternion based on the given sequence.

        This method uses scipy's Rotation class to perform the conversion.

        Args:
            sequence (str, optional): The sequence of rotations. Defaults to "zyx".

        Returns:
            np.ndarray: A quaternion representation of the pose's orientation.

        Example:
            >>> pose = Pose6D(x=0, y=0, z=0, roll=np.pi / 4, pitch=0, yaw=np.pi / 2)
            >>> np.round(pose.quaternion(), 3)
            array([0.653, 0.271, 0.653, 0.271])
        """
        euler = "xyz" if sequence == "zyx" else "zyx"
        rotation = Rotation.from_euler(euler, [self.roll, self.pitch, self.yaw])
        return rotation.as_quat()

    def rotation_matrix(self, sequence="zyx") -> NDArray[float]:
        """Convert roll, pitch, yaw to a rotation matrix based on the given sequence.

        This method uses scipy's Rotation class to perform the conversion.

        Args:
            sequence (str, optional): The sequence of rotations. Defaults to "zyx".

        Returns:
            np.ndarray: A 3x3 rotation matrix representing the pose's orientation.

        Example:
            >>> pose = Pose6D(x=0, y=0, z=0, roll=0, pitch=np.pi / 2, yaw=0)
            >>> np.round(pose.rotation_matrix(), 3)
            array([[ 0., -0.,  1.],
                   [ 0.,  1.,  0.],
                   [-1., -0.,  0.]])
        """
        rotation: Rotation = Rotation.from_euler(sequence, [self.roll, self.pitch, self.yaw])
        return cast( NDArray[np.float64], rotation.as_matrix())


Pose: TypeAlias = Pose6D



class PlaneModel(Coordinate):
    """ax + by + cz + d = 0."""

    _info: Dict[str, Any] = CoordinateField(reference_frame="camera", visibility="private")
    a: float
    b: float
    c: float
    d: float

    def __slice__(self, start: int = 0, stop: int = -1, step: int = 1) -> ArrayLike:
        return self.numpy()[start:stop:step]

    def __getitem__(self, item: int | str) -> float:
        if isinstance(item, str):
            return getattr(self, item)
        return self.numpy()[item]
    
    @computed_field
    def normal(self) -> Point:
        """Calculate the normal vector of the plane."""
        return Coordinate(
            **dict(zip("xyz", [self.a, self.b, self.c])),
        )



class Plane(Sample):
    coefficients: PlaneModel
    inliers: List | None = None
    point_cloud: Any | None = None

    @staticmethod
    def normal(coefficients: PlaneModel) -> Point:
        """Calculate the normal vector of the plane."""
        return Coordinate(
            **dict(zip("xyz", coefficients[:3] / np.linalg.norm(coefficients[:3]), strict=False))
        )

    def __init__(self, coefficients: PlaneModel | ArrayLike, inliers: List | None = None, point_cloud: Any | None = None, **kwargs):
        if isinstance(coefficients, np.ndarray):
            coefficients = PlaneModel(**dict(zip("abcd", coefficients, strict=False)))
        super().__init__(coefficients=coefficients, inliers=inliers, point_cloud=point_cloud, **kwargs)

if __name__ == "__main__":
    p = Pose6D(x=1, y=2, z=3, roll=0, pitch=0, yaw=np.pi / 2)
    p = Pose3D(np.array([1, 2, 3]))
