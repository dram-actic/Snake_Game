import pygame
import os
import random

pygame.init()

# Background Music setting
pygame.mixer.init()
pygame.mixer.music.load('music/startmusic.mp3')
pygame.mixer.music.play(15)
pygame.mixer.music.set_volume(0.6)

#set Window Screen
screen_wid = 720
screen_height = 480
gameWindow = pygame.display.set_mode((screen_wid, screen_height))

# Background Image setting
bgimg = pygame.image.load('Images/bgimg.jpg')
bgimg = pygame.transform.scale(bgimg, (screen_wid, screen_height)).convert_alpha()
intro = pygame.image.load('Images/startimage.jpg')
intro = pygame.transform.scale(intro, (screen_wid, screen_height)).convert_alpha()

#setting game Title
pygame.display.set_caption("Snake")
pygame.display.update()

#Setting colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (17, 124, 19)
peru = (205, 132, 63)
yellow = (255,184,14)
blue = (168,226,249)
grey = (216,216,216)
cream = (255,254,237)
pink = (251,150,181)
light_yellow = (253,233,125)
infra_red = (253, 68, 112)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 47)

def txt_screen(text, color, x, y) :
    screen_txt = font.render(text, True, color)
    gameWindow.blit(screen_txt, [x, y])

def snake_plot(gameWindow, color, snake_list, snake_size) :
    for x,y in snake_list :
        pygame.draw.rect(gameWindow, color, [x,y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game :
        # gameWindow.fill(blue)
        gameWindow.blit(intro, (0,0))
        txt_screen("Snake Game", pink, 270, 175)
        txt_screen("Press Space to Play", pink, 210, 225)
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                exit_game = True
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE :
                    pygame.mixer.music.load('music/bgmusic.mp3')
                    pygame.mixer.music.play()
                    pygame.mixer.music.set_volume(0.6)
                    gameloop()
        pygame.display.update()
        clock.tick(60)


# Game Loop
def gameloop() :

# Game event
    exit_game = False
    game_over = False
    x_pos = 200
    x_velocity = 0
    y_pos = 125
    y_velocity = 0
    init_velocity = 3
    snake_list = []
    snake_length = 1
    snake_size = 15
    fps = 60
    score = 0

# Bug fixing. if file doesn't exists shows error
    if not os.path.exists("highscore.txt") :
        with open("highscore.txt", "w") as f :
            f.write("0")
    with open("highscore.txt", "r") as f:
        highscore = f.read()

# Food Variables
    food_x = random.randint(20, screen_wid / 1.2)
    food_y = random.randint(20, screen_height / 1.2)
    food_size = 10

    while not exit_game :

        if game_over :
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))
# GameOverScreen
            gameWindow.fill(grey)
            txt_screen("Game Over!", infra_red, 275, 180)
            txt_screen("Press Enter to continue", infra_red, 180, 225)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN :
                        welcome()

        else :

            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    exit_game = True

                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d :
                        x_velocity = init_velocity
                        y_velocity = 0
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a :
                        x_velocity = -init_velocity
                        y_velocity = 0
                    elif event.key == pygame.K_UP or event.key == pygame.K_w :
                        y_velocity = -init_velocity
                        x_velocity = 0
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s :
                        y_velocity = init_velocity
                        x_velocity = 0

            x_pos += x_velocity
            y_pos += y_velocity

            if abs(x_pos-food_x)<12 and abs(y_pos-food_y)<12 :
                pygame.mixer.music.load('music/eatSound.mp3')
                pygame.mixer.music.play()
                pygame.mixer.music.set_volume(0.6)
                score += 10
                food_x = random.randint(20, screen_wid / 1.2)
                food_y = random.randint(20, screen_height / 1.2)
                snake_length += 5
                if score > int(highscore) :
                    highscore = score

            # gameWindow.fill(green)
            gameWindow.blit(bgimg, (0, 0))
            txt_screen("Score : " + str(score) + "  Highsocre : " + str(highscore), red, 10, 10)
            pygame.draw.rect(gameWindow, light_yellow, [food_x, food_y, food_size, food_size])

            head = []
            head.append(x_pos)
            head.append(y_pos)
            snake_list.append(head)

            if len(snake_list)>snake_length :
                del snake_list[0]

            if head in snake_list[ : -1] :
                game_over = True
                pygame.mixer.music.load('music/collapsemusic.mp3')
                pygame.mixer.music.play()
                pygame.mixer.music.set_volume(0.6)

            if x_pos < 0 or x_pos > screen_wid or y_pos < 0 or y_pos > screen_height :
                game_over = True
                pygame.mixer.music.load('music/collapsemusic.mp3')
                pygame.mixer.music.play()
                pygame.mixer.music.set_volume(0.6)

            snake_plot(gameWindow, black, snake_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

welcome()