import random
from collections import deque
from dataclasses import dataclass, field
from typing import Self

from grid import Grid

DIRECTIONS = ((0, 1), (0, -1), (1, 0), (-1, 0))


def color_for_index(index: int) -> tuple[int, int, int]:
    rng = random.Random(index)
    return rng.randint(64, 255), rng.randint(64, 255), rng.randint(64, 255)


@dataclass
class Player:
    id: int
    color: tuple[int, int, int]
    origin: tuple[int, int]
    queue: deque[tuple[int, int]] = field(default_factory=deque)
    active: bool = True

    @classmethod
    def create(cls, index: int, row: int, col: int) -> Self:
        return cls(id=index + 1, color=color_for_index(index), origin=(row, col))

    def place(self, grid: Grid) -> None:
        grid.register_owner(self.id, self.color)
        grid.claim(*self.origin, self.id)
        grid.mark_origin(*self.origin)

    def begin(self) -> None:
        self.queue = deque([self.origin])
        self.active = True

    def expand_one_step(self, grid: Grid) -> None:
        if not self.active or not self.queue:
            self.active = False
            return

        row, col = self.queue.popleft()

        if grid.values[row, col] != self.id:
            return

        for dr, dc in DIRECTIONS:
            nr, nc = row + dr, col + dc
            if not grid.in_bounds(nr, nc):
                continue
            if not grid.is_empty(nr, nc):
                continue
            if grid.claim(nr, nc, self.id):
                self.queue.append((nr, nc))

        if not self.queue:
            self.active = False
