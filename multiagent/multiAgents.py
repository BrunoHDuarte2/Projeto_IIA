# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState
import math

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        print("---------------------------")
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        print("Ações possíveis: ", legalMoves)
        print("Scores: ", scores )
        print("Ação feita: ",legalMoves[chosenIndex])
        print("---------------------------")
        "Add more of your code here if you want to"
        
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Comida
        if action == "Stop":
            score = float("-inf")
            return score
        mapaComida = currentGameState.getFood()
        comidas = []
        for x, linha in enumerate(mapaComida):
            for y, boolean in enumerate(linha):
                if boolean == True:
                    comidas.append((x, y))
        pacman_x, pacman_y = currentGameState.getPacmanPosition()
        listaDistanciaComida = [math.sqrt(((x-pacman_x)**2+(y-(pacman_y+1))**2)) for (x, y) in comidas]
        menorDistanciaComida = min(listaDistanciaComida)
        index = listaDistanciaComida.index(menorDistanciaComida)
        food_x, food_y = comidas[index]
        print("Pacman X Comida", ((pacman_x, pacman_y),(food_x, food_y)))
        # Qual ação minimiza a distância entre o pacman e a comida
        
        if action == "North":
            proxDistance = math.sqrt(((food_x-pacman_x)**2+(food_y-(pacman_y+1))**2))
        if action == "South":
            proxDistance = math.sqrt(((food_x-pacman_x)**2+(food_y-(pacman_y-1))**2))   
        if action == "West":
            proxDistance = math.sqrt(((food_x-(pacman_x-1))**2+(food_y-pacman_y)**2)) 
        if action == "East":
            proxDistance = math.sqrt(((food_x-(pacman_x+1))**2+(food_y-pacman_y)**2)) 
        if proxDistance<menorDistanciaComida:
            menorDistanciaComida = proxDistance
        print("----------------")
        # Evitando fantasmas!
        # Distância entre o fantasma e o pacman
        ghostPos = currentGameState.getGhostPositions()
        distGhosts = [math.sqrt(((x-pacman_x)**2+(y-pacman_y)**2)) for (x, y) in ghostPos]
        distanciaGhostMaisPerto = min(distGhosts)
        emergencia = 1
        print("Distancia pacman e fantasma: ", distanciaGhostMaisPerto)
        print("Distancia comida: ", menorDistanciaComida)
        if any(d <= 4 for d in distGhosts):
            # Minimizar a distância entre o PacMan e o fantasma
            if action == "North":
                proxDistance = min([math.sqrt(((x-pacman_x)**2+(y-(pacman_y+1))**2)) for (x, y) in ghostPos])         
            if action == "South":
                proxDistance = min([math.sqrt(((x-pacman_x)**2+(y-(pacman_y-1))**2)) for (x, y) in ghostPos])
            if action == "West":
                proxDistance = min([math.sqrt(((x-(pacman_x-1))**2+(y-pacman_y)**2)) for (x, y) in ghostPos])
            if action == "East":
                proxDistance = min([math.sqrt(((x-(pacman_x+1))**2+(y-pacman_y)**2)) for (x, y) in ghostPos])
            if distanciaGhostMaisPerto<proxDistance:
                distanciaGhostMaisPerto = proxDistance
            if distanciaGhostMaisPerto<=2:
                emergencia = 10
            score = distanciaGhostMaisPerto*emergencia
        else:
            score = menorDistanciaComida*(-1)
        
        print("Score: ",score)
        print("Ação Associada: ", action)
        return score

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
