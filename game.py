import pygame
import random

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 800
TILE_SIZE = 40
INITIAL_SNAKE_LENGTH = 8
SNAKE_SPEED = 8

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

def draw_tile(x, y, color):
    pygame.draw.rect(screen, color, pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE - 1, TILE_SIZE - 1))

class Snake:
    """A snake represented by a list of tiles, each tile is a list of x and y coordinates"""
    def __init__(self):
        self.body = [[i, 0] for i in range(INITIAL_SNAKE_LENGTH, 1, -1)]
        self.direction = [1, 0]
        self.grow = False
        self.score = 0

    def move(self):
        head = self.body[0].copy()
        # Move the head in the direction of the snake
        head[0] += self.direction[0]
        head[1] += self.direction[1]
        # Wrap around the screen
        head[0] %= WINDOW_WIDTH // TILE_SIZE
        head[1] %= WINDOW_HEIGHT // TILE_SIZE
        self.body.insert(0, head)
        if not self.grow:
            self.body.pop()
        self.grow = False

    def eat(self):
        self.grow = True
        self.score += 1
        self.print_score()

    @property
    def head(self):
        return self.body[0]
    
    def is_dead(self):
        return self.head in self.body[1:]

    def draw(self):
        draw_tile(self.head[0], self.head[1], BLUE)
        for tile in self.body[1:]:
            draw_tile(tile[0], tile[1], GREEN)

    def print_score(self):
        print(f"Score: {self.score}")


class Food:
    """A food represented by a list of x and y coordinates"""
    def __init__(self, snake):
        self.position = self.generate(snake)

    def generate(self, snake):
        """Generate a new position for the food that is not on the snake"""
        while True:
            position = [random.randint(0, WINDOW_WIDTH // TILE_SIZE - 1),
                        random.randint(0, WINDOW_HEIGHT // TILE_SIZE - 1)]
            if position not in snake.body:
                return position

    def draw(self):
        draw_tile(self.position[0], self.position[1], RED)


def main():

    clock = pygame.time.Clock()
    snake = Snake()
    food = Food(snake)

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.direction = [0, -1]
                elif event.key == pygame.K_DOWN:
                    snake.direction = [0, 1]
                elif event.key == pygame.K_LEFT:
                    snake.direction = [-1, 0]
                elif event.key == pygame.K_RIGHT:
                    snake.direction = [1, 0]

        snake.move()

        # Check if the snake has eaten the food
        if snake.body[0] == food.position:
            snake.eat()
            food = Food(snake)

        if snake.is_dead():
            return

        snake.draw()
        food.draw()

        pygame.display.flip()
        clock.tick(SNAKE_SPEED)


if __name__ == "__main__":
    main()