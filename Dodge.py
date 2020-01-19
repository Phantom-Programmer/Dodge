# Python
# Phantom_Programmer
# A simple dodge game

# Imports modules
import pygame, sys, random, time
from pygame.locals import *
# Initiates pygame
pygame.init()
# Sets up dictionaries
mouse = {"x": 0, "y": 0, "down": False}
window = {"width": 800, "height": 600, "caption": "Dodge"}
player = {"x": window["width"] / 2, "y": window["height"] - 40, "size": 40, "color": (255, 0, 0)}
# Sets up lists
blocks = []
# Sets up variables
clock = pygame.time.Clock()

# FUNCTIONS
def drawText(text, x, y, size=20, color=(0, 0, 0), centered=1, return_rect=0, antialiazation=False, alternate_surface=0, font='freesansbold.ttf'):
    # Draws the text to the display surface
    fontObj = pygame.font.Font(font, size)
    textSurfaceObj = fontObj.render(text, antialiazation, color)
    if centered == 1:
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (x, y)
        if not alternate_surface:
            DS.blit(textSurfaceObj, textRectObj)
        else:
            alternate_surface.blit(textSurfaceObj, textRectObj)
        if return_rect == (True or 1):
            return textRectObj
    else:
        textRectObj = textSurfaceObj.get_rect()
        if not alternate_surface:
            DS.blit(textSurfaceObj, (x, y))
        else:
            alternate_surface.blit(textSurfaceObj, (x, y))
        if return_rect == (True or 1):
            return textRectObj

def get_mouse_input():
    # Gets the mouse input
    mouse["x"], mouse["y"] = pygame.mouse.get_pos()
    mouse["down"] = pygame.mouse.get_pressed()[0]

def set_up_window(width, height, caption):
    # Sets up the window
    global DS
    DS = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    
def terminate():
    # Terminates the game
    pygame.quit()
    sys.exit()

# MAIN FUNCTION(S)
def game():
    # Sets up the game
    running = True
    # Sets up the key dictionary
    key = {"left": False, "right": False}
    # Sets up the blocks
    blocks = [[random.randint(0, window["width"] - 40), 0 - 50, random.randint(10, 40), (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)), random.randint(5, 15)]]
    # Sets up teh block counter for spawning bocks
    block_counter = 10
    # Sets up the score
    score = 0
    while running:
        clock.tick(30)
        # Gets the input
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_LEFT:
                    key["left"] = True
                    key["right"] = False
                if event.key == K_RIGHT:
                    key["right"] = True
                    key["left"] = False
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    key["left"] = False
                if event.key == K_RIGHT:
                    key["right"] = False
        # Moves the player
        if key["left"]:
            if player["x"] > 0:
                player["x"] -= 5
        if key["right"]:
            if player["x"] < window["width"] + player["size"]:
                player["x"] += 5
        # Spawns blocks
        block_counter -= 1
        if block_counter <= 0:
            block_counter = random.randint(5, 15)
            blocks.append([random.randint(0, window["width"] - 40), 0 - 50, random.randint(10, 40), (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)), random.randint(5, 15)])
        # Clears the display
        DS.fill((0, 0, 0))
        # Draws the falling blocks
        block = 0
        for i in range(0, len(blocks)):
            pygame.draw.rect(DS, blocks[block][3], (blocks[block][0], blocks[block][1], blocks[block][2], blocks[block][2]))
            blocks[block][1] += blocks[block][4]
            if blocks[block][1] >= window["height"]:
                del blocks[block]
                block -= 1
                score += 1
            # Goes to the next block
            block += 1
        # Checks for collisions between the player and the falling blocks
        for i in range(0, len(blocks)):
            # Makes the rects for collision detection
            player_rect = pygame.Rect(player["x"], player["y"], player["size"], player["size"])
            block_rect = pygame.Rect(blocks[i][0], blocks[i][1], blocks[i][2], blocks[i][2])
            # Checks if there is a collision
            if player_rect.colliderect(block_rect):
                running = False
        # Draws the player
        pygame.draw.rect(DS, player["color"], (player["x"], player["y"], player["size"], player["size"]))
        # Draws the score
        drawText("Score: " + str(score), 10, 10, 30, (255, 255, 255), 0, 0, True)
        # Updates the display
        pygame.display.flip()
    # Draws the scrore
    drawText("GAME OVER", window["width"] / 2, window["height"] / 2, 30, (255, 255, 255), 1, 0, True)
    drawText("Score: " + str(score), window["width"] / 2, window["height"] / 2 + 30, 30, (255, 255, 255), 1, 0, True)
    pygame.display.flip()
    time.sleep(3)

def menu():
    # Sets up the text sizes fo rtest interaction
    play_size = 40
    exit_size = 40
    # Makes blocks too make the menu look better
    for i in range(0, 10):
        size = random.randint(10, 40)
        x = random.randint(0, window["width"] - size)
        y = random.randint(0, window["height"] - size)
        color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        blocks.append([x, y, size, color])
    while True:
        clock.tick(30)
        # Gets input
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
        # Gets the mouse input
        get_mouse_input()
        # Clears the display
        DS.fill((0, 0, 0))
        # Draws stuff in the background to make the menu look less "bland"
        for i in range(0, len(blocks)):
            pygame.draw.rect(DS, blocks[i][3], (blocks[i][0], blocks[i][1], blocks[i][2], blocks[i][2]))
            blocks[i][1] += 5
            if blocks[i][1] >= window["height"]:
                blocks[i][1] = 0 - blocks[i][2]
                blocks[i][0] = random.randint(0, window["width"] - blocks[i][2])
        # Draws the title
        drawText("Dodge", window["width"] / 2, 50, 40, (255, 255, 255), 1, 0, True)
        # Draws the buttons
        Play = drawText("Play", window["width"] / 2, window["height"] / 2 - 30, play_size, (255, 255, 255), 1, 1, True)
        Exit = drawText("Exit", window["width"] / 2, window["height"] / 2 + 30, exit_size, (255, 255, 255), 1, 1, True)
        # Makes a mouse rect for collision detection
        mouse_rect = pygame.Rect(mouse["x"], mouse["y"], 1, 1)
        # Checks if the play button gets touched or clicked
        if mouse_rect.colliderect(Play):
            play_size = 50
            if mouse["down"]:
                game()
        else:
            play_size = 40
        # Checks if the exit button gets touched or clicked
        if mouse_rect.colliderect(Exit):
            exit_size = 50
            if mouse["down"]:
                terminate()
        else:
            exit_size = 40
        # Updates the display
        pygame.display.flip()

def main():
    # Sets up the main window
    set_up_window(window["width"], window["height"], window["caption"])
    while True:
        menu()
        
main()