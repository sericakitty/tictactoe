# import document from javascript
from js import document # type: ignore

# import add_event_listener for event listener
from pyodide.ffi.wrappers import add_event_listener # type: ignore

# import asyncio library for async await
import asyncio

# import random library 
import random



# The dictionary that contains the game state.
gameState = {
        
        'init_board': True,
        
        'play': False,
        
        'mode': None,
        
        'board': None,
        
        'boardSize': None,
        'smallboard' : {
            "size": 3
        },
        'mediumboard': {
            "size": 5
        },
        'largeboard': {
            "size": 7
        },
        'tableWidth': 300,
        
        'player_one': {
            'name': 'Player one',
            'mark': None,
            'turn': False,
            'wins': 0,
            'losses': 0
            },
        
        'player_two': {
            'name': 'Player two',
            'mark': None,
            'turn': False,
            'wins': 0,
            'losses': 0
            },
        
        'ties': 0
        
    }



def initBoard(el, size):
    """
    It creates a table with the given size and adds event listeners to each cell
    
    :param el: The element that is being displayed
    :param size: The size of the board
    """
    
    if gameState['init_board']: 
        
        
        el.style.display = 'block'
        
        boardList = []
        
        table = boardTable
        
        table.style.width = f'{gameState["tableWidth"]}px'
        
        luku = 0
        indeksi = 0
        while luku < (size*size):
            boardList.append([])
            for _ in range(size):
                td = document.createElement('td')
                td.style.fontSize = f'{int(50 - 15 * (size - 3) / 2)}px'
                td.style.width = f'{gameState["tableWidth"] // size }px'
                td.style.height = f'{int(105 * ( 3 / size))}px'
                boardList[indeksi].append(td)
                luku += 1
            indeksi += 1

        for row_index in range(len(boardList)):
            tr = document.createElement('tr')
            for column_index in range(len(boardList[0])):
                td = boardList[row_index][column_index]
                
                list(map(lambda eventType: add_event_listener(td, eventType, lambda event: boxClick(event, gameState["player_one"] if gameState["player_one"]["turn"] else gameState["player_two"]) if checkMobileTouch(event) else False), ['touchstart', 'touchend']))
                add_event_listener(td, 'click', lambda event: boxClick(event, gameState["player_one"] if gameState["player_one"]["turn"] else gameState["player_two"]) if checkMouseClick(event) else False)
                
                tr.appendChild(td)
            table.appendChild(tr)
        
        
        
        boardTableMarkInfo.textContent = f'{gameState["player_one"]["name"]}: {gameState["player_one"]["mark"]}    {gameState["player_two"]["name"]}: {gameState["player_two"]["mark"]}'
        
        gameState['init_board'] = False
        gameState['board'] = boardList
        gameState['play'] = True



def getBoundArea(event):
    
    """
    This function will collect all different values from table and td elements and 
    return them so later program can calculate if mouse click or mobile touch are within box
    """
    
    rect = {}
    
    rect["td"] = event.target
    rect["tableNode"] = rect["td"].offsetParent
    rect["tableOffsetLeft"] = rect["tableNode"].offsetLeft
    rect["tableOffsetTop"] = rect["tableNode"].offsetTop 
    rect["tdLeftBorder"] = rect["td"].offsetLeft
    rect["tdRightBorder"] = rect["tdLeftBorder"] + rect["td"].offsetWidth
    rect["tdTopBorder"] = rect["td"].offsetTop
    rect["tdBottomBorder"] = rect["tdTopBorder"] + rect["td"].offsetHeight
    
    
    return rect

def checkMobileTouch(event):
    
    """
    Function will check if player touch on mobile
    """
    
    if event.type == 'touchstart':
        rect = getBoundArea(event)
        
        touch = list(event.touches)[0]
        touchX = touch.clientX - rect["tableOffsetLeft"]
        touchY = touch.clientY - rect["tableOffsetTop"]
        
        
        if rect["tdLeftBorder"] < touchX < rect["tdRightBorder"] and rect["tdTopBorder"] < touchY < rect["tdBottomBorder"]:

            return True
    else:
        return False


