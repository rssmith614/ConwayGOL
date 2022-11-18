import random as rand
import numpy as np
import time
from scipy import signal

_VARS = {'size': 75, 'genNumber': 0, 'runTime': 0., 'numLiving': 0, 'algSwitchThreshold': 0.3}

_MAPS = {'world': 0, 'neighborMap': 0, 
    'L': np.empty(shape=(0,2), dtype=np.int8), 
    'D': np.empty(shape=(0,2), dtype=np.int8),
    'kernel': np.array([[1,1,1],[1,0,1],[1,1,1]])}

_MAPS['world'] = np.zeros(shape=(_VARS['size'], _VARS['size']), dtype=np.int8)

_MAPS['neighborMap'] = np.zeros(shape=(_VARS['size'], _VARS['size']), dtype=np.int8)

# randomly populate the world
def randomPop():
    _VARS['genNumber'] = 0
    for r in range(0, _VARS['size']):
        for c in range(0, _VARS['size']):
            _MAPS['world'][r][c] = rand.randint(0,1)
            _VARS['numLiving'] += _MAPS['world'][r][c]
    checkAll()

# burn the world
def genocide():
    for r in range(0, _VARS['size']):
        for c in range(0, _VARS['size']):
            _MAPS['world'][r][c] = 0
            _MAPS['neighborMap'][r][c] = 0
    _VARS['genNumber'] = 0
    _VARS['numLiving'] = 0

# change the size of the world
def resize(n):
    _VARS['size'] = n

    _MAPS['world'] = np.zeros(shape=(_VARS['size'], _VARS['size']), dtype=np.int8)

    _MAPS['neighborMap'] = np.zeros(shape=(_VARS['size'], _VARS['size']), dtype=np.int8)

def printArr():
    for r in _MAPS['world']:
        for c in r:
            print(c,end = " ")
        print()

def findLiving():
    # return the set of coordinates of every living cell
    return np.asarray(np.where(_MAPS['world'] == 1)).T

def findDead():
    # return the set of coordinates of every dead cell
    return np.asarray(np.where(_MAPS['world'] == 0)).T

def checkAll():
    _MAPS['neighborMap'] = signal.convolve2d(_MAPS['world'], _MAPS['kernel'], mode='same', boundary='fill')

def checkLiving(L):
    livingMarked = np.zeros(shape=(0, 2), dtype=np.int8)    # empty set

    for cell in L:
        if _MAPS['neighborMap'][cell[0]][cell[1]] > 3 or _MAPS['neighborMap'][cell[0]][cell[1]] <= 1:
            livingMarked = np.append(livingMarked, cell)    # if a living cell has fewer than 2 neighbors or more than 3, mark it

    # format the output as a set of tuples
    markedSize = int(livingMarked.size / 2)
    livingMarked = np.reshape(livingMarked, (markedSize, 2))
    return livingMarked

def checkDead(D):
    deadMarked = np.zeros(shape=(0,2), dtype=np.int8)  # empty set

    for cell in D:
        if _MAPS['neighborMap'][cell[0]][cell[1]] == 3:
            deadMarked = np.append(deadMarked, cell)    # if a dead cell has 3 neighbors, mark it

    # format the output as a set of tuples
    markedSize = int(deadMarked.size / 2)
    deadMarked = np.reshape(deadMarked, (markedSize, 2))
    return deadMarked

def kill(marked):
    for cell in marked:
        _MAPS['world'][cell[0]][cell[1]] = 0    # kill cell
        _VARS['numLiving'] -= 1

def giveLife(marked):
    for cell in marked:
        _MAPS['world'][cell[0]][cell[1]] = 1    # bring cell to life
        _VARS['numLiving'] += 1

def iterate():
    startTime = time.perf_counter()             # keep track of runtime

    checkAll()

    _MAPS['L'] = findLiving()                   # find every living cell
    livingMarked = checkLiving(_MAPS['L'])      # decide which living cells should die

    _MAPS['D'] = findDead()                     # find every dead cell
    deadMarked = checkDead(_MAPS['D'])          # decide which dead cells should come to life

    kill(livingMarked)                          # kill cells that should die
    giveLife(deadMarked)                        # bring cells to life

    _VARS['genNumber'] += 1                     # increment generation number
    totalTime = time.perf_counter() - startTime # determine runtime
    _VARS['runTime'] = totalTime**(-1)          # determine runtime

def getWorld():
    return _MAPS['world']

def getPopulation():
    return _VARS['numLiving']

def getRunTime():
    return _VARS['runTime']

def getGenNumber():
    return _VARS['genNumber']