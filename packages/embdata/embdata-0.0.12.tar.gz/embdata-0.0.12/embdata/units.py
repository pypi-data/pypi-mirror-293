# Copyright (c) 2024 Mbodi AI
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from typing_extensions import Literal

LinearUnit = Literal["m", "cm", "mm", "km", "in", "ft", "yd", "mi"]
AngularUnit = Literal["rad", "deg"]
TemporalUnit = Literal["s", "ms", "us", "ns"]

LinearLabel = Literal["x", "y", "z", "length", "width", "height", "radius", "l", "w", "h", "r"]
AngularLabel = Literal["roll", "pitch", "yaw", "theta", "phi", "psi", "delta", "gamma", "beta", "alpha"]
