import pygame

from grid import Grid, GridConfig
from player import Player

GRID_LINE_COLOR = (0, 102, 0)


def draw_delimitations(screen: pygame.Surface, grid: Grid) -> None:
    width, height = grid.config.window_size
    rows, cols = grid.config.rows, grid.config.cols

    for col in range(cols + 1):
        x = col * width // cols
        pygame.draw.line(screen, GRID_LINE_COLOR, (x, 0), (x, height))
    for row in range(rows + 1):
        y = row * height // rows
        pygame.draw.line(screen, GRID_LINE_COLOR, (0, y), (width, y))


class Renderer:
    """Holds reusable surfaces so each frame avoids per-frame allocations."""

    def __init__(self, grid: Grid) -> None:
        self.cell_surface = pygame.Surface((grid.config.rows, grid.config.cols))
        self.scaled_surface = pygame.Surface(grid.config.window_size)

    def draw(self, screen: pygame.Surface, grid: Grid) -> None:
        pygame.surfarray.blit_array(self.cell_surface, grid.to_rgb())
        pygame.transform.scale(
            self.cell_surface, grid.config.window_size, self.scaled_surface
        )
        screen.blit(self.scaled_surface, (0, 0))
        draw_delimitations(screen, grid)
        pygame.display.flip()


def main() -> None:
    config = GridConfig()
    grid = Grid(config)

    pygame.init()
    screen = pygame.display.set_mode(config.window_size)
    pygame.display.set_caption("Voronoi")
    clock = pygame.time.Clock()
    renderer = Renderer(grid)

    players: list[Player] = []
    sim_running = False
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not sim_running:
                    row, col = grid.cell_from_pixel(*event.pos)
                    if grid.is_empty(row, col):
                        player = Player.create(len(players), row, col)
                        player.place(grid)
                        players.append(player)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and players and not sim_running:
                    for player in players:
                        player.begin()
                    sim_running = True
                elif event.key == pygame.K_r:
                    players.clear()
                    sim_running = False
                    grid.reset()

        if sim_running:
            for player in players:
                player.expand_one_step(grid)
            if not any(player.active for player in players):
                sim_running = False

        if grid.dirty:
            renderer.draw(screen, grid)
            grid.dirty = False

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
