import pygame
import sys
import random

pygame.init()
pygame.mixer.init()

collect_sound = pygame.mixer.Sound("sounds/collect_point.mp3")
game_over_sound = pygame.mixer.Sound("sounds/game_over.mp3")

WIDTH, HEIGHT = 800, 530
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

BACKGROUND = (10, 15, 25)
SNAKE_HEAD = (76, 175, 80)
SNAKE_BODY = (56, 142, 60)
FOOD_COLOR = (244, 67, 54)
TEXT_COLOR = (255, 255, 255)
HOVER_COLOR = (100, 100, 255)
OVERLAY_COLOR = (0, 0, 0, 180)

score_font = pygame.font.SysFont("consolas", 28, bold=True)
big_font = pygame.font.SysFont("consolas", 64, bold=True)
button_font = pygame.font.SysFont("consolas", 30, bold=True)

def draw_text(text, font, color, center):
    render = font.render(text, True, color)
    rect = render.get_rect(center=center)
    screen.blit(render, rect)

class Button:
    def __init__(self, text, center, width=220, height=60):
        self.text = text
        self.center = center
        self.width = width
        self.height = height
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = center
        self.clicked = False

    def draw(self, surface, mouse_pos):
        color = HOVER_COLOR if self.rect.collidepoint(mouse_pos) else TEXT_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        draw_text(self.text, button_font, BACKGROUND, self.rect.center)

    def is_clicked(self, mouse_pos, mouse_pressed):
        if self.rect.collidepoint(mouse_pos):
            if mouse_pressed[0]:
                if not self.clicked:
                    self.clicked = True
                    return True
            else:
                self.clicked = False
        else:
            self.clicked = False
        return False

def draw_score(score):
    score_text = score_font.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(score_text, (10, 10))

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.score = 0
        self.grow_to = 3
        self.speed = 10

    def get_head_position(self):
        return self.positions[0]

    def set_direction(self, new_dir):
        opposite = (-self.direction[0], -self.direction[1])
        if new_dir != opposite:
            self.next_direction = new_dir

    def update(self):
        self.direction = self.next_direction

        head = self.get_head_position()
        x, y = self.direction
        new_position = ((head[0] + x) % GRID_WIDTH, (head[1] + y) % GRID_HEIGHT)

        if new_position in self.positions[1:]:
            return False

        self.positions.insert(0, new_position)
        if len(self.positions) > self.grow_to:
            self.positions.pop()
        return True

    def render(self):
        for i, pos in enumerate(self.positions):
            rect = pygame.Rect(pos[0]*GRID_SIZE, pos[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE)
            color = SNAKE_HEAD if i == 0 else SNAKE_BODY
            pygame.draw.rect(screen, color, rect, border_radius=6)

class Food:
    def __init__(self, snake_positions):
        self.position = (0, 0)
        self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions):
        available_positions = [
            (x, y)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x, y) not in snake_positions
        ]
        if not available_positions:
            return
        self.position = random.choice(available_positions)

    def render(self):
        rect = pygame.Rect(
            self.position[0]*GRID_SIZE, self.position[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(screen, FOOD_COLOR, rect, border_radius=8)

def start_menu():
    play_button = Button("Play", (WIDTH // 2, HEIGHT // 2))
    quit_button = Button("Quit", (WIDTH // 2, HEIGHT // 2 + 90))

    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        screen.fill(BACKGROUND)

        draw_text("🐍 SNAKE GAME 🐍", big_font, TEXT_COLOR, (WIDTH // 2, HEIGHT // 3))

        play_button.draw(screen, mouse_pos)
        quit_button.draw(screen, mouse_pos)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if play_button.is_clicked(mouse_pos, mouse_pressed):
            pygame.time.wait(150)
            pygame.event.clear()
            return 'play'
        if quit_button.is_clicked(mouse_pos, mouse_pressed):
            pygame.quit()
            sys.exit()

        clock.tick(30)

def game_over_screen(score):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill(OVERLAY_COLOR)

    play_button = Button("Play Again", (WIDTH // 2, HEIGHT // 2 + 30))
    quit_button = Button("Quit", (WIDTH // 2, HEIGHT // 2 + 120))

    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        screen.fill(BACKGROUND)
        screen.blit(overlay, (0, 0))

        draw_text("GAME OVER", big_font, (255, 80, 80), (WIDTH // 2, HEIGHT // 3 - 50))
        draw_text(f"Your Score: {score}", button_font, TEXT_COLOR, (WIDTH // 2, HEIGHT // 2 - 50))  # moved up 40 px

        play_button.draw(screen, mouse_pos)
        quit_button.draw(screen, mouse_pos)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if play_button.is_clicked(mouse_pos, mouse_pressed):
            pygame.time.wait(150)
            pygame.event.clear()
            return 'play'

        if quit_button.is_clicked(mouse_pos, mouse_pressed):
            pygame.quit()
            sys.exit()

        clock.tick(30)


def game_loop():
    snake = Snake()
    food = Food(snake.positions)
    running = True

    while running:
        clock.tick(snake.speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.set_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.set_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.set_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.set_direction((1, 0))

        if not snake.update():
            game_over_sound.play()
            pygame.time.wait(1000)
            return snake.score

        if snake.get_head_position() == food.position:
            snake.score += 10
            snake.grow_to += 1
            collect_sound.play()
            food.randomize_position(snake.positions)

        screen.fill(BACKGROUND)
        snake.render()
        food.render()
        draw_score(snake.score)
        pygame.display.flip()

def main():
    # Start by showing start menu
    action = start_menu()

    while True:
        if action == 'play':
            score = game_loop()
            action = game_over_screen(score)
        else:
            # fallback to start menu if somehow other action
            action = start_menu()

if __name__ == "__main__":
    main()
