import pygame
import pygame.locals
import random
import numpy as np


class agent(pygame.sprite.Sprite):
    def __init__(self):
        super(agent, self).__init__()
        # the image has 20 X 20 pixels
        self.image = pygame.image.load('agent.png').convert()
        self.image.set_colorkey((255, 255, 255), pygame.locals.RLEACCEL)
        # get_rect returns a list
        # the first 2 elements are [x,y], coordinates of image's top-left corner
        self.rect = self.image.get_rect(center=(210, 310))
        # since the image is centered at [10,10], thus the topleft corner is [0,0]
        self.home = [200, 300]
        # print(self.rect[0:2])
        self.stepSize = 20  # 20 pixels is one cell on the screen
        self.collectedGemsCounter = 0
        self.goUp = np.array([0, 1])
        self.goDown = np.array([0, -1])
        self.goRight = np.array([1, 0])
        self.goLeft = np.array([-1, 0])
        self.isEnemyNearby = False
        self.nearestEnemyPosition = np.array([0, 0])
    # =============================================
    '''The following 3 methods define the 3 possible states of the agent'''
    '''Before moving, the agent should determine its states.
    There are 3 states the agent need to check for every step.
    The 1st one is to check if any enemy within 5 cells away;
    The 2nd one is to check if the agent is full loaded with 3 gems;
    The 3rd one is to check if the agent has arrived home.
    Thus the state machine should check these 3 states for the agent
    and then determine what to do at the next step'''

    # ============================================
    '''The 1st thing that's needed to check before moving
       Is there any enemy is nearby within 5 cells
       This is done in the main.py, self.isEnemyNearby is updated'''

    # ============================================
    '''The 2nd thing that's needed to check before moving.
       Is the agent full loaded with 3 gems'''

    def isFullLoaded(self):
        if self.collectedGemsCounter < 3:
            return False
        else:
            return True

    # ============================================
    '''The 3rd thing that's needed to check before moving
       Has the agent arrived home'''

    def isHome(self):
        if self.rect[0:2] == self.home:
            print("Back at home")
            return True
        elif self.rect[0:2] != self.home:
            return False

    # ============================================
    '''Based on the above 3 states, determine what to do next for the agent.
    check the explaination file for more detail for the state machine'''

    def toDoNext(self, posAgent):
        # check 3 states
        state1 = self.isEnemyNearby
        state2 = self.isFullLoaded()
        state3 = self.isHome()

        # next step based on current state
        if state1 is False and state2 is False and state3 is False:
            self.walkRandomly()

        elif state1 is False and state2 is False and state3 is True:
            self.walkRandomly()

        elif state1 is False and state2 is True and state3 is False:
            self.goHome()

        elif state1 is False and state2 is True and state3 is True:
            self.collectedGemsCounter = 0
            self.walkRandomly()

        elif state1 is True and state2 is False and state3 is False:
            self.runAway()

        elif state1 is True and state2 is False and state3 is True:
            self.runAway()

        elif state1 is True and state2 is True and state3 is False:
            self.runAway()

        else:
            self.collectedGemsCounter = 0
            self.runAway()

    # ============================================
    '''The following 3 methods define the 3 things we may need to do next'''
    '''There are 3 type of things we can do next based on the 3 states.
    The 1st thing we can do is that the agent randomly searches to find a gem stone;
    The 2nd thing we can do is that the agent run away from the enemy;
    The 3rd thing we can do is that the agent return home.'''

    # ============================================
    ''' The 1st thing we can do is that the agent randomly searches to find a gem stone.'''
    # requirement: If there is no enemy in the proximity (within 5 cells distance),
    # agent randomly search to find a gem stone.

    def walkRandomly(self):
        if self.isTopLeft() is True:
            self.move2RandomDirections(self.goDown, self.goRight)

        elif self.isTopRight() is True:
            self.move2RandomDirections(self.goDown, self.goLeft)

        elif self.isBottomLeft() is True:
            self.move2RandomDirections(self.goUp, self.goRight)

        elif self.isBottomRight() is True:
            self.move2RandomDirections(self.goUp, self.goLeft)

        elif self.isEdgeLeft() is True:
            self.move2RandomDirections(self.goUp, self.goDown, self.goRight)

        elif self.isEdgeRight() is True:
            self.move2RandomDirections(self.goUp, self.goDown, self.goLeft)

        elif self.isEdgeTop() is True:
            self.move2RandomDirections(self.goDown, self.goLeft, self.goRight)

        elif self.isEdgeBottom() is True:
            self.move2RandomDirections(self.goUp, self.goLeft, self.goRight)

        else:
            self.move2RandomDirections(self.goUp, self.goDown, self.goLeft, self.goRight)

        # Keep agent on the screen, X-axis
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= 400:
            self.rect.right = 400
        # Keep agent on the screen, Y-axis
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600

    # ============================================
    '''The 2nd thing we can do is that the agent run away from the enemy.'''
    # requirement: Agent can collect up to three stones at a time,
    # and needs to return home to store the collected stones.

    def goHome(self):
        # print("Going home")
        displacement = np.array(self.home) - np.array(self.rect[0:2])
        if displacement[0] != 0:
            stepX = self.stepSize * np.sign(displacement[0])
            stepY = 0
            self.rect.move_ip(stepX, stepY)
        elif displacement[0] == 0 and displacement[1] != 0:
            stepX = 0
            stepY = self.stepSize * np.sign(displacement[1])
            self.rect.move_ip(stepX, stepY)
        else:
            pass

    # ============================================
    '''The 3rd thing we can do is that the agent return home.'''
    # requirement: Agent run-away when there is an enemy in proximity.
    '''
    There are 3 cases when the agent wants to run away.
        case 1: The agent is at 4 corners of the screen.  Only 2 directions are available.
        case 2: The agent is on 4 edges, but not corners. Only 3 directions are available.
        case 3: The agent is neither at corners or on edges.   4 directions are available.
    '''

    def runAway(self):
        # ========================================
        # at top-left corner
        if self.isTopLeft() is True:
            self.move2Directions(self.goDown, self.goRight)
        # at top-right corner
        elif self.isTopRight() is True:
            self.move2Directions(self.goDown, self.goLeft)
        # at bottom-left corner
        elif self.isBottomLeft is True:
            self.move2Directions(self.goUp, self.goRight)
        # at bottom-right corner
        elif self.isBottomRight is True:
            self.move2Directions(self.goUp, self.goLeft)
        # on the left edge, but not corners
        elif self.isEdgeLeft() is True:
            self.move2Directions(self.goUp, self.goDown, self.goRight)
        # on the right edge, but not corners
        elif self.isEdgeRight() is True:
            self.move2Directions(self.goUp, self.goDown, self.goLeft)
        # on the top edge, but not corners
        elif self.isEdgeTop() is True:
            self.move2Directions(self.goDown, self.goLeft, self.goRight)
        # on the bottom edge, but not corners
        elif self.isEdgeBottom() is True:
            self.move2Directions(self.goUp, self.goLeft, self.goRight)
        # neither corners nor edges
        else:
            self.move2Directions(self.goUp, self.goDown, self.goLeft, self.goRight)
        # ===================================
        # Keep agent on the screen
        # X-axis
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= 400:
            self.rect.right = 400
        # Y-axis
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600

    # ==============================
    # this function is only used inside runaway() method
    # calculate L2 distance between 2 numpy arrays
    def dst(self, a, b):
        if isinstance(a, np.ndarray) and isinstance(b, np.ndarray):
            return np.linalg.norm(a - b)
        else:
            raise Exception("Wrong calling of method: dst")

    # ==============================
    # is the agent at top-left corner
    def isTopLeft(self):
        if self.dst(np.array(self.rect[0:2]), np.array([0, 0])) == 0.0:
            print("====TopLeft")
            return True
        else:
            return False

    # ==============================
    # is the agent at top-right corner
    def isTopRight(self):
        if self.dst(np.array(self.rect[0:2]), np.array([380, 0])) == 0.0:
            print("====TopRight")
            return True
        else:
            return False

    # ==============================
    # is the agent at bottom-left corner
    def isBottomLeft(self):
        if self.dst(np.array(self.rect[0:2]), np.array([0, 580])) == 0.0:
            print("====BottomLeft")
            return True
        else:
            return False

    # ==============================
    # is the agent at bottom-right corner
    def isBottomRight(self):
        if self.dst(np.array(self.rect[0:2]), np.array([380, 580])) == 0.0:
            print("====BottomRight")
            return True
        else:
            return False

    # ==============================
    # is the agent on left edge
    def isEdgeLeft(self):
        if np.array(self.rect[0:2])[0] == 0 and \
                self.isTopLeft() is False and \
                self.isBottomLeft() is False:
            print("====EdgeLeft")
            return True
        else:
            return False

    # ==============================
    # is the agent on right edge
    def isEdgeRight(self):
        if np.array(self.rect[0:2])[0] == 380 and \
                self.isTopRight() is False and \
                self.isBottomRight() is False:
            print("====EdgeRight")
            return True
        else:
            return False

    # ==============================
    # is the agent on top edge
    def isEdgeTop(self):
        if np.array(self.rect[0:2])[1] == 0 and \
                self.isTopLeft() is False and \
                self.isTopRight() is False:
            print("====EdgeTop")
            return True
        else:
            return False

    # ==============================
    # is the agent on bottom edge
    def isEdgeBottom(self):
        if np.array(self.rect[0:2])[1] == 580 and \
                self.isBottomLeft() is False and \
                self.isBottomRight() is False:
            print("====EdgeBottom")
            return True
        else:
            return False

    # ==============================
    # move random direction
    def move2RandomDirections(self, direction1=None, direction2=None, direction3=None, direction4=None):
        # ====================================
        if direction1 is not None and direction2 is not None and direction3 is None and direction4 is None:
            print("****random move 2")
            stepX = self.stepSize * random.choice([direction1, direction2])[0]
            stepY = self.stepSize * random.choice([direction1, direction2])[1]
            self.rect.move_ip(stepX, stepY)
        # ====================================
        elif direction1 is not None and direction2 is not None and direction3 is not None and direction4 is None:
            print("****random move 3")
            stepX = self.stepSize * random.choice([direction1, direction2, direction3])[0]
            stepY = self.stepSize * random.choice([direction1, direction2, direction3])[1]
            self.rect.move_ip(stepX, stepY)
        # ====================================
        elif direction1 is not None and direction2 is not None and direction3 is not None and direction4 is not None:
            print("****random move 4")
            stepX = self.stepSize * random.choice([direction1, direction2, direction3, direction4])[0]
            stepY = self.stepSize * random.choice([direction1, direction2, direction3, direction4])[1]
            self.rect.move_ip(stepX, stepY)

        else:
            raise Exception("Wrong calling of method: move2RandomDirections")

    # ==============================
    # this function is only used inside runaway() method
    # choose a direction to move
    def move2Directions(self, chooseDir1=None, chooseDir2=None, chooseDir3=None, chooseDir4=None):
        # =======================================
        agentPosition = np.array(self.rect[0:2])
        enemyPosition = self.nearestEnemyPosition
        # ========================================
        if chooseDir1 is not None and chooseDir2 is not None and chooseDir3 is None and chooseDir4 is None:
            print("****escape move 2")

            stepX1 = self.stepSize * chooseDir1[0]
            stepY1 = self.stepSize * chooseDir1[1]
            distance1 = self.dst(enemyPosition, np.array([agentPosition[0] + stepX1,
                                                          agentPosition[1] + stepY1]))

            stepX2 = self.stepSize * chooseDir2[0]
            stepY2 = self.stepSize * chooseDir2[1]
            distance2 = self.dst(enemyPosition, np.array([agentPosition[0] + stepX2,
                                                          agentPosition[1] + stepY2]))

            if distance1 >= distance2:
                self.rect.move_ip(stepX1, stepY1)
            else:
                self.rect.move_ip(stepX2, stepY2)
        # ====================================
        elif chooseDir1 is not None and chooseDir2 is not None and chooseDir3 is not None and chooseDir4 is None:
            print("****escape move 3")

            stepX1 = self.stepSize * chooseDir1[0]
            stepY1 = self.stepSize * chooseDir1[1]
            distance1 = self.dst(enemyPosition, np.array([agentPosition[0] + stepX1,
                                                          agentPosition[1] + stepY1]))

            stepX2 = self.stepSize * chooseDir2[0]
            stepY2 = self.stepSize * chooseDir2[1]
            distance2 = self.dst(enemyPosition, np.array([agentPosition[0] + stepX2,
                                                          agentPosition[1] + stepY2]))

            stepX3 = self.stepSize * chooseDir3[0]
            stepY3 = self.stepSize * chooseDir3[1]
            distance3 = self.dst(enemyPosition, np.array([agentPosition[0] + stepX3,
                                                          agentPosition[1] + stepY3]))

            if distance1 >= distance2 and distance1 >= distance3:
                self.rect.move_ip(stepX1, stepY1)

            elif distance2 >= distance1 and distance2 >= distance3:
                self.rect.move_ip(stepX2, stepY2)

            else:
                self.rect.move_ip(stepX3, stepY3)
        # ====================================
        elif chooseDir1 is not None and chooseDir2 is not None and chooseDir3 is not None and chooseDir4 is not None:
            print("****escape move 4")
            stepX1 = self.stepSize * chooseDir1[0]
            stepY1 = self.stepSize * chooseDir1[1]
            distance1 = self.dst(enemyPosition, np.array([agentPosition[0] + stepX1,
                                                          agentPosition[1] + stepY1]))

            stepX2 = self.stepSize * chooseDir2[0]
            stepY2 = self.stepSize * chooseDir2[1]
            distance2 = self.dst(enemyPosition, np.array([agentPosition[0] + stepX2,
                                                          agentPosition[1] + stepY2]))

            stepX3 = self.stepSize * chooseDir3[0]
            stepY3 = self.stepSize * chooseDir3[1]
            distance3 = self.dst(enemyPosition, np.array([agentPosition[0] + stepX3,
                                                          agentPosition[1] + stepY3]))

            stepX4 = self.stepSize * chooseDir4[0]
            stepY4 = self.stepSize * chooseDir4[1]
            distance4 = self.dst(enemyPosition, np.array([agentPosition[0] + stepX4,
                                                          agentPosition[1] + stepY4]))

            if distance1 >= distance2 and distance1 >= distance3 and distance1 >= distance4:
                self.rect.move_ip(stepX1, stepY1)

            elif distance2 >= distance1 and distance2 >= distance3 and distance2 >= distance4:
                self.rect.move_ip(stepX2, stepY2)

            elif distance3 >= distance1 and distance3 >= distance2 and distance3 >= distance4:
                self.rect.move_ip(stepX3, stepY3)

            else:
                self.rect.move_ip(stepX4, stepY4)
        # ====================================
        else:
            raise Exception("Wrong calling of method: move2Directions")
