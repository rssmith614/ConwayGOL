import sys
import pygame
import pygame_gui
import gameController

# CONSTANTS:
SCREENSIZE = WIDTH, HEIGHT = 1200, 800
HOVER_COLOR = (80, 80, 80)

_VARS = {'cellMAP': 0, 'surf': False, 'gridWH': 800,
         'gridOrigin': (400, 0), 'gridCells': 0, 'lineWidth': 1,
         'gameState': 0, 'manager': False,
         'live_color': (255,255,255), 'dead_color': (0,0,0)}

_UI = {'boardSizeSelector': 0, 'livingColorSelector': 0, 'deadColorSelector': 0,
        'randButton': 0, 'startButton': 0,
        'currentPopLabel': 0, 'currentGenLabel': 0, 'currentRateLabel': 0,
        'stepButton': 0, 'clearButton': 0, 'quitButton': 0}

clock = pygame.time.Clock()

def main():
    pygame.init()
    _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)
    _VARS['manager'] = pygame_gui.UIManager(SCREENSIZE)
    _VARS['cellMAP'] = gameController.getWorld()
    _VARS['gridCells'] = _VARS['cellMAP'].shape[0]
    pygame.display.set_caption('Conway\'s Game of Life Simulator')
    initUi()
    time_delta = clock.tick(60)/1000.0
    while True:
        checkEvents()                                       # check for ui interactions and key presses
        updateUI()                                          # update displayed data
        _VARS['surf'].fill(_VARS['dead_color'])             # fill background
        placeCells()                                        # color living cells
        if _VARS['gameState'] == 0:
            glowCells()                                     # if sim is paused, interact with mouse
        if _VARS['gameState'] == 1:
            _VARS['runTime'] = gameController.iterate()     # if sim is running, iterate the simulator
        _VARS['manager'].update(time_delta) 
        _VARS['manager'].draw_ui(_VARS['surf'])
        pygame.display.update()

# make the cell under the mouse brighter
def glowCells():
    mouse = pygame.mouse.get_pos()
    # GET CELL DIMENSIONS...
    cellBorder = 0
    celldimX = celldimY = (_VARS['gridWH']/_VARS['gridCells']) - (cellBorder*2)

    # DOUBLE LOOP
    for row in range(_VARS['cellMAP'].shape[0]):
        for column in range(_VARS['cellMAP'].shape[1]):
            x = _VARS['gridOrigin'][0] + (celldimY*row) + cellBorder + (2*row*cellBorder) + _VARS['lineWidth']/2
            y = _VARS['gridOrigin'][1] + (celldimX*column) + cellBorder + (2*column*cellBorder) + _VARS['lineWidth']/2
            if x <= mouse[0] <= x + celldimX and y <= mouse[1] <= y + celldimY:               
                if _VARS['cellMAP'][column][row] == 0:
                    drawSquareCell(x, y, celldimX, celldimY, (calcHoverColor(_VARS['dead_color'][0], HOVER_COLOR[0]), calcHoverColor(_VARS['dead_color'][1], HOVER_COLOR[1]), calcHoverColor(_VARS['dead_color'][2], HOVER_COLOR[2])))
                else:
                    drawSquareCell(x, y, celldimX, celldimY, (calcHoverColor(_VARS['live_color'][0], HOVER_COLOR[0]), calcHoverColor(_VARS['live_color'][1], HOVER_COLOR[1]), calcHoverColor(_VARS['live_color'][2], HOVER_COLOR[2])))

# prevent overflow when adding hover color overlay
def calcHoverColor(base, hover):
    if base + hover > 255 or base + hover < 0:
        return base - hover
    else:
        return base + hover

