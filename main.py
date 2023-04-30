import pygame
import random

# Initialize pygame
pygame.init()

# Title and Icon
pygame.display.set_caption("Pong")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Create screen
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Player:
    WIDTH = 20
    HEIGHT = 150
    SPEED = 15

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.score = 0

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), self.rect())

    def move(self, direction):
        self.y += (self.SPEED * direction)

    def rect(self):
        return pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

    def place_at(self, x, y):
        self.x = x
        self.y = y


class Ball:
    WIDTH = 20
    HEIGHT = 20
    INITIAL_X = SCREEN_WIDTH / 2
    INITIAL_Y = SCREEN_HEIGHT / 2

    def __init__(self, x=INITIAL_X, y=INITIAL_Y):
        self.x = x
        self.y = y
        self.x_change = random.choice([3, -3])
        self.y_change = 0

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), self.rect())

    def rect(self):
        return pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

    def move(self):
        self.x += (self.x_change * 4)
        self.y += (self.y_change * 15)  # Make the ball move faster in y-axis

    def reset_pos(self):
        self.x = self.INITIAL_X
        self.y = self.INITIAL_Y
        self.x_change = random.choice([3, -3])
        self.y_change = 0


class Game:
    def __init__(self):
        self.player1 = Player(30, SCREEN_HEIGHT / 2)
        self.player2 = Player(SCREEN_WIDTH - 50, SCREEN_HEIGHT / 3)
        self.ball = Ball()
        self.paused = False

    def ball_collision_check(self):
        ball = self.ball.rect()
        player1 = self.player1.rect()
        player2 = self.player2.rect()

        # Ball hits top or bottom
        if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
            self.ball.y_change *= -1

        # Ball hits player1
        if player1.colliderect(ball):
            self.ball.x_change = abs(self.ball.x_change)
            self.ball.y_change = -((ball.centery - player1.centery) / (player1.height / 2))

        # Ball hits player2
        if player2.colliderect(ball):
            self.ball.x_change = -abs(self.ball.x_change)
            self.ball.y_change = -((ball.centery - player2.centery) / (player2.height / 2))

        # Ball hits player1's wall
        if ball.left <= 0:
            self.player2.score += 1
            self.reset_position()
            self.paused = True

        # Ball hits player2's wall
        if ball.right >= SCREEN_WIDTH:
            self.player1.score += 1
            self.reset_position()
            self.paused = True

    def reset_position(self):
        self.ball.reset_pos()
        self.player1.place_at(30, SCREEN_HEIGHT / 2)
        self.player2.place_at(SCREEN_WIDTH - 50, SCREEN_HEIGHT / 3)

    def show_score(self):
        score_font = pygame.font.Font('freesansbold.ttf', 20)
        x = (SCREEN_HEIGHT / 2) - 27
        y = 20

        text = score_font.render(str(self.player1.score) + "  -  " + str(self.player2.score), True, (255, 255, 255))
        screen.blit(text, (x, y))

    def show_help(self):
        font = pygame.font.Font('freesansbold.ttf', 20)
        x = (SCREEN_HEIGHT / 2) - 95
        y = SCREEN_HEIGHT - 35

        if self.paused:
            text = "Press 'space' to resume"
        else:
            text = "Press 'space' to pause"

        content = font.render(text, True, (255, 255, 255))
        screen.blit(content, (x, y))

    def draw_elements(self):
        self.player1.draw()
        self.player2.draw()
        self.show_score()
        self.ball.draw()
        self.show_help()


# Game
game = Game()
running = True
while running:
    # Ensure 60 FPS
    pygame.time.Clock().tick(60)

    # Background
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game.paused = False if game.paused else True

    if not game.paused:
        keys = pygame.key.get_pressed()

        game.ball_collision_check()
        game.ball.move()

        # Move player 1's paddle
        if keys[pygame.K_w] and game.player1.rect().top > 0:
            game.player1.move(-1)
        if keys[pygame.K_s] and game.player1.rect().bottom < SCREEN_HEIGHT:
            game.player1.move(1)

        # Move player 2's paddle
        if keys[pygame.K_UP] and game.player2.rect().top > 0:
            game.player2.move(-1)
        if keys[pygame.K_DOWN] and game.player2.rect().bottom < SCREEN_HEIGHT:
            game.player2.move(1)

    game.draw_elements()
    pygame.display.update()
