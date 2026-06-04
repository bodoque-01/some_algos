import pygame

from grid import Grid, GridConfig

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


def draw_grid(screen: pygame.Surface, grid: Grid) -> None:
    surface = pygame.surfarray.make_surface(grid.to_rgb())
    scaled = pygame.transform.scale(surface, grid.config.window_size)
    screen.blit(scaled, (0, 0))
    draw_delimitations(screen, grid)
    pygame.display.flip()


def main() -> None:
    config = GridConfig()
    grid = Grid(config)

    pygame.init()
    screen = pygame.display.set_mode(config.window_size)
    pygame.display.set_caption("Voronoi - grid")
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_grid(screen, grid)
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
