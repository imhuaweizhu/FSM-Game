# Authored by Huawei Zhu
# 2019 Feb 20
import pygame
import pygame.locals
import time
import numpy as np

from agent import agent
from enemy import enemy
from gemstone import gemstone

# ====================
# initializes all the PyGame modules, it must be called before you do anything else with PyGame.
pygame.init()
# ====================
# create a screen to display the game
screenWidth = 400   # each cell has 20 pixels width, thus 20 cells means 400 pixes
screenHeight = 600  # each cell has 20 pixels height, thus 30 cells means 600 pixes
screenSize = (screenWidth, screenHeight)
screen = pygame.display.set_mode(screenSize)  # create a screen to display on
# set screen background
screenBackground = pygame.Surface(screen.get_size())
red = 100
green = 100
blue = 100
backgroundColor = (red, green, blue)
screenBackground.fill(backgroundColor)
# set screen background for game over
screenBackground4GameOver = pygame.Surface(screen.get_size())
# ====================
# creat the agent instance
myAgent = agent()
# ====================
# create 10 enemies instances
numberOfEnemies = 10
enemyList = []
for i in range(numberOfEnemies):
    enemyList.append(enemy())  # creat a enemy instance
# ====================
# create 50 gems instances
numberOfGems = 50
gemList = []
for j in range(numberOfGems):
    gemList.append(gemstone())  # creat a gem instance

'''
************************
      The main loop
************************
'''

keepGoing = True
while keepGoing:
    # ====================
    # Check if we need to exit the game
    for event in pygame.event.get():
        if event.type == pygame.locals.KEYDOWN:  # check if any key is pressed
            if event.key == pygame.locals.K_ESCAPE:  # check if the pressed key is Esc key
                keepGoing = False  # exit the game
        elif event.type == pygame.locals.QUIT:   # if the game window is closed
            keepGoing = False  # exit the game
        else:
            pass

    # =========================
    '''while there are still gems to be collected'''
    # =========================
    while len(gemList) > 0:
        # ====================
        # draw the screen background
        # the starting position is at top-Left of the game window
        # blit() takes two arguments: The Surface to draw and the location to draw
        topLeftPosition = (0, 0)
        screen.blit(screenBackground, topLeftPosition)
        # ====================
        # draw lines to make 20x30 grid on the screen
        # each cell(grid) has 20 X 20 pixels
        red = 20
        green = 150
        blue = 200
        lineColor = (red, green, blue)
        lineWidth = 1
        gridWidth = 20  # 20 pixels
        gridHeight = 20  # 20 pixels
        for x in range(20, screenWidth, gridWidth):
            start_pos = (x, 0)
            end_pos = (x, screenHeight)
            pygame.draw.line(screen,
                             lineColor,
                             start_pos,
                             end_pos,
                             (lineWidth))
        for y in range(20, screenHeight, gridHeight):
            start_pos = (0, y)
            end_pos = (screenWidth, y)
            pygame.draw.line(screen,
                             lineColor,
                             start_pos,
                             end_pos,
                             (lineWidth))
        # ====================
        # draw all the gems
        for eachGem in gemList:
            screen.blit(eachGem.image, eachGem.rect)
        # ====================
        # determine if a gem is collected by the agent
        # if collected, delete the gem from gemList
        agentPos = np.array(myAgent.rect[0:2])
        for eachGem in gemList:
            # get each gem's top-left position
            gemPos = np.array(eachGem.rect[0:2])
            collectedGemIndex = None
            if myAgent.dst(agentPos, gemPos) == 0:
                if myAgent.isFullLoaded() is True:
                    print("Full loaded. Can't take this gem")
                else:  # myAgent.isFullLoaded() is False
                    #print("Got a Gem at = ", gemPos)
                    myAgent.collectedGemsCounter += 1
                    collectedGemIndex = gemList.index(eachGem)
                    del gemList[collectedGemIndex]
                    #print("There are", len(gemList), "gems now on the screen")
            else:
                pass
        # ====================
        # draw the agent onto the screen
        # the top-left position of the agent
        screen.blit(myAgent.image, myAgent.rect)
        # myAgent.walkRandomly()
        # ====================
        # update enemy's position, and draw all enemies
        enemyNearbyPosList = []
        agentPos = np.array(myAgent.rect[0:2])
        for eachEnemy in enemyList:
            # draw each enemy onto the screen
            screen.blit(eachEnemy.image, eachEnemy.rect)
            # find all enemies that are within 5 cells
            # 5 celles = 100 pixels
            if myAgent.dst(agentPos, np.array(eachEnemy.rect[0:2])) <= 100:
                enemyNearbyPosList.append(np.array(eachEnemy.rect[0:2]))
            # update the position of each enemy
            eachEnemy.update()
        # ========================
        # determine which one is the nearest enemy
        if len(enemyNearbyPosList) == 0:
            myAgent.isEnemyNearby = False
            myAgent.nearestEnemyPosition = None
        elif len(enemyNearbyPosList) >= 1:
            myAgent.isEnemyNearby = True
            myAgent.nearestEnemyPosition = enemyNearbyPosList[0]
            nearestDistance = myAgent.dst(
                agentPos, myAgent.nearestEnemyPosition)
            for i in range(1, len(enemyNearbyPosList), 1):
                if myAgent.dst(agentPos, enemyNearbyPosList[i]) < nearestDistance:
                    myAgent.nearestEnemyPosition = enemyNearbyPosList[i]
                else:
                    pass
        # =====================
        # update the top-left position of the agent
        myAgent.toDoNext(myAgent.rect[0:2])
        # ====================
        # sleep 0.5s
        time.sleep(0.2)
        # ====================
        # flip() updates the entire screen with everything that has been drawn since the last flip.
        pygame.display.flip()
    # =========================
    '''End of while there are still gems to be collected.'''
    # =========================

    # =========================
    '''All gems are collected'''
    screen.blit(pygame.image.load("winGame.png").convert(), (0, 0))
    pygame.display.flip()
'''
************************
  End of The main loop
************************
'''
