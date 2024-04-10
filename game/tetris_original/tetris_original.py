import random as rd

def update_board(board): # 현재 보드판의 상태 출력
    for i in board:
        print(i)

board = [[0 for i in range(10)] for j in range(20)] # 10 X 20 이중 리스트의 보드판 생성
blocks = [ [[1, 1], [1, 1]], [[1, 1, 1, 1]], [[0, 1, 1], [1, 1, 0]], [[1, 1, 0], [0, 1, 1]] ] # 랜덤으로 생성할 블록
randomBlock = rd.choice(blocks) # 블록 랜덤 초이스

update_board(board) # 보드판 상태 업데이트

# 생성한 블록을 꼭대기 가운데에 배치
def spawn_block():
    for i in range(len(randomBlock)): # 블록의 위아래 높이 만큼 반복합니다.
        blockLen = len(randomBlock[i]) # 블록의 길이
        place = int((len(board[0])-blockLen) / 2) # 배치할 위치를 정합니다.
        for j in range(len(randomBlock[i])): # 블록의 첫줄부터 1을 찾습니다.
            if randomBlock[i][j] == 1:  # 블록의 해당 위치가 1인지
                board[i][j+place] = 1  # 보드에서 배치할 위치에 1로 채웁니다.

spawn_block()
update_board(board)

def move_down(): # 블록이 한 칸 아래로 움직입니다.
    for i in range(len(board)-2, -1, -1): # 보드의 리스트를 역순으로 아래에서 위로 참조 합니다.
        for j in range(len(board[i])): # 맨 아랫줄 부터 시작
            if board[i][j] == 1 and board[i+1][j] == 0: # 특정 칸에 1이 있으면 바로 아랫줄 같은 칸이 0인지
                board[i+1][j] = 1 # 바로 아랫줄 칸을 1로 바꾸고
                board[i][j] = 0 # 현재 칸은 0으로 바꿉니다.
            elif board[i][j] == board[i+1][j] == 1: # 블록이 더이상 아래로 내려갈 수 없을때
                board[i][j], board[i+1][j] = 7, 7 # 둘 다 1이면 숫자를 7로 변경합니다. 숫자 7은 사용자의 입력을 무시하기 위한 목적입니다.

move_down()
update_board(board)

def input_move_key():
    moveKey = input("이동할 방향 입력(a, s, d): ") # 좌우, 아래 키 입력 가능
    
    if moveKey == "a": # 왼쪽으로 한 칸 이동합니다.
        for i in range(len(board)-1, -1, -1):
            for j in range(1, len(board[i])): # 리스트 행의 오른쪽에서 왼쪽으로 역순으로 참조합니다.
                if board[i][j] == 1 and board[i][j-1] == 0: # 특정 칸에 1이 있고 바로 왼쪽 칸이 0인지
                    board[i][j-1] = 1 # 왼쪽 칸을 1로 바꾸고
                    board[i][j] = 0 # 현재 칸을 0으로 바꿉니다.
    elif moveKey == "d": # 오른쪽으로 한 칸 이동합니다.
        for i in range(len(board)-1, -1, -1):
            for j in range(len(board[i])-2, -1, -1): # 리스트 행의 왼쪽에서 오른쪽으로 역순으로 참조합니다.
                if board[i][j] == 1 and board[i][j+1] == 0: # 특정 칸에 1이 있고 바로 오른쪽 칸이 0인지
                    board[i][j+1] = 1 # 오른쪽 칸을 1로 바꾸고
                    board[i][j] = 0 # 현재 칸을 0으로 바꿉니다.
    elif moveKey == "s": # move_down() 함수를 호출해 아래로 한 칸 이동합니다.
        move_down()

input_move_key()
update_board(board)

def break_block(): # 숫자 7이 모두 채워진 행들을 0으로 초기화 하는 함수입니다.
    breakCount = 0 # 7로 채워진 행의 개수 입니다. 개수만큼 move_down() 함수를 호출해 부숴진 라인 위에 블록들을 내려오게 할 목적입니다.
    for i, v in enumerate(board):
        if sum(v) == 70: # 행의 요소들이 모두 7로 이루어져있다면 총합이 70일 것입니다.
            board[i] = [0 for j in range(10)] # 조건에 만족하는 행을 0으로 채워 초기화 합니다.
            breakCount += 1 # 초기화 횟수를 기록합니다.
    for k in range(len(board)): # 그러나 숫자 7은 이동을 무시하는 블록입니다.
        for l in range(len(board[k])): # 위에서 초기화 작업이 끝났다면 숫자 7을 모두 1로 바꿉니다.
            if board[k][l] == 7:
                board[k][l] = 1
    for m in range(breakCount+1): # 마지막으로 초기화한 수 만큼 move_down()을 호출할건데
        move_down()               # move_down() 함수는 블록이 바닥을 통과하려고 시도할때 1숫자 블록들을 7로 바꿔주기 때문에
                                  # +1을 하여 한 번 더 호출합니다.
break_block()
update_board(board)