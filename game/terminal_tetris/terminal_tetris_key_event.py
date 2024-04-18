import random as rd # 블록을 랜덤으로 뽑기 위해서 사용하는 모듈
import keyboard
import time
import os

background = "⚫" # 배경 타일
board = [[background for i in range(10)] for j in range(21)] # 10 X 21 보드판 생성
blockPos = [] # 블록의 각 픽셀이 위치하는 행과 열의 번호
orgBlockPos = [] # 블록을 원점에 배치했을 때 각 픽셀이 위치하는 행과 열의 번호
rotateCenterPos = () # 블록의 회전 중심이 되는 행과 열의 번호
blocks = [
    [["🤖", "🤖"], # 정사각형 블록
     ["🤖", "🤖"]],
    
    [["🛸", "🛸", "🛸", "🛸"]], # 일자 블록
    
    [["👽", "👽", "⚫"], # Z블록
     ["⚫", "👽", "👽"]],
    
    [["⚫", "👾", "👾"], # Z블록 반전
     ["👾", "👾", "⚫"]],
    
    [["🤔", "⚫", "⚫"], # ㄴ자 블록
     ["🤔", "🤔", "🤔"]],
    
    [["⚫", "⚫", "🔫"], # ㄴ자 블록 반전
     ["🔫", "🔫", "🔫"]],

    [["⚫", "👻", "⚫"], # ㅗ자 블록
     ["👻", "👻", "👻"]]
    ]
randomArrange = [] # 7개 블록 순서 랜덤 배열
score = 0 # 점수
gameOver = False
key_left = False
key_right = False
key_down = False
key_space = False
key_z = False
reset = False
pause = False
Request_for_update = False
send_input_event = False
input_processing = False

def update_board(): # 현재 보드판의 상태 출력
    print("Score: %d" % (score))
    for i in board[1:]:
        print(*i)

def spawn_block():
    if board[0].count(background) == 10: # 블록이 쌓인 칸 수가 20을 초과하지 않았으면
        global blockPos
        global orgBlockPos
        global rotateCenterPos
        blockPos = []
        orgBlockPos = []
        if not randomArrange:
            while len(randomArrange) < 7:
                randomBlock = rd.choice(blocks) # 블록 랜덤 선택
                if randomBlock not in randomArrange:
                    randomArrange.append(randomBlock)
        currentBlock = randomArrange[0]
        blockLen = len(currentBlock) # 블록의 행 길이
        randomArrange.remove(randomArrange[0])
        place = int((len(board[0])-blockLen) / 2) # (보드의 행 길이 - 블록의 행 길이) / 2
        prlDisplace = () # 평행이동 수치
        for i in range(len(currentBlock)): # 블록의 행 조회
            for j in range(len(currentBlock[i])): # 블록의 열 조회
                if currentBlock[i][j] != background:
                    board[i][j+place] = currentBlock[i][j] # 블록의 각 행을 보드판 위쪽 가운데에 배치
                    blockPos.append((i, j+place)) # 배치된 행과 열의 번호를 blockPos에 저장
                    orgBlockPos.append((i, j)) # 원점에 배치했을 때 행과 열의 번호를 orgBlockPos에 저장
                    if i == len(currentBlock) // 2 and j == len(currentBlock[0]) // 2:
                        rotateCenterPos = (i, j+place) # 블록의 행의 중심, 열의 중심 위치
                        prlDisplace = (i, j) # 블록의 첫번째 행의 첫번째 열의 위치와 rotateCenterPos의 거리 차이
        for i, pos in enumerate(orgBlockPos):
            orgBlockPos[i] = (pos[0] - prlDisplace[0], pos[1] - prlDisplace[1]) # 블록을 원점에 배치했을 때, prlDisplace 만큼 평행이동하여
                                                                                # 블록의 회전중심이 원점에 배치되도록 설정
    else:
        global gameOver
        gameOver = True

