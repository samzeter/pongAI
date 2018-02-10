import sys
import pygame
import random
from pygame.locals import *

# CONSTANTS
BLACK = 0, 0, 0
WHITE = 255, 255, 255
FPS = 60
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
BALL_WIDTH, BALL_LENGTH = 15, 15
PADDLE_WIDTH, PADDLE_LENGTH = 25, 100
UP = [0, -1]
DOWN = [0, 1]
PADDLE_BUFFER = 10
THICKNESS = 10
pygame.font.init()
FONT = pygame.font.Font('freesansbold.ttf', 20)


# CLASSES

class Object:
    def __init__(self, x, width, length, color, surf):
        self.x = x  # objects x co-ordinate
        self.color = color
        self.surf = surf
        self.y = (WINDOW_WIDTH/2 - PADDLE_WIDTH/2)
        self.rect = pygame.Rect(self.x, self.y, width, length)
        self.score = 0

    def draw(self):
        return pygame.draw.rect(self.surf, self.color, self.rect)


class Arena:
    def __init__(self, surf, color):
        self.surf = surf
        self.color = color
        
    def update(self, player, computer):
        self.surf.fill(self.color)
        pygame.draw.rect(self.surf, self.color, ((0, 0), (
                WINDOW_WIDTH, WINDOW_HEIGHT)), THICKNESS)
        score_text = "Player: " + str(
            player.score) + "   :  Computer: " + str(computer.score)
        textSurface = FONT.render(score_text, True, WHITE)
        self.surf.blit(textSurface, (WINDOW_WIDTH/4, 0))


def main():
    init()
    runGame()


def init():
    global DISPLAY_SURF, FPS_CLOCK, FONT
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("PONG")


def random_int():
    x = 1 if random.random() < 0.5 else -1
    y = 1 if random.random() < 0.5 else -1
    return x, y


def runGame():
    # creating objects
    arena = Arena(DISPLAY_SURF, BLACK)
    ball = Object((WINDOW_WIDTH/2 - BALL_WIDTH/2),
                  BALL_WIDTH, BALL_LENGTH, WHITE, DISPLAY_SURF)
    player = Object(PADDLE_BUFFER, PADDLE_WIDTH,
                    PADDLE_LENGTH, WHITE, DISPLAY_SURF)
    computer = Object((WINDOW_WIDTH-PADDLE_WIDTH-PADDLE_BUFFER),
                      PADDLE_WIDTH, PADDLE_LENGTH, WHITE, DISPLAY_SURF)

    # create random start position for ball
    r_x, r_y = random_int()
    print("Random Starting position X:", r_x, "Y: ", r_y)
    position = [r_x, r_y]  # movement of ball
    sPressed = False  # move paddle down
    wPressed = False  # move paddle up

    # Main event loop
    # PART 1: HANDLING USER INPUT
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            # KEYDOWN assignments - when key is pressed
            elif event.type == KEYDOWN:
                if event.key == K_w:
                    wPressed = True #"up" is pressed
                elif event.key == K_s:
                    sPressed = True #"down" is pressed
                elif event.key == K_ESCAPE:
                    terminate()

        # KEYUP assignments - when key goes up, stop movement
            elif event.type == KEYUP:
                if event.key == K_s:
                    sPressed = False
                elif event.key == K_w:
                    wPressed = False

    # PART 2: UPDATING THE GAME STATE
        # player paddle movement
        if sPressed and player.rect.bottom < WINDOW_HEIGHT:
            player.rect = player.rect.move(DOWN)
        elif wPressed and player.rect.top > 0:
            player.rect = player.rect.move(UP)

        # computer paddle movement
        if position[0] == -1:  # if ball is moving away
            if computer.rect.centery < (WINDOW_HEIGHT/2):
                computer.rect = computer.rect.move(DOWN)
                print("AWAY DOWN")
            elif computer.rect.centery > (WINDOW_HEIGHT/2):
                computer.rect = computer.rect.move(UP)
                print("AWAY UP")

        # if ball is moving towards paddle, track its movement
        # if ball is travelling down and computer paddles base is less than
        # that of the window
        elif position[0] == 1:
            if computer.rect.centery < ball.rect.centery:
                computer.rect = computer.rect.move(DOWN)
                print("TOWARDS DOWN")
            elif computer.rect.centery > ball.rect.centery:
                computer.rect = computer.rect.move(UP)
                print("TOWARDS UP")

        # ball movement
        ball.rect = ball.rect.move(position)
        
        # ball reflection from walls
        if ball.rect.left < 0 or ball.rect.right > WINDOW_WIDTH:
            position[0] = -position[0]
#            print("TEST")
        if ball.rect.top < 0 or ball.rect.bottom > WINDOW_HEIGHT:
            position[1] = -position[1]
#            print("TEST")

        # collision
        if (ball.rect.colliderect(player.rect)) or (
                ball.rect.colliderect(computer.rect)):
            position[0] = -position[0]
            position[1] = -position[1]
        
        # if ball goes out of bounds -update score
        # if ball goes past paddle on LHS
        if ball.rect.x == -1:
            computer.score = computer.score + 1
            # update the score
            # textSurface, textRect = updateScore(player, computer)            
            
            # if ball goes past paddle on RHS
        elif ball.rect.x == (WINDOW_WIDTH-BALL_WIDTH+1):
            player.score += 1
            print(player.score)
            
    # PART 3: RERENDERING THE SCENE
        arena.update(player, computer)
        computer.draw()
        player.draw()
        ball.draw()

        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
