import pygame

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

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), self.rect())

    def move(self, direction):
        self.y += (self.SPEED * direction)

    def rect(self):
        return pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)


class Ball:
    WIDTH = 20
    HEIGHT = 20

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_change = -3
        self.y_change = 0

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), self.rect())

    def rect(self):
        return pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

    def move(self):
        self.x += (self.x_change * 4)
        self.y += (self.y_change * 15)  # Make the ball move faster in y-axis


class Game:
    def __init__(self):
        self.player1 = Player(30, SCREEN_HEIGHT / 2)
        self.player2 = Player(SCREEN_WIDTH - 50, SCREEN_HEIGHT / 4)
        self.ball = Ball(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def ball_collision_check(self):
        ball = self.ball.rect()
        player1 = self.player1.rect()
        player2 = self.player2.rect()

        if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
            self.ball.y_change *= -1

        if player1.colliderect(ball):
            self.ball.x_change = abs(self.ball.x_change)
            self.ball.y_change = -((ball.centery - player1.centery) / (player1.height / 2))

        if player2.colliderect(ball):
            self.ball.x_change = -abs(self.ball.x_change)
            self.ball.y_change = -((ball.centery - player2.centery) / (player2.height / 2))


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

    game.ball_collision_check()
    game.ball.move()

    keys = pygame.key.get_pressed()
    # Move player 1's paddle
    if keys[pygame.K_w]:
        game.player1.move(-1)
    if keys[pygame.K_s]:
        game.player1.move(1)

    # Move player 2's paddle
    if keys[pygame.K_UP]:
        game.player2.move(-1)
    if keys[pygame.K_DOWN]:
        game.player2.move(1)

    game.player1.draw()
    game.player2.draw()
    game.ball.draw()
    pygame.display.update()
