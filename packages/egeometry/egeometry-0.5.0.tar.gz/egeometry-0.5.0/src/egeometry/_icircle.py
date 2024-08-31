# generated from codegen/templates/_circle.py

from __future__ import annotations

__all__ = ["ICircle", "ICircleOverlappable"]

# egeometry
from ._iboundingbox2d import IBoundingBox2d

# emath
from emath import DVector2
from emath import IVector2

# python
from typing import Protocol
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # egeometry
    from ._irectangle import IRectangle


class ICircleOverlappable(Protocol):
    def overlaps_i_circle(self, other: ICircle) -> bool:
        ...


class ICircle:
    __slots__ = ["_bounding_box", "_position", "_radius"]

    def __init__(self, position: IVector2, radius: int):
        if radius <= 0:
            raise ValueError("radius must be > 0")
        self._position = position
        self._radius = radius
        self._bounding_box = IBoundingBox2d(position - radius, IVector2(radius * 2))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ICircle):
            return False
        return self._position == other._position and self._radius == other._radius

    def __repr__(self) -> str:
        return f"<Circle position={self._position} radius={self._radius}>"

    def overlaps(self, other: IVector2 | ICircleOverlappable) -> bool:
        if isinstance(other, IVector2):
            return self.overlaps_i_vector_2(other)
        try:
            other_overlaps = other.overlaps_i_circle
        except AttributeError:
            raise TypeError(other)
        return other_overlaps(self)

    def _overlaps_rect_like(self, other: IBoundingBox2d | IRectangle) -> bool:
        assert other.size != IVector2(0)
        o_center = DVector2(*other.position) + (DVector2(*other.size) * 0.5)
        f_position = DVector2(*self._position)
        diff = f_position - o_center
        closest_o_point = DVector2(
            min(max(diff.x, other.position.x), other.extent.x),
            min(max(diff.y, other.position.y), other.extent.y),
        )
        closest_o_point_distance = round(f_position.distance(closest_o_point))
        return closest_o_point_distance < self._radius

    def overlaps_i_bounding_box_2d(self, other: IBoundingBox2d) -> bool:
        if other.size == IVector2(0):
            return False
        return self._overlaps_rect_like(other)

    def overlaps_i_circle(self, other: ICircle) -> bool:
        min_distance = self._radius + other._radius
        distance = round(DVector2(*self._position).distance(DVector2(*other._position)))
        return distance < min_distance

    def overlaps_i_rectangle(self, other: IRectangle) -> bool:
        return self._overlaps_rect_like(other)

    def overlaps_i_vector_2(self, other: IVector2) -> bool:
        distance = round(DVector2(*self._position).distance(DVector2(*other)))
        return distance < self._radius

    def translate(self, translation: IVector2) -> ICircle:
        return ICircle(self._position + translation, self._radius)

    @property
    def bounding_box(self) -> IBoundingBox2d:
        return self._bounding_box

    @property
    def position(self) -> IVector2:
        return self._position

    @property
    def radius(self) -> int:
        return self._radius