def move_down_block(moveKeyX=False):
    global blockPos
    global rotateCenterPos
    while True:
        movable = True
        for i in range(len(board)-1, -1, -1): # 행 조회(아래에서 위로 역순)
            for j in range(len(board[i])): # 열 조회
                if (i, j) in blockPos: # blockPos가 갖고 있는 행과 열의 번호이면
                    if i != len(board)-1: # 가장 아래쪽 칸이 아니면
                        if board[i+1][j] != background: # 아래 칸이 배경 타일이 아니면
                            if (i+1, j) not in blockPos: # 아래 칸이 blockPos가 갖고 있지 않은 행과 열의 번호이면
                                movable = False # 이동 불가로 변경하고 열 조회 중지
                                break
                    else: # 가장 아래쪽 칸이면
                        movable = False
                        break
            if not movable: # 이동 불가 상태이면 행 조회도 중지
                break
        if movable: # 이동 가능 상태가 유지 되었으면
            rotateCenterPos = (rotateCenterPos[0]+1, rotateCenterPos[1]) # 회전 중심의 행 번호 +1
            blockPos.reverse() # blockPos의 배열을 역순으로 변경
            for i, pos in enumerate(blockPos): # 블록의 행, 열 조회
                board[pos[0]+1][pos[1]] = board[pos[0]][pos[1]] # 픽셀을 아래쪽으로 한 칸 이동
                board[pos[0]][pos[1]] = background
                blockPos[i] = (pos[0]+1, pos[1]) # blockPos의 행과 열의 번호를 수정
            blockPos.reverse() # 배열을 역순에서 원래대로 변경
            if not moveKeyX: # 사용자가 x키를 누르지 않았으면 break
                break
        else: # 이동 불가 상태이면 break
            reset_line() # reset_line 함수를 호출하여 값이 모두 채워진 행이 있는지 검사
            break

def input_move_key(key):
    if not input_processing:
        global pause
        if not pause and key.name == "left":
            global key_left
            key_left = True
        elif not pause and key.name == "right":
            global key_right
            key_right = True
        elif not pause and key.name == "down":
            global key_down
            key_down = True
        elif not pause and key.name == "space":
            global key_space
            key_space = True
        elif not pause and key.name == "z":
            global key_z
            key_z = True
        elif key.name == "q":
            global gameOver
            gameOver = True
        elif key.name == "r":
            global reset
            reset = True
        elif key.name == "p":
            pause = not pause
        
        global send_input_event
        send_input_event = True

def rotate_block():
    rotatedblockPos = [] # 블록 회전 결과
    for pos in orgBlockPos: # 원점 배열 조회
        rotateRow = pos[1] + rotateCenterPos[0] # 회전했을 때 행 번호
        rotateCol = -pos[0] + rotateCenterPos[1] # 회전했을 때 열 번호
        if 0 <= rotateRow <= len(board)-1 and 0 <= rotateCol <= len(board[0])-1: # 행, 열 번호가 보드판을 벗어나지 않으면
            if board[rotateRow][rotateCol] != background: # 회전 했을때 위치의 값이 배경 타일이 아니면
                if (rotateRow, rotateCol) not in blockPos: # 행, 열 번호가 blockPos에 없으면
                    rotatedblockPos = [] # 리스트를 비우고 중지
                    break
            rotatedblockPos.append((rotateRow, rotateCol)) # break가 안 걸렸으면 행, 열 번호 추가
        else: # 벗어나면
            rotatedblockPos = [] # 리스트를 비우고 중지
            break
    return rotatedblockPos # 결과 반환

def reset_line():
    resetCount = 0 # 행 초기화 횟수
    for i in range(1, len(board)): # 두번째 행 ~ 마지막 행까지 조회
        if background not in board[i]: # 행 안에 값이 모두 채워져 있으면
            board[i] = [background for i in range(10)] # 행의 모든 값을 배경 타일로 초기화
            resetCount += 1 # 행 초기화 횟수 추가
    if resetCount: # 행 초기화 작업이 이루어 졌다면
        global score
        score += resetCount*100
        move_down_line(resetCount) # 모든 행들을 아래로 밀착 시키기 위해 move_down_line 함수에 resetCount만큼 값을 전달하여 호출
    spawn_block() # 밀착이 끝났다면 spawn_block 함수를 호출해 랜덤 블록 생성

def move_down_line(repeat):
    while repeat: # reset_line 함수에서 행 초기화 횟수만큼 수행
        for i in range(len(board)-1, 1, -1): # 행 조회(아래에서 위로 세번째 행 까지 역순)
            if board[i].count(background) == 10: # 행의 모든 값이 배경 타일이면
                board[i] = board[i-1] # 위에 행을 현재 행으로 변경
                board[i-1] = [background for i in range(10)] # 위에 행은 모든 값을 배경 타일로 초기화
        repeat -= 1 # 수행이 끝날 때마다 횟수 차감

spawn_block()
update_board()

keyList = ["left", "right", "down", "z", "space", "q", "r", "p"]
for key in keyList:
    keyboard.on_press_key(key, input_move_key)

move_down_coolTime = 1
pastTime = int(time.time())