def checkMouseClick(event):
    """
    This function will check if player click with mouse
    """
    
    if event.type == 'click' and event.pointerType == 'mouse': 
        rect = getBoundArea(event)
        clickX = event.x - rect["tableOffsetLeft"]
        clickY = event.y - rect["tableOffsetTop"]
        
        if rect["tdLeftBorder"] < clickX < rect["tdRightBorder"] and rect["tdTopBorder"] < clickY < rect["tdBottomBorder"]:
            
            return True
    
    return False
        
    
def checkBoardSize(el):
    
    """
    This function check how big board will be printed out
    """
    
    startBoardsizeSectionDiv.style.display = 'none'
    
    boardTableTurnInfo.textContent = f'"{gameState["player_one"]["mark"] if gameState["player_one"]["turn"] else gameState["player_two"]["mark"]}" turn'
    
    size = gameState[el.value]["size"]
    
    gameState['boardSize'] = size
    
    initBoard(boardTableDiv, size)

def check_winner(player):
    
    """
    This Function will check if there's a winner after every round
    """
    
    board = gameState['board']
    size = gameState['boardSize']
    get_winner = False
    get_tie = False
        
    # check rows winner
    for row_index in range(size):
        row_list = []
        for column_index in range(size):
            row_list.append(board[row_index][column_index].textContent)
        if all(mark == player["mark"] for mark in row_list):
            get_winner = True
    
    # check columns winner
    if not get_winner:
        for column_index in range(size):
            column_list = []
            for row_index in range(size):
                column_list.append(board[row_index][column_index].textContent)
            if all(mark == player["mark"] for mark in column_list):
                get_winner = True
    
    # check diagonals winner
    if not get_winner:    
        diagonal1 = []
        diagonal2 = []
        
        for row_index in range(size):
            diagonal1.append(board[row_index][row_index].textContent)
            diagonal2.append(board[row_index][size - row_index - 1].textContent)
        
        if all(mark == player["mark"] for mark in diagonal1) or all(mark == player["mark"] for mark in diagonal2):
            get_winner = True
    
    
    if not get_winner:
        count_empty_spaces = 0
        for row_index in range(size):
            for column_index in range(size):
                if board[row_index][column_index].textContent == "":
                    count_empty_spaces += 1
        if count_empty_spaces == 0:
            get_tie = True
    
    
    
    if get_winner and player["name"] == 'Player one':
        player["wins"] += 1
        gameState["player_two"]["losses"] += 1
    
    if get_winner and player["name"] == 'Player two':
        player["wins"] += 1
        gameState["player_one"]["losses"] += 1
    
    if get_tie and not get_winner:
        gameState["ties"] += 1
        winnerInfoDiv.textContent = 'Tie'
        
    if get_winner and not get_tie:
        winnerInfoDiv.textContent = f'{player["name"]} Won!'
    
    if get_winner or get_tie:
        gameState['play'] = False
        newGameButton.style.display = 'inline-block'
        resetGameButton.style.display = 'inline-block'
        
        stats_p1.textContent = f'{gameState["player_one"]["name"]} wins: {gameState["player_one"]["wins"]}, losses: {gameState["player_one"]["losses"]}'
        stats_p2.textContent = f'{gameState["player_two"]["name"]} wins: {gameState["player_two"]["wins"]}, losses: {gameState["player_two"]["losses"]}'
        stats_p3.textContent = f'Ties: {gameState["ties"]}'
        return True
        
    # No winner found
    boardTableTurnInfo.textContent = f'"{gameState["player_one"]["mark"] if gameState["player_one"]["turn"] else gameState["player_two"]["mark"]}" turn'
    return False

def checkValidBox(event, player):
    """
    Function will check if box is empty and player's mark is eather "X" or "O" 
    """
    return event.target.textContent == "" and (player['mark'] == "X" or player['mark'] == "O")
    
def changeValue(event, mark):
    """
    Function will update mark
    """
    event.target.textContent = mark



async def boxClick(event, player): 
    """
    Function will check if play is True
    Next it will check game mode and if click is in valid box
    Finally function will check if there is a winner
    """
    
    if not gameState["play"]:
        return
    
    if gameState['mode'] == 'Human Vs Human' and checkValidBox(event, player=player):
        
        changeValue(event, player['mark'])
    
        gameState["player_one"]["turn"] = not gameState["player_one"]["turn"]
        gameState["player_two"]["turn"] = not gameState["player_two"]["turn"]

    
    await asyncio.sleep(0.01)
    
    check_winner(player)

