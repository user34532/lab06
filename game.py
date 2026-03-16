import pygame
import random

# Constants
WIDTH = 900
HEIGHT = 700
GRID = 20

BLACK = (0, 0, 0)
GREEN = (0, 0 , 255)
HEAD_GREEN = (0, 255, 0)
RED = (255,150, 0)
WHITE = (255, 255, 255)

SNAKE_SPEED = 12


class SnakeGame:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)

        self.reset()

    def reset(self):
        self.snake = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (GRID, 0)

        self.score = 0
        self.game_over = False

        self.food = []
        for _ in range(3):
            self.spawn_food()

    def spawn_food(self):
        while True:
            x = random.randrange(0, WIDTH, GRID)
            y = random.randrange(0, HEIGHT, GRID)
            if (x, y) not in self.snake:
                self.food.append((x, y))
                break

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r and self.game_over:
                    self.reset()

                if event.key == pygame.K_w and self.direction != (0, GRID):
                    self.direction = (0, -GRID)

                if event.key == pygame.K_s and self.direction != (0, -GRID):
                    self.direction = (0, GRID)

                if event.key == pygame.K_a and self.direction != (GRID, 0):
                    self.direction = (-GRID, 0)

                if event.key == pygame.K_d and self.direction != (-GRID, 0):
                    self.direction = (GRID, 0)

    def update(self):
        if self.game_over:
            return

        head_x, head_y = self.snake[0]
        dx, dy = self.direction

        new_head = (head_x + dx, head_y + dy)

        # Wall collision
        if (
            new_head[0] < 0
            or new_head[0] >= WIDTH
            or new_head[1] < 0
            or new_head[1] >= HEIGHT
        ):
            self.game_over = True
            return

        # Self collision
        if new_head in self.snake:
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        if new_head in self.food:
            self.food.remove(new_head)
            self.score += 10
            self.spawn_food()
        else:
            self.snake.pop()

    def draw(self):
        self.screen.fill(BLACK)

        # Draw snake
        for i, segment in enumerate(self.snake):
            color = HEAD_GREEN if i == 0 else GREEN
            pygame.draw.rect(self.screen, color, (*segment, GRID, GRID))

        # Draw food
        for f in self.food:
            pygame.draw.circle(
                self.screen,
                RED,
                (f[0] + GRID // 2, f[1] + GRID // 2),
                GRID // 2,
            )

        # Score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        food_text = self.font.render(f"Food: {len(self.food)}", True, WHITE)

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(food_text, (10, 40))

        if self.game_over:
            game_over_text = self.font.render(
                "GAME OVER - Press R to Restart", True, WHITE
            )
            rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(game_over_text, rect)

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(SNAKE_SPEED)


if __name__ == "__main__":
    game = SnakeGame()
    game.run()