while not gameOver:
    if not pause:
        currentTime = int(time.time())
        if currentTime - pastTime >= move_down_coolTime:
            move_down_block()
            Request_for_update = True
            pastTime = currentTime

        if Request_for_update:
            os.system('cls')
            update_board()
            Request_for_update = False
        
        if send_input_event:
            input_processing = True
            movable = True
            if key_left: # 왼쪽 키를 입력했을 경우
                key_left = False
                for i in range(len(board)): # 행 조회
                    for j in range(len(board[i])): # 열 조회
                        if (i, j) in blockPos: # blockPos가 갖고 있는 행과 열의 번호이면
                            if j != 0: # 가장 왼쪽 칸이 아니면
                                if board[i][j-1] != background: # 왼쪽 칸이 배경 타일이 아니면
                                    if (i, j-1) not in blockPos: # 왼쪽 칸이 blockPos가 갖고 있지 않은 행과 열의 번호이면
                                        movable = False # 이동 불가로 변경하고 열 조회 중지
                                        break
                            else: # 가장 왼쪽 칸이면
                                movable = False
                                break
                    if not movable: # 이동 불가 상태이면 행 조회도 중지
                        break
                if movable: # 이동 가능 상태가 유지 되었으면
                    rotateCenterPos = (rotateCenterPos[0], rotateCenterPos[1]-1) # 회전 중심의 열 번호 -1
                    for i, pos in enumerate(blockPos): # 블록의 행, 열 조회
                        board[pos[0]][pos[1]-1] = board[pos[0]][pos[1]] # 픽셀을 왼쪽으로 한 칸 이동
                        board[pos[0]][pos[1]] = background
                        blockPos[i] = (pos[0], pos[1]-1) # blockPos의 행과 열의 번호를 수정
            elif key_right: # 오른쪽 키를 입력했을 경우
                key_right = False
                for i in range(len(board)): # 행 조회
                    for j in range(len(board[i])-1, -1, -1): # 열 조회(역순)
                        if (i, j) in blockPos: # blockPos가 갖고 있는 행과 열의 번호이면
                            if j != len(board[i])-1: # 가장 오른쪽 칸이 아니면
                                if board[i][j+1] != background: # 오른쪽 칸이 배경 타일이 아니면
                                    if (i, j+1) not in blockPos: # 오른쪽 칸이 blockPos가 갖고 있지 않은 행과 열의 번호이면
                                        movable = False # 이동 불가로 변경하고 열 조회 중지
                                        break
                            else: # 가장 오른쪽 칸이면
                                movable = False
                                break
                    if not movable: # 이동 불가 상태이면 행 조회도 중지
                        break
                if movable: # 이동 가능 상태가 유지 되었으면
                    rotateCenterPos = (rotateCenterPos[0], rotateCenterPos[1]+1) # 회전 중심의 열 번호 +1
                    blockPos.reverse() # blockPos의 배열을 역순으로 변경
                    for i, pos in enumerate(blockPos): # 블록의 행, 열 조회
                        board[pos[0]][pos[1]+1] = board[pos[0]][pos[1]] # 픽셀을 오른쪽으로 한 칸 이동
                        board[pos[0]][pos[1]] = background
                        blockPos[i] = (pos[0], pos[1]+1) # blockPos의 행과 열의 번호를 수정
                    blockPos.reverse() # 배열을 역순에서 원래대로 변경
            elif key_down: # 아래쪽 키를 입력했을 경우
                key_down = False
                move_down_block() # move_down_block 함수 호출
            elif key_space: # 스페이스바를 입력했을 경우
                key_space = False
                move_down_block(moveKeyX=True) # moveKeyX의 기본값을 True로 변경해서 호출
            elif key_z: # z를 입력했을 경우
                key_z = False
                rotatedblockPos = rotate_block() # 블록 회전 결과
                if rotatedblockPos: # 반환값의 리스트가 비어있지 않으면
                    for i, pos in enumerate(blockPos): # 블록의 행, 열 조회
                        newRow, newCol = rotatedblockPos[i][0], rotatedblockPos[i][1] # rotatedblockPos의 행, 열 번호
                        board[newRow][newCol] = board[pos[0]][pos[1]] # 행, 열 번호로 픽셀 이동
                        if (pos[0], pos[1]) not in rotatedblockPos: # 픽셀의 행, 열 번호가 rotatedblockPos안에 있지 않으면
                            board[pos[0]][pos[1]] = background
                        blockPos[i] = (newRow, newCol) # blockPos의 행, 열 번호 수정
                        orgBlockPos[i] = (newRow - rotateCenterPos[0], newCol - rotateCenterPos[1]) # orgBlockPos의 행, 열 번호 수정
                    blockPos.sort()
                    orgBlockPos.sort()
            
            Request_for_update = True
            send_input_event = False
            input_processing = False
    
    if reset:
        board = [[background for i in range(10)] for j in range(21)]
        randomArrange = []
        score = 0
        spawn_block()
        Request_for_update = True
        pause = False
        reset = False
    time.sleep(0.017)

print("Game Over")