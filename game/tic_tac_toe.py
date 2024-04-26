import random as rd

board = [["👀" for i in range(3)] for j in range(3)]
placeDict = {1:(0, 0), 2:(0, 1), 3:(0, 2),
             4:(1, 0), 5:(1, 1), 6:(1, 2),
             7:(2, 0), 8:(2, 1), 9:(2, 2)}

def update_board(board):
    print("\n")
    for i in board:
        print(i)

def check_winner(emoji):
    for i in range(3):
        if emoji == board[i][0] == board[i][1] == board[i][2]:
            return True
        elif emoji == board[0][i] == board[1][i] == board[2][i]:
            return True
        elif emoji == board[0][0] == board[1][1] == board[2][2]:
            return True
        elif emoji == board[0][2] == board[1][1] == board[2][0]:
            return True

def user_turn():
    while True:
        userChoice = int(input("자리 입력(1~9): "))
        userChoice = placeDict[userChoice]
        if board[userChoice[0]][userChoice[1]] == "👀":
            board[userChoice[0]][userChoice[1]] = "🙂"
        else:
            print("선택할 수 없는 자리")
            continue
        break
    if check_winner("🙂"):
        update_board(board)
        print("Winner: 🙂")
        return
    else:
        cpu_turn()

def cpu_turn():
    cpuChoice = []
    for i in range(len(board)):
        for j, v in enumerate(board):
            if v[i] == "👀":
                cpuChoice.append((j, i))
    
    randomChoice = rd.choice(cpuChoice)
    board[randomChoice[0]][randomChoice[1]] = "🤖"
    update_board(board)
    if check_winner("🤖"):
        print("Winner: 🤖")
        return
    else:
        user_turn()

update_board(board)
user_turn()