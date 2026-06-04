from dataclasses import dataclass

import numpy as np

EMPTY = 0
ORIGIN_DARKEN = 0.45


@dataclass(frozen=True, slots=True)
class GridConfig:
    rows: int = 30
    cols: int = 30
    window_size: tuple[int, int] = (800, 800)

    @property
    def cell_size(self) -> int:
        return min(self.window_size) // max(self.rows, self.cols)


class Grid:
    def __init__(self, config: GridConfig | None = None) -> None:
        self.config = config or GridConfig()
        self.values = np.zeros(
            (self.config.rows, self.config.cols),
            dtype=np.int16,
        )
        self._color_table = np.array([[255, 255, 255]], dtype=np.uint8)
        self._rgb = np.empty(
            (self.config.rows, self.config.cols, 3),
            dtype=np.uint8,
        )
        self._origins: set[tuple[int, int]] = set()
        self.dirty = True

    def reset(self) -> None:
        self.values.fill(EMPTY)
        self._color_table = np.array([[255, 255, 255]], dtype=np.uint8)
        self._origins.clear()
        self.dirty = True

    def mark_origin(self, row: int, col: int) -> None:
        if self.in_bounds(row, col):
            self._origins.add((row, col))
            self.dirty = True

    def register_owner(self, owner_id: int, color: tuple[int, int, int]) -> None:
        if owner_id >= len(self._color_table):
            extended = np.zeros((owner_id + 1, 3), dtype=np.uint8)
            extended[: len(self._color_table)] = self._color_table
            self._color_table = extended
        self._color_table[owner_id] = color
        self.dirty = True

    def is_empty(self, row: int, col: int) -> bool:
        return self.in_bounds(row, col) and self.values[row, col] == EMPTY

    def claim(self, row: int, col: int, owner_id: int) -> bool:
        if not self.in_bounds(row, col) or self.values[row, col] != EMPTY:
            return False
        self.values[row, col] = owner_id
        self.dirty = True
        return True

    def in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.config.rows and 0 <= col < self.config.cols

    def cell_from_pixel(self, x: int, y: int) -> tuple[int, int]:
        return x // self.config.cell_size, y // self.config.cell_size

    def to_rgb(self) -> np.ndarray:
        np.take(self._color_table, self.values, axis=0, out=self._rgb)
        for row, col in self._origins:
            owner = self.values[row, col]
            if owner != EMPTY:
                self._rgb[row, col] = (
                    self._color_table[owner].astype(np.float32) * ORIGIN_DARKEN
                ).astype(np.uint8)
        return self._rgb