def randomPlayerCharacters():
    """
    This function choose randomly first player's mark and how goes first
    """
    
    if gameState['mode'] != None:
        characters = ['X', 'O']
        booleans = [True, False]
        gameState['player_one']['mark'] = characters.pop(random.randint(0, len(characters) - 1))
        go_first = booleans.pop(random.randint(0, len(booleans) - 1)) 
    
    
    if gameState['mode'] == 'Human Vs Human':
        if go_first:
            gameState['player_one']['turn'] = True
            
        else:
            gameState['player_two']['turn'] = True
        
        gameState['player_two']['mark'] = characters[0]
    
    
    
    

async def modeSetter(event):
    """
    Function sets mode in gameState dict 
    Next it will invoke randomPlayerCharacters function which will generate turns and marks for players  
    """
    event.target.value = gameState['mode'] = event.target.textContent
    startModeSelectionDiv.style.display = 'none'
    startBoardsizeSectionDiv.style.display = 'block'
    await asyncio.sleep(0.01)
    randomPlayerCharacters()

def resetGame():

    """
    This function will erase statics and player can choose a new boardsize for the game
    """
    
    startModeSelectionDiv.style.display = 'block'
    
    startBoardsizeSection.selectedIndex = 0
    startBoardsizeSection.value = ""
    startBoardsizeSectionDiv.style.display = 'none'
    
    boardTableDiv.style.display = 'none'
    boardTable.innerHTML = ""
    
    stats_p1.textContent = stats_p2.textContent = stats_p3.textContent = ""
    
    winnerInfoDiv.textContent = ""
    
    newGameButton.style.display = 'none'
    resetGameButton.style.display = 'none'
    
    gameState['init_board'] = True
    
    gameState['player_one']['mark'] = None
    gameState["player_one"]["wins"] = 0
    gameState["player_one"]["losses"] = 0
    
    gameState['player_two']['mark'] = None
    gameState["player_two"]["wins"] = 0
    gameState["player_two"]["losses"] = 0
    
    gameState["ties"] = 0
    gameState['play'] = False
    gameState['board'] = None
    gameState['mode'] = None


def newGame():
    
    """
    This function will make a new game
    It will remember statics from players
    """
    
    boardTable.innerHTML = ""
    
    newGameButton.style.display = 'none'
    resetGameButton.style.display = 'none'
    
    winnerInfoDiv.textContent = ""
    gameState['init_board'] = True
    
    initBoard(boardTableDiv, gameState['boardSize'])






if __name__ == "__main__":
    
    """
    This main section contain all elements from html
    
    last four are event listeners for buttons
    
    when player has chosen boardsize, it will triggers "checkBoardSize" function and game will start
    """    
    

    startModeSelectionDiv = document.getElementById('startModeSelectionDiv')
    
    startBoardsizeSectionDiv = document.getElementById('startBoardsizeSectionDiv')
    startBoardsizeSection = document.getElementById('startBoardsizeSection')
    
    boardTableDiv = document.getElementById('boardTableDiv')
    boardTableMarkInfo, boardTableTurnInfo = boardTableDiv.querySelectorAll('p')
    boardTable = boardTableDiv.querySelector('table')
    
    staticInfoDiv = document.getElementById('staticInfoDiv')
    stats_p1, stats_p2, stats_p3 = staticInfoDiv.querySelectorAll('p')
    
    winnerInfoDiv = document.getElementById('winnerInfoDiv')
    
    newGameButton = document.getElementById('newGameButton')
    
    resetGameButton = document.getElementById('resetGameButton')
    
    
    
    add_event_listener(startModeSelectionDiv, 'click', lambda event: modeSetter(event))
    
    startBoardsizeSection.onchange = lambda event: checkBoardSize(event.target)
    
    add_event_listener(newGameButton, 'click', lambda event: newGame())
    
    
    add_event_listener(resetGameButton, 'click', lambda event: resetGame())

    