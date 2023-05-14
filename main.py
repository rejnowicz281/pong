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

main_font = pygame.font.Font('freesansbold.ttf', 20)


def draw_text(x, y, text, font=main_font, color=(255, 255, 255)):
    content = font.render(text, True, color)
    content_rect = content.get_rect(center=(x, y))
    screen.blit(content, content_rect)


class Player(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.image = self.get_player_surface()
        self.rect = self.image.get_rect(center=(x, y))
        self.score = 0
        self.speed = 15

    @staticmethod
    def get_player_surface():
        surf = pygame.Surface((20, 150))
        surf.fill((255, 255, 255))
        return surf

    def move_up(self):
        self.rect.y -= self.speed

    def move_down(self):
        self.rect.y += self.speed

    def place_at(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y


class Ball(pygame.sprite.Sprite):
    X = SCREEN_WIDTH / 2
    Y = SCREEN_HEIGHT / 2

    def __init__(self, x=X, y=Y):
        super().__init__()
        self.image = self.get_ball_surface()
        self.rect = self.image.get_rect(center=(x, y))
        self.x_change = random.choice([3, -3])
        self.y_change = 0

    @staticmethod
    def get_ball_surface():
        surf = pygame.Surface((20, 20))
        surf.fill((255, 255, 255))

        return surf

    def move(self):
        self.rect.x += (self.x_change * 4)
        self.rect.y += (self.y_change * 15)  # Make the ball move faster in y-axis

    def reset(self):
        self.rect.centerx = self.X
        self.rect.centery = self.Y
        self.x_change = random.choice([3, -3])
        self.y_change = 0

    def update(self):
        self.move()


class Game:
    PLAYER1_POS = 30, SCREEN_HEIGHT / 2 + 38
    PLAYER2_POS = SCREEN_WIDTH - 30, SCREEN_HEIGHT / 2 - 38

    def __init__(self):
        self.player1 = pygame.sprite.GroupSingle(Player(self.PLAYER1_POS[0], self.PLAYER1_POS[1]))
        self.player2 = pygame.sprite.GroupSingle(Player(self.PLAYER2_POS[0], self.PLAYER2_POS[1]))
        self.ball = pygame.sprite.GroupSingle(Ball())
        self.paused = False

    def player_input(self):
        keys = pygame.key.get_pressed()
        player1 = self.player1.sprite
        player2 = self.player2.sprite

        # Move player 1's paddle
        if keys[pygame.K_w] and player1.rect.top > 0:
            player1.move_up()
        if keys[pygame.K_s] and player1.rect.bottom < SCREEN_HEIGHT:
            player1.move_down()

        # Move player 2's paddle
        if keys[pygame.K_UP] and player2.rect.top > 0:
            player2.move_up()
        if keys[pygame.K_DOWN] and player2.rect.bottom < SCREEN_HEIGHT:
            player2.move_down()

    def ball_collision_check(self):
        ball = self.ball.sprite
        player1 = self.player1.sprite
        player2 = self.player2.sprite

        # Ball hits top or bottom
        if ball.rect.top <= 0 or ball.rect.bottom >= SCREEN_HEIGHT:
            ball.y_change *= -1

        # Ball hits player1
        if player1.rect.colliderect(ball.rect):
            ball.x_change = abs(ball.x_change)
            ball.y_change = -((ball.rect.centery - player1.rect.centery) / (player1.rect.height / 2))

        # Ball hits player2
        if player2.rect.colliderect(ball.rect):
            ball.x_change = -abs(ball.x_change)
            ball.y_change = -((ball.rect.centery - player2.rect.centery) / (player2.rect.height / 2))

        # Ball hits player1's wall
        if ball.rect.left <= 0:
            player2.score += 1
            self.reset()
            self.paused = True

        # Ball hits player2's wall
        if ball.rect.right >= SCREEN_WIDTH:
            player1.score += 1
            self.reset()
            self.paused = True

    def reset(self):
        self.ball.sprite.reset()
        self.player1.sprite.place_at(self.PLAYER1_POS[0], self.PLAYER1_POS[1])
        self.player2.sprite.place_at(self.PLAYER2_POS[0], self.PLAYER2_POS[1])

    def show_score(self):
        x = SCREEN_HEIGHT / 2
        y = 25
        text = str(self.player1.sprite.score) + "  -  " + str(self.player2.sprite.score)

        draw_text(x, y, text)

    def show_help(self):
        x = SCREEN_WIDTH / 2
        y = SCREEN_HEIGHT - 35
        text = f"Press 'space' to {'resume' if self.paused else 'pause'}"

        draw_text(x, y, text)

    def update(self):
        if not game.paused:
            self.ball_collision_check()
            self.ball.update()
            self.player_input()

        self.player1.draw(screen)
        self.player2.draw(screen)
        self.ball.draw(screen)
        self.show_score()
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

    game.update()

    pygame.display.update()