# change the state of the cell being clicked
def pickCell():
    mouse = pygame.mouse.get_pos()
    # GET CELL DIMENSIONS...
    cellBorder = 0
    celldimX = celldimY = (_VARS['gridWH']/_VARS['gridCells']) - (cellBorder*2)

    # DOUBLE LOOP
    for row in range(_VARS['cellMAP'].shape[0]):
        for column in range(_VARS['cellMAP'].shape[1]):
            x = _VARS['gridOrigin'][0] + (celldimY*row) + cellBorder + (2*row*cellBorder) + _VARS['lineWidth']/2
            y = _VARS['gridOrigin'][1] + (celldimX*column) + cellBorder + (2*column*cellBorder) + _VARS['lineWidth']/2
            if x <= mouse[0] <= x + celldimX and y <= mouse[1] <= y + celldimY:
                if _VARS['cellMAP'][column][row] == 0:
                    gameController.giveLife([[column, row]])
                else:
                    gameController.kill([[column, row]])

# color living cells
def placeCells():
    # GET CELL DIMENSIONS...
    cellBorder = 0
    celldimX = celldimY = (_VARS['gridWH']/_VARS['gridCells']) - (cellBorder*2)
    # DOUBLE LOOP
    for row in range(_VARS['cellMAP'].shape[0]):
        for column in range(_VARS['cellMAP'].shape[1]):
            # Is the grid cell tiled ?
            if(_VARS['cellMAP'][column][row] == 1):
                drawSquareCell(
                    _VARS['gridOrigin'][0] + (celldimY*row)
                    + cellBorder + (2*row*cellBorder) + _VARS['lineWidth']/2,
                    _VARS['gridOrigin'][1] + (celldimX*column)
                    + cellBorder + (2*column*cellBorder) + _VARS['lineWidth']/2,
                    celldimX, celldimY, _VARS['live_color'])

# Draw filled rectangle at coordinates
def drawSquareCell(x, y, dimX, dimY, color):
    pygame.draw.rect(
     _VARS['surf'], color,
     (x, y, dimX, dimY)
    )

# define ui elements
def initUi():
    boardSizeSelector_Rect = pygame.Rect((0,0),(400,50))
    livingColorSelector_Rect = pygame.Rect((0,50),(200,50))
    deadColorSelector_Rect = pygame.Rect((200,50),(200,50))

    randButton_Rect = pygame.Rect((0,150),(400,50))
    startButton_Rect = pygame.Rect((0,200),(400,50))

    currentPopLabel_Rect = pygame.Rect((100,300),(200,50))
    currentGenLabel_Rect = pygame.Rect((100,350),(200,50))
    currentRateLabel_Rect = pygame.Rect((100,400),(200,50))

    stepButton_Rect = pygame.Rect((0,650),(400,50))
    clearButton_Rect = pygame.Rect((0,700),(400,50))
    quitButton_Rect = pygame.Rect((0,750),(400,50))

    _UI['boardSizeSelector'] = pygame_gui.elements.UIDropDownMenu(["50x50","75x75","100x100","150x150"],"75x75",boardSizeSelector_Rect,manager=_VARS['manager'])
    _UI['livingColorSelector'] = pygame_gui.elements.UIDropDownMenu(["White","Blue","Red","Green","Black"],"White",livingColorSelector_Rect,manager=_VARS['manager'])
    _UI['deadColorSelector'] = pygame_gui.elements.UIDropDownMenu(["Black","White"],"Black",deadColorSelector_Rect,manager=_VARS['manager'])

    _UI['randButton'] = pygame_gui.elements.UIButton(randButton_Rect,"Randomize",manager=_VARS['manager'])
    _UI['startButton'] = pygame_gui.elements.UIButton(startButton_Rect,"Start!",manager=_VARS['manager'])

    _UI['currentPopLabel'] = pygame_gui.elements.UILabel(currentPopLabel_Rect,"Current Population: 0",manager=_VARS['manager'])
    _UI['currentGenLabel'] = pygame_gui.elements.UILabel(currentGenLabel_Rect,"Current Generation: 0",manager=_VARS['manager'])
    _UI['currentRateLabel'] = pygame_gui.elements.UILabel(currentRateLabel_Rect,"0 iterations/s",manager=_VARS['manager'])

    _UI['stepButton'] = pygame_gui.elements.UIButton(stepButton_Rect,"Step",manager=_VARS['manager'])
    _UI['clearButton'] = pygame_gui.elements.UIButton(clearButton_Rect,"Clear",manager=_VARS['manager'])
    _UI['quitButton'] = pygame_gui.elements.UIButton(quitButton_Rect,"Quit",manager=_VARS['manager'])

