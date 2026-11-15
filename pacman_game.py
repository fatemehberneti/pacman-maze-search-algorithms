import pygame
import random
from collections import deque

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
PACMAN_SIZE = 20
FOOD_SIZE = 14
GRID_SIZE = 20

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
PATH_COLOR = (40, 90, 160)
RED = (255, 0, 0)


class PacMan:
    def __init__(self):
        self.x = GRID_SIZE * (SCREEN_WIDTH // 2 // GRID_SIZE)
        self.y = GRID_SIZE * (SCREEN_HEIGHT // 2 // GRID_SIZE)
        self.size = PACMAN_SIZE

    def move(self, dx, dy):
        self.x = max(0, min(SCREEN_WIDTH - self.size, self.x + dx))
        self.y = max(0, min(SCREEN_HEIGHT - self.size, self.y + dy))

    def draw(self, surface):
        center = (self.x + self.size // 2, self.y + self.size // 2)
        pygame.draw.circle(surface, YELLOW, center, self.size // 2)

    def get_position(self):
        return (self.x // GRID_SIZE, self.y // GRID_SIZE)


class Food:
    def __init__(self):
        self.x = random.randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE
        self.y = random.randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        self.size = FOOD_SIZE

    def draw(self, surface):
        offset = (GRID_SIZE - self.size) // 2
        pygame.draw.rect(surface, RED, (self.x + offset, self.y + offset, self.size, self.size))

    def get_position(self):
        return (self.x // GRID_SIZE, self.y // GRID_SIZE)


def reconstruct_path(parent, current):
    path = []
    while current is not None:
        path.append(current)
        current = parent[current]
    return path[::-1]


def bfs(start, goal):
    cols = SCREEN_WIDTH // GRID_SIZE
    rows = SCREEN_HEIGHT // GRID_SIZE
    queue = deque([start])
    visited = {start}
    parent = {start: None}

    while queue:
        current = queue.popleft()
        if current == goal:
            return reconstruct_path(parent, goal)

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < cols and 0 <= neighbor[1] < rows and neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                parent[neighbor] = current
    return []


def dfs(start, goal):
    cols = SCREEN_WIDTH // GRID_SIZE
    rows = SCREEN_HEIGHT // GRID_SIZE
    stack = [start]
    visited = {start}
    parent = {start: None}

    while stack:
        current = stack.pop()
        if current == goal:
            return reconstruct_path(parent, goal)

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < cols and 0 <= neighbor[1] < rows and neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)
                parent[neighbor] = current
    return []


def ids(start, goal, max_depth=50):
    cols = SCREEN_WIDTH // GRID_SIZE
    rows = SCREEN_HEIGHT // GRID_SIZE

    for depth in range(max_depth + 1):
        stack = [(start, 0)]
        visited = {start}
        parent = {start: None}

        while stack:
            current, d = stack.pop()
            if current == goal:
                return reconstruct_path(parent, goal)

            if d < depth:
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    neighbor = (current[0] + dx, current[1] + dy)
                    if 0 <= neighbor[0] < cols and 0 <= neighbor[1] < rows and neighbor not in visited:
                        visited.add(neighbor)
                        stack.append((neighbor, d + 1))
                        parent[neighbor] = current
    return []


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pac-Man with Search Algorithms")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    pacman = PacMan()
    food = Food()
    score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT]:
            dx = -GRID_SIZE
        elif keys[pygame.K_RIGHT]:
            dx = GRID_SIZE
        elif keys[pygame.K_UP]:
            dy = -GRID_SIZE
        elif keys[pygame.K_DOWN]:
            dy = GRID_SIZE

        pacman.move(dx, dy)

        if pacman.get_position() == food.get_position():
            score += 1
            food = Food()

        goal = food.get_position()
        # Switch between bfs, dfs, or ids
        path = bfs(pacman.get_position(), goal)
        # path = dfs(pacman.get_position(), goal)
        # path = ids(pacman.get_position(), goal, max_depth=50)

        screen.fill(BLACK)

        # Draw path first so Pac-Man and food render clearly on top
        for (px, py) in path:
            pygame.draw.rect(screen, PATH_COLOR, (px * GRID_SIZE, py * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        food.draw(screen)
        pacman.draw(screen)

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(15)

    pygame.quit()


if __name__ == "__main__":
    main()