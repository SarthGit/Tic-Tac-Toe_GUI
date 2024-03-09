from tkinter import *
import random

root = Tk()
root.geometry("1200x700")
root.title("Tic Tac Toe GUI")
root.resizable(0, 0)

frame1 = Frame(root)
frame1.pack()
titleLabel = Label(frame1, text="Tic Tac Toe", font=("Arial", 25), bg="white", width=20)
titleLabel.grid(row=0, column=0)

optionFrame = Frame(root, bg="grey")
optionFrame.pack()

frame2 = Frame(root, bg="yellow")
frame2.pack()

board = {1: " ", 2: " ", 3: " ",
         4: " ", 5: " ", 6: " ",
         7: " ", 8: " ", 9: " "}

turn = "x"
game_end = False
mode = "singlePlayer"
difficulty = "easy"
player1_name = ""
player2_name = ""

def changeModeToSinglePlayer():
    global mode
    mode = "singlePlayer"
    singlePlayerButton["bg"] = "lightgreen"
    multiPlayerButton["bg"] = "lightgrey"
    showDifficultyLevels()

def changeModeToMultiplayer():
    global mode
    mode = "multiPlayer"
    hideDifficultyLevels()
    multiPlayerButton["bg"] = "lightgreen"
    singlePlayerButton["bg"] = "lightgrey"

def changeDifficultyToEasy():
    global difficulty
    difficulty = "easy"
    hideDifficultyLevels()
    easyButton["bg"] = "lightgreen"
    mediumButton["bg"] = "lightgrey"
    hardButton["bg"] = "lightgrey"

def changeDifficultyToMedium():
    global difficulty
    difficulty = "medium"
    hideDifficultyLevels()
    easyButton["bg"] = "lightgrey"
    mediumButton["bg"] = "lightgreen"
    hardButton["bg"] = "lightgrey"

def changeDifficultyToHard():
    global difficulty
    difficulty = "hard"
    hideDifficultyLevels()
    easyButton["bg"] = "lightgrey"
    mediumButton["bg"] = "lightgrey"
    hardButton["bg"] = "lightgreen"

def updateBoard():
    for key in board.keys():
        buttons[key - 1]["text"] = board[key]

def checkForWin(player):
    # Check rows, columns, and diagonals for winning condition
    for i in range(3):
        if all(board[j] == player for j in range(1 + i * 3, 4 + i * 3)) or \
                all(board[j] == player for j in range(1 + i, 8 + i, 3)):
            return True
    if board[1] == board[5] == board[9] == player or board[3] == board[5] == board[7] == player:
        return True
    return False

def checkForDraw():
    return " " not in board.values()

def restartGame():
    global game_end
    game_end = False
    for button in buttons:
        button["text"] = " "

    for i in board.keys():
        board[i] = " "

    titleLabel.config(text="Tic Tac Toe")

def playComputer():
    if difficulty == "easy":
        available_moves = [key for key, value in board.items() if value == " "]
        if available_moves:
            move = random.choice(available_moves)
            board[move] = "o"
            updateBoard()
    elif difficulty == "medium":
        # Blocking player's winning moves occasionally
        if random.random() > 0.3:
            playComputer()
        else:
            available_moves = [key for key, value in board.items() if value == " "]
            if available_moves:
                move = random.choice(available_moves)
                board[move] = "o"
                updateBoard()
    elif difficulty == "hard":
        best_score = -float('inf')
        best_move = None
        for move in board.keys():
            if board[move] == " ":
                board[move] = "o"
                score = minimax(board, False)
                board[move] = " "
                if score > best_score:
                    best_score = score
                    best_move = move
        board[best_move] = "o"
        updateBoard()

def minimax(board, is_maximizing):
    if checkForWin("o"):
        return 1
    elif checkForWin("x"):
        return -1
    elif checkForDraw():
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for move in board.keys():
            if board[move] == " ":
                board[move] = "o"
                score = minimax(board, False)
                board[move] = " "
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = float('inf')
        for move in board.keys():
            if board[move] == " ":
                board[move] = "x"
                score = minimax(board, True)
                board[move] = " "
                best_score = min(best_score, score)
        return best_score