# update displayed data on ui
def updateUI():
    currentPop = "Current Population: " + str(gameController.getPopulation())
    currentGen = "Current Generation: " + str(gameController.getGenNumber())
    currentRate = '%.2f' % gameController.getRunTime() + " iterations/s"

    pygame_gui.elements.UILabel.set_text(_UI['currentPopLabel'],currentPop)
    pygame_gui.elements.UILabel.set_text(_UI['currentGenLabel'],currentGen)
    pygame_gui.elements.UILabel.set_text(_UI['currentRateLabel'],currentRate)

# update background color with black/white correction
def changeDeadColor(color):
    if _VARS['live_color'] == color:
        _VARS['live_color'] = opposite(color)
    _VARS['dead_color'] = color

# update cell color with black/white correction
def changeLiveColor(color):
    if _VARS['dead_color'] == color:
        _VARS['dead_color'] = opposite(color)
    _VARS['live_color'] = color

# black/white correction
def opposite(color):
    if color == (0,0,0):
        return (255,255,255)
    else:
        return (0,0,0)

# change the size of the board and update variables accordingly
def resize(size):
    gameController.resize(size)
    _VARS['cellMAP'] = gameController.getWorld()
    _VARS['gridCells'] = _VARS['cellMAP'].shape[0]

def checkEvents(): 
    for event in pygame.event.get():
        _VARS['manager'].process_events(event)
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == _UI['quitButton'] : # quit
            pygame.quit()
            sys.exit()

        elif event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == _UI['randButton']: # randomize
            gameController.randomPop()
            _VARS['gameState'] = 0

        elif event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == _UI['startButton']: # pause/unpause
            if _VARS['gameState'] == 0:
                _VARS['gameState'] = 1
                pygame_gui.elements.UIButton.set_text(_UI['startButton'],"Stop")
            elif _VARS['gameState'] == 1:
                _VARS['gameState'] = 0
                pygame_gui.elements.UIButton.set_text(_UI['startButton'],"Resume")

        elif event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == _UI['stepButton']: # step (perform one iteration)
            gameController.iterate()

        elif event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == _UI['clearButton']: # clear (kill all cells)
            gameController.genocide()
            _VARS['gameState'] = 0

        elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED and event.ui_element == _UI['boardSizeSelector']: # change board size
            _VARS['gameState'] = 0
            if event.text == "50x50":
                resize(50)
            elif event.text == "75x75":
                resize(75)
            elif event.text == "100x100":
                resize(100)
            elif event.text == "150x150":
                resize(150)
            pygame_gui.elements.UIButton.set_text(_UI['startButton'],"Start!")
            gameController.randomPop()

        elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED and event.ui_element == _UI['deadColorSelector']: # change background color
            if event.text == 'Black':
                changeDeadColor((0,0,0))
            elif event.text == 'White':
                changeDeadColor((255,255,255))

        elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED and event.ui_element == _UI['livingColorSelector']: # change living cell color
            if event.text == 'Black':
                changeLiveColor((0,0,0))
            elif event.text == 'White':
                changeLiveColor((255,255,255))
            elif event.text == 'Blue':
                changeLiveColor((0,0,255))
            elif event.text == 'Red':
                changeLiveColor((255,0,0))
            elif event.text == 'Green':
                changeLiveColor((0,255,0))

        elif event.type == pygame.MOUSEBUTTONDOWN and _VARS['gameState'] == 0: # place cells by hand
            pickCell()

if __name__ == '__main__':
    main()