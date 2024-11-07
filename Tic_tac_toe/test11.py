import tkinter as tk
from tkinter import messagebox

def clickButton(position):
    if board[position] == ' ':
        board[position] = player
        updateButton(position)
        if checkForWin():
            messagebox.showinfo("Game Over", "Player wins!")
            resetGame()
        elif checkDraw():
            messagebox.showinfo("Game Over", "It's a draw!")
            resetGame()
        else:
            compMove()
def checkForWin():
    if (board[1] == board[2] and board[1] == board[3] and board[1] != ' '):
        return True
    elif (board[4] == board[5] and board[4] == board[6] and board[4] != ' '):
        return True
    elif (board[7] == board[8] and board[7] == board[9] and board[7] != ' '):
        return True
    elif (board[1] == board[4] and board[1] == board[7] and board[1] != ' '):
        return True
    elif (board[2] == board[5] and board[2] == board[8] and board[2] != ' '):
        return True
    elif (board[3] == board[6] and board[3] == board[9] and board[3] != ' '):
        return True
    elif (board[1] == board[5] and board[1] == board[9] and board[1] != ' '):
        return True
    elif (board[7] == board[5] and board[7] == board[3] and board[7] != ' '):
        return True
    else:
        return False

def checkDraw():
    for key in board.keys():
        if (board[key] == ' '):
            return False
    return True

def updateButton(position):
    buttons[position].config(text=board[position])

def resetGame():
    global board
    board = {i: ' ' for i in range(1, 10)}
    for i in range(1, 10):
        updateButton(i)
        
def checkWhichMarkWon(mark):
    if board[1] == board[2] and board[1] == board[3] and board[1] == mark:
        return True
    elif (board[4] == board[5] and board[4] == board[6] and board[4] == mark):
        return True
    elif (board[7] == board[8] and board[7] == board[9] and board[7] == mark):
        return True
    elif (board[1] == board[4] and board[1] == board[7] and board[1] == mark):
        return True
    elif (board[2] == board[5] and board[2] == board[8] and board[2] == mark):
        return True
    elif (board[3] == board[6] and board[3] == board[9] and board[3] == mark):
        return True
    elif (board[1] == board[5] and board[1] == board[9] and board[1] == mark):
        return True
    elif (board[7] == board[5] and board[7] == board[3] and board[7] == mark):
        return True
    else:
        return False


def minimax(board, depth, isMaximizing):
    if (checkWhichMarkWon(bot)):
        return 1
    elif (checkWhichMarkWon(player)):
        return -1
    elif (checkDraw()):
        return 0

    if (isMaximizing):
        bestScore = -800
        for key in board.keys():
            if (board[key] == ' '):
                board[key] = bot
                score = minimax(board, depth + 1, False)
                board[key] = ' '
                if (score > bestScore):
                    bestScore = score
        return bestScore

    else:
        bestScore = 800
        for key in board.keys():
            if (board[key] == ' '):
                board[key] = player
                score = minimax(board, depth + 1, True)
                board[key] = ' '
                if (score < bestScore):
                    bestScore = score
        return bestScore


def compMove():
    bestScore = -800
    bestMove = 0
    for key in board.keys():
        if board[key] == ' ':
            board[key] = bot
            score = minimax(board, 0, False)
            board[key] = ' '
            if score > bestScore:
                bestScore = score
                bestMove = key
    board[bestMove] = bot
    updateButton(bestMove)
    if checkForWin():
        messagebox.showinfo("Game Over", "Bot wins!")
        resetGame()
    elif checkDraw():
        messagebox.showinfo("Game Over", "It's a draw!")
        resetGame()

# Create the main window
root = tk.Tk()
root.title("Tic Tac Toe")

# Create buttons for the Tic Tac Toe grid
buttons = {}
for i in range(1, 10):
    row = (i-1) // 3
    col = (i-1) % 3
    action = lambda x=i: clickButton(x)
    button = tk.Button(root, text=' ', font=('normal', 20), height=3, width=6,
                       command=action)
    button.grid(row=row, column=col)
    buttons[i] = button

# Initialize board and players
board = {i: ' ' for i in range(1, 10)}
player = 'O'
bot = 'X'

# Run the main event loop
root.mainloop()
