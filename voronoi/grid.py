from dataclasses import dataclass
from enum import IntEnum

import numpy as np


class Cell(IntEnum):
    EMPTY = 0


COLOR_TABLE = np.array(
    [
        [255, 255, 255],  # EMPTY
    ],
    dtype=np.uint8,
)


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
        self.values = np.full(
            (self.config.rows, self.config.cols),
            Cell.EMPTY,
            dtype=np.int8,
        )

    def reset(self) -> None:
        self.values.fill(Cell.EMPTY)

    def in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.config.rows and 0 <= col < self.config.cols

    def cell_from_pixel(self, x: int, y: int) -> tuple[int, int]:
        return x // self.config.cell_size, y // self.config.cell_size

    def set_cell(self, row: int, col: int, cell: Cell) -> bool:
        if not self.in_bounds(row, col):
            return False
        self.values[row, col] = cell
        return True

    def get_cell(self, row: int, col: int) -> Cell | None:
        if not self.in_bounds(row, col):
            return None
        return Cell(self.values[row, col])

    def to_rgb(self) -> np.ndarray:
        return COLOR_TABLE[self.values]
