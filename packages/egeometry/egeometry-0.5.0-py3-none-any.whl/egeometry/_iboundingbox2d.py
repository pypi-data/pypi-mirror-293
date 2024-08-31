# generated from codegen/templates/_boundingbox2d.py

from __future__ import annotations

__all__ = ["IBoundingBox2d", "IBoundingBox2dOverlappable"]

# emath
from emath import IVector2

# python
from typing import Protocol
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # egeometry
    from ._icircle import ICircle
    from ._irectangle import IRectangle


class IBoundingBox2dOverlappable(Protocol):
    def overlaps_i_bounding_box_2d(self, other: IBoundingBox2d) -> bool:
        ...


class IBoundingBox2d:
    __slots__ = ["_extent", "_position", "_size"]

    def __init__(self, position: IVector2, size: IVector2):
        if size < IVector2(0):
            raise ValueError("each size dimension must be >= 0")
        self._position = position
        self._size = size
        self._extent = self._position + self._size

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, IBoundingBox2d):
            return False
        return self._position == other._position and self._size == other._size

    def __repr__(self) -> str:
        return f"<BoundingBox2d position={self._position} size={self._size}>"

    def overlaps(self, other: IVector2 | IBoundingBox2dOverlappable) -> bool:
        if isinstance(other, IVector2):
            return self.overlaps_i_vector_2(other)
        try:
            other_overlaps = other.overlaps_i_bounding_box_2d
        except AttributeError:
            raise TypeError(other)
        return other_overlaps(self)

    def overlaps_i_circle(self, other: ICircle) -> bool:
        return other.overlaps_i_bounding_box_2d(self)

    def overlaps_i_rectangle(self, other: IRectangle) -> bool:
        return other.overlaps_i_bounding_box_2d(self)

    def overlaps_i_bounding_box_2d(self, other: IBoundingBox2d) -> bool:
        return not (
            self._position.x >= other._extent.x
            or self._extent.x <= other._position.x
            or self._position.y >= other._extent.y
            or self._extent.y <= other._position.y
        )

    def overlaps_i_vector_2(self, other: IVector2) -> bool:
        return (
            other.x >= self._position.x
            and other.x < self._extent.x
            and other.y >= self._position.y
            and other.y < self._extent.y
        )

    def translate(self, translation: IVector2) -> IBoundingBox2d:
        return IBoundingBox2d(self._position + translation, self._size)

    @property
    def bounding_box(self) -> IBoundingBox2d:
        return self

    @property
    def extent(self) -> IVector2:
        return self._extent

    @property
    def position(self) -> IVector2:
        return self._position

    @property
    def size(self) -> IVector2:
        return self._size
