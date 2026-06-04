from collections import deque
from collections.abc import Iterator

from grid import Grid

DIRECTIONS = ((0, 1), (0, -1), (1, 0), (-1, 0))


def bfs(grid: Grid, start: tuple[int, int]) -> Iterator[tuple[int, int]]:
    """Your friendly neighborhood BFS implementation, consider neighbors in all four directions (no diagonals)."""
    queue = deque([start])
    visited = {start}

    while queue:
        row, col = queue.popleft()
        yield row, col

        for dr, dc in DIRECTIONS:
            neighbor = (row + dr, col + dc)
            if neighbor not in visited and grid.in_bounds(*neighbor):
                visited.add(neighbor)
                queue.append(neighbor)
