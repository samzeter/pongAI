import sys
import pygame
import random

# CONSTANTS
BLACK = 0, 0, 0
WHITE = 255, 255, 255
FPS = 60
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
BALL_SIZE = BALL_WIDTH, BALLHEIGHT = 50, 50
PADDLE_SIZE = PADDLE_WIDTH, PADDLE_HEIGHT = 25, 100
PADDLE_SPEED = 2
BALL_X_SPEED = 3
BALL_Y_SPEED = 2
DOWN = 'down'
UP = 'up'

# CLASSES


class Object:    
    def __init__(self, img, scale, x, screen=pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)), color=WHITE):
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img,scale)
        self.x = x
        self.y = random.randint(0,WINDOW_HEIGHT -PADDLE_HEIGHT)
        self.rect = pygame.Rect(x, self.y, scale[0], scale[1])
        self.score = 0
        self.draw = pygame.draw.rect(screen, color, self.rect)

# MAIN 
def main():
    init()
    runGame()

def init():
    global SCREEN, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    pygame.display.set_caption("PONG")
    


def runGame():
    theBall = Object("ball.png",(BALL_WIDTH,BALL_HEIGHT), randomX())
    pPlayer = Object("paddle.png", (PADDLE_WIDTH,PADDLE_HEIGHT),0)
    pComputer = Object("paddle.png", (PADDLE_WIDTH,PADDLE_HEIGHT),
                       WINDOW_WIDTH-PADDLE_WIDTH)

    position = [10,10] #movement of ball
    sPressed = False #move paddle down
    wPressed = False #move paddle up
    computerScore = False
    playerScore = False
    # computer - player score display
    textSurface, textRect = updateScore(pPlayer, pComputer)


    #main event loop
    #PART 1: HANDLING USER INPUT
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            #KEYDOWN assignments
            elif event.type == KEYDOWN:
                if event.key == K_w:
                    wPressed = True #"up" is pressed
                elif event.key == K_s:
                    sPressed = True #"down" is pressed
                elif event.key == K_ESCAPE:
                    terminate()

        #KEYUP assignments - when key goes up, stop movement
            elif event.type == KEYUP:
                if event.key == K_s:
                    sPressed = False
                elif event.key == K_w:
                    wPressed = False

    #PART 2: UPDATING THE GAME STATE
        #paddle movement
        if sPressed and pPlayer.rect.bottom < WINDOW_HEIGHT:
            pPlayer.rect = pPlayer.rect.move([0,5])
        elif wPressed and pPlayer.rect.top > 0:
            pPlayer.rect = pPlayer.rect.move([0,-5])

        #ball movement
        theBall.rect = theBall.rect.move(position)
        #ball reflection from walls
        if theBall.rect.left < 0 or theBall.rect.right > WINDOW_WIDTH:
            position[0] = -position[0]
        if theBall.rect.top < 0 or theBall.rect.bottom > WINDOW_HEIGHT:
            position[1] = -position[1]

        # collision
        if theBall.rect.colliderect(pPlayer.rect):
            position[0] = -position[0]
            position[1] = -position[1]
        # if ball goes out of bounds   
        if theBall.rect.x < 1:
            pComputer.score += 1
            # update the score
            textSurface, textRect = updateScore(pPlayer, pComputer)            
            
        elif theBall.rect.x > WINDOW_WIDTH-BALL_WIDTH:
            pPlayer.score += 1
            # update the score
            textSurface, textRect = updateScore(pPlayer, pComputer)
            
    #PART 3: RERENDERING THE SCENE
        SCREEN.fill(BLACK)
#        SCREEN.blit(b1, b1)
        SCREEN.blit(theBall.img,theBall.rect)
        SCREEN.blit(pPlayer.img,pPlayer.rect)
        SCREEN.blit(pComputer.img,(pComputer.x,pComputer.y))
        SCREEN.blit(textSurface,textRect)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def terminate():
    pygame.quit()
    sys.exit()

def randomX():
    return random.randint(PADDLE_WIDTH, WINDOW_WIDTH-(PADDLE_WIDTH*2))

def updateScore(pPlayer, pComputer):
    font = pygame.font.Font('freesansbold.ttf',20)
    scoreText  = "Player: " + str(pPlayer.score) + "   ||  Computer: "  + str(pComputer.score)
    textSurface = font.render(scoreText, True, WHITE)
    textRect = textSurface.get_rect()
    textRect.center = ((WINDOW_WIDTH/2),(WINDOW_HEIGHT/10))
    return textSurface, textRect
    

if __name__ == '__main__':
    main()