def play(event):
    global turn, game_end
    if game_end:
        return

    button = event.widget
    buttonText = str(button)
    clicked = buttonText[-1]
    if clicked=="n":
        clicked=1
    else:
        clicked=int(clicked)

    if button["text"] == " ":
        board[clicked] = turn
        updateBoard()
        if checkForWin(turn):
            if mode == "multiPlayer":
                if turn == "x":
                    titleLabel.config(text=f"{player1_name} wins the game")
                else:
                    titleLabel.config(text=f"{player2_name} wins the game")
            else:
                if turn == "x":
                    titleLabel.config(text=f"{player1_name} wins the game")
                else:
                    titleLabel.config(text="Computer wins the game")
            game_end = True
        elif checkForDraw():
            titleLabel.config(text="Game Draw")
            game_end = True
        else:
            if turn == "x":
                turn = "o"
                if mode == "singlePlayer":
                    playComputer()
                    if checkForWin("o"):
                        titleLabel.config(text="Computer wins the game")
                        game_end = True
                    elif checkForDraw():
                        titleLabel.config(text="Game Draw")
                        game_end = True
                    turn = "x"
            else:
                turn = "x"

def showDifficultyLevels():
    easyButton.grid(row=1, column=0)
    mediumButton.grid(row=1, column=1)
    hardButton.grid(row=1, column=2)

def hideDifficultyLevels():
    easyButton.grid_forget()
    mediumButton.grid_forget()
    hardButton.grid_forget()

def getPlayerNames():
    global player1_name, player2_name
    player1_name = player1Entry.get()
    player2_name = player2Entry.get()

# Change Mode options
singlePlayerButton = Button(optionFrame, text="SinglePlayer", width=13, height=1, font=("Arial", 15),
                            bg="lightgrey", relief=RAISED, borderwidth=5, command=changeModeToSinglePlayer)
singlePlayerButton.grid(row=0, column=0, columnspan=1, sticky=NW)

multiPlayerButton = Button(optionFrame, text="Multiplayer", width=13, height=1, font=("Arial", 15),
                           bg="lightgrey", relief=RAISED, borderwidth=5, command=changeModeToMultiplayer)
multiPlayerButton.grid(row=0, column=1, columnspan=1, sticky=NW)

# Difficulty levels
easyButton = Button(optionFrame, text="Easy", width=8, height=1, font=("Arial", 15), bg="lightgreen",
                    relief=RAISED, borderwidth=5, command=changeDifficultyToEasy)
mediumButton = Button(optionFrame, text="Medium", width=8, height=1, font=("Arial", 15), bg="lightgrey",
                      relief=RAISED, borderwidth=5, command=changeDifficultyToMedium)
hardButton = Button(optionFrame, text="Hard", width=8, height=1, font=("Arial", 15), bg="lightgrey",
                    relief=RAISED, borderwidth=5, command=changeDifficultyToHard)

# Tic Tac Toe Board
buttons = []
for i in range(3):
    for j in range(3):
        btn = Button(frame2, text=" ", width=4, height=2, font=("Arial", 30), bg="yellow",
                     relief=RAISED, borderwidth=5)
        btn.grid(row=i, column=j)
        btn.bind("<Button-1>", play)
        buttons.append(btn)

restartButton = Button(frame2, text="Restart Game", width=19, height=1, font=("Arial", 20), bg="Green",
                       relief=RAISED, borderwidth=5, command=restartGame)
restartButton.grid(row=3, column=0, columnspan=3)

# Entry widgets for player names
player1Label = Label(optionFrame, text="Player 1 Name:", font=("Arial", 15), bg="grey")
player1Label.grid(row=2, column=0, sticky=E)

player1Entry = Entry(optionFrame, font=("Arial", 15))
player1Entry.grid(row=2, column=1, sticky=W)

player2Label = Label(optionFrame, text="Player 2 Name:", font=("Arial", 15), bg="grey")
player2Label.grid(row=3, column=0, sticky=E)

player2Entry = Entry(optionFrame, font=("Arial", 15))
player2Entry.grid(row=3, column=1, sticky=W)

startGameButton = Button(optionFrame, text="Start Game", width=10, height=1, font=("Arial", 15),
                         bg="lightgrey", relief=RAISED, borderwidth=5, command=getPlayerNames)
startGameButton.grid(row=4, column=0, columnspan=2)

root.mainloop()
