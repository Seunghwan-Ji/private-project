import random as rd # 블록 모양을 랜덤으로 뽑는 용도
from copy import deepcopy # 값을 복사하여 복사본을 수정 후 원본에 덮어 씌우는 용도
import keyboard # 키 이벤트 처리 용도
import time # 루프 속도, 기능의 쿨타임 관리 용도
import os # 이전 출력 제거하는 용도

backgroundTile = "⚫" # 배경 타일
board = [[backgroundTile for _ in range(10)] for _ in range(21)] # 10 X 21 보드판 생성
blockPos = [] # 블록의 각 픽셀이 위치하는 행, 열 번호
orgBlockPos = [] # 블록을 원점에 배치했을 때 각 픽셀이 위치하는 행, 열 번호
rotateCenterPos = () # 블록의 회전 중심이 되는 행, 열 번호
silhouettePos = [] # 실루엣의 각 픽셀이 위치하는 행, 열 번호
blocks = [ # 블록 모양 종류
    [["🛸", "🛸"],
     ["🛸", "🛸"]],
    
    [["🚀", "🚀", "🚀", "🚀"]],
    
    [["👾", "👾", "⚫"],
     ["⚫", "👾", "👾"]],
    
    [["⚫", "👻", "👻"],
     ["👻", "👻", "⚫"]],
    
    [["👽", "⚫", "⚫"],
     ["👽", "👽", "👽"]],
    
    [["⚫", "⚫", "🤖"],
     ["🤖", "🤖", "🤖"]],

    [["⚫", "🪐", "⚫"],
     ["🪐", "🪐", "🪐"]]
    ]
silhouetteTile = "🌕" # 실루엣 타일
randomArrange = [] # 7개 블록 순서 랜덤 배열
score = 0 # 점수
gameOver = False
key_left = False
key_right = False
key_down = False
key_space = False
key_z = False
reset = False # 재시작
pause = False # 일시 중지
request_update_board = False # 보드 업데이트 요청
request_key_process = False # 키 처리 요청
key_processing = False # 키 처리중

def update_board(): # 현재 보드판의 상태 출력
    board_gui = "Score: %d" % (score)
    for i in board[1:]:
        board_gui += ("\n" + "".join(i))
    print(board_gui)

def spawn_block(): # 블록 생성
    if board[0].count(backgroundTile) == 10: # 블록이 쌓인 칸 수가 20을 초과하지 않았으면
        global blockPos
        global orgBlockPos
        global rotateCenterPos
        blockPos = []
        orgBlockPos = []
        if not randomArrange:
            while len(randomArrange) < 7:
                randomBlock = rd.choice(blocks) # 블록 모양 랜덤 선택
                if randomBlock not in randomArrange:
                    randomArrange.append(randomBlock)
        currentBlock = randomArrange[0]
        blockLen = len(currentBlock) # 블록의 행 길이
        randomArrange.remove(randomArrange[0])
        place = int((len(board[0])-blockLen) / 2) # (보드의 행 길이 - 블록의 행 길이) / 2
        prlDisplace = () # 평행이동 수치
        for i in range(len(currentBlock)): # 블록의 행 조회
            for j in range(len(currentBlock[i])): # 블록의 열 조회
                if currentBlock[i][j] != backgroundTile:
                    board[i][j+place] = currentBlock[i][j] # 블록의 각 행을 보드판 위쪽 가운데에 배치
                    blockPos.append((i, j+place)) # 배치된 행, 열 번호를 blockPos에 저장
                    orgBlockPos.append((i, j)) # 원점에 배치했을 때 행, 열 번호를 orgBlockPos에 저장
                    if i == len(currentBlock) // 2 and j == len(currentBlock[0]) // 2:
                        rotateCenterPos = (i, j+place) # 보드에서 회전중심이 위치하는 행, 열 번호
                        prlDisplace = (i, j) # 원점에 배치했을 때 원점과 회전중심의 거리차이
        for i, pos in enumerate(orgBlockPos):
            orgBlockPos[i] = (pos[0] - prlDisplace[0], pos[1] - prlDisplace[1]) # 블록을 원점에 배치했을 때, prlDisplace 만큼 평행이동하여
                                                                                # 블록의 회전중심이 원점에 배치되도록 설정
    else:
        global gameOver
        gameOver = True

def move_block_down(moveKeyX=False): # 블록 아래로 이동
    global board
    global blockPos
    global rotateCenterPos
    while True:
        copy_board = deepcopy(board) # 현재 보드판 상태 복사
        copy_blockPos = deepcopy(blockPos) # 현재 블록 위치 정보 복사
        movable = True
        for i, pos in enumerate(blockPos):
            row, col = pos[0], pos[1]
            if row != len(board)-1: # 보드의 마지막 행 번호가 아니면
                lowerSpace = board[row+1][col]
                if lowerSpace == backgroundTile or lowerSpace == silhouetteTile or (row+1, col) in blockPos:
                    copy_blockPos[i] = (row+1, col)
                    copy_board[row+1][col] = board[row][col]
                    if (row, col) not in copy_blockPos:
                        copy_board[row][col] = backgroundTile
                else:
                    movable = False
                    break
            else:
                movable = False
                break
        
        if movable: # 이동 가능 상태가 유지 되었으면
            rotateCenterPos = (rotateCenterPos[0]+1, rotateCenterPos[1]) # 회전 중심의 행 번호 +1
            board = copy_board # 복사본의 변경사항을 적용
            blockPos = copy_blockPos
            if not moveKeyX: # 사용자가 x키를 누르지 않았으면 break
                break
        else: # 이동 불가 상태이면 break
            reset_row() # reset_row 함수를 호출하여 값이 모두 채워진 행이 있는지 검사
            break

def move_block_left(): # 블록 왼쪽으로 이동
    global board
    global blockPos
    global rotateCenterPos
    copy_board = deepcopy(board)
    copy_blockPos = deepcopy(blockPos)
    movable = True
    for i, pos in enumerate(blockPos):
        row, col = pos[0], pos[1]
        if col != 0: # 가장 왼쪽 칸이 아니면
            if board[row][col-1] == backgroundTile or (row, col-1) in blockPos:
                copy_blockPos[i] = (row, col-1)
                copy_board[row][col-1] = board[row][col]
                if (row, col) not in copy_blockPos:
                    copy_board[row][col] = backgroundTile
            else:
                movable = False
                break
        else: # 가장 왼쪽 칸이면
            movable = False
            break

    if movable:
        rotateCenterPos = (rotateCenterPos[0], rotateCenterPos[1]-1)
        board = copy_board
        blockPos = copy_blockPos

def move_block_right(): # 블록 오른쪽으로 이동
    global board
    global blockPos
    global rotateCenterPos
    copy_board = deepcopy(board)
    copy_blockPos = deepcopy(blockPos)
    movable = True
    for i, pos in enumerate(blockPos):
        row, col = pos[0], pos[1]
        if col != len(board[i])-1: # 가장 오른쪽 칸이 아니면
            if board[row][col+1] == backgroundTile or (row, col+1) in blockPos:
                copy_blockPos[i] = (row, col+1)
                copy_board[row][col+1] = board[row][col]
                if (row, col) not in copy_blockPos:
                    copy_board[row][col] = backgroundTile
            else:
                movable = False
                break
        else: # 가장 오른쪽 칸이면
            movable = False
            break
    
    if movable:
        rotateCenterPos = (rotateCenterPos[0], rotateCenterPos[1]+1)
        board = copy_board
        blockPos = copy_blockPos

def rotate_block(): # 블록 회전
    rotatedblockPos = [] # 블록 회전 결과
    for pos in orgBlockPos: # 원점 배열 조회
        rotateRow = pos[1] + rotateCenterPos[0] # 회전했을 때 행 번호
        rotateCol = -pos[0] + rotateCenterPos[1] # 회전했을 때 열 번호
        if 0 <= rotateRow <= len(board)-1 and 0 <= rotateCol <= len(board[0])-1: # 행, 열 번호가 보드판을 벗어나지 않으면
            if board[rotateRow][rotateCol] != backgroundTile and board[rotateRow][rotateCol] != silhouetteTile: # 회전 했을때 위치의 값이 배경 타일이 아니면
                if (rotateRow, rotateCol) not in blockPos: # 행, 열 번호가 blockPos에 없으면
                    rotatedblockPos = [] # 리스트를 비우고 중지
                    break
            rotatedblockPos.append((rotateRow, rotateCol)) # break가 안 걸렸으면 행, 열 번호 추가
        else: # 벗어나면
            rotatedblockPos = []
            if rotateRow < 0: # 천장 이탈
                move_block_down()
                rotate_block() # 아래로 한 칸 이동 후 재귀
            elif rotateCol < 0: # 왼쪽벽 이탈
                move_block_right()
                rotate_block() # 오른쪽으로 한 칸 이동 후 재귀
            elif rotateCol > len(board[0])-1: # 오른쪽 벽 이탈
                move_block_left()
                rotate_block() # 왼쪽으로 한 칸 이동 후 재귀
            break
    
    if rotatedblockPos: # 리스트가 비어있지 않으면
        for i, pos in enumerate(blockPos): # 블록의 행, 열 번호 조회
            newRow, newCol = rotatedblockPos[i][0], rotatedblockPos[i][1] # rotatedblockPos의 행, 열 번호
            board[newRow][newCol] = board[pos[0]][pos[1]] # 행, 열 번호로 픽셀 이동
            if (pos[0], pos[1]) not in rotatedblockPos: # 픽셀의 행, 열 번호가 rotatedblockPos안에 있지 않으면
                board[pos[0]][pos[1]] = backgroundTile # 픽셀의 이전 위치의 값은 배경 타일로 변경
            blockPos[i] = (newRow, newCol) # blockPos의 행, 열 번호 수정
            orgBlockPos[i] = (newRow - rotateCenterPos[0], newCol - rotateCenterPos[1]) # orgBlockPos의 행, 열 번호 수정
        blockPos.sort()
        orgBlockPos.sort()

def reset_row(): # 채워진 행 초기화
    resetCount = 0 # 행 초기화 횟수
    for i in range(1, len(board)): # 두번째 행 ~ 마지막 행까지 조회
        if backgroundTile not in board[i] and silhouetteTile not in board[i]: # 행 안에 값이 모두 채워져 있으면
            board[i] = [backgroundTile for i in range(10)] # 행의 모든 값을 배경 타일로 초기화
            resetCount += 1 # 행 초기화 횟수 추가
    if resetCount: # 행 초기화 작업이 이루어 졌다면
        global score
        score += resetCount*100 # 점수 부여
        move_row_down(resetCount) # 모든 행들을 아래로 밀착 시키기 위해 move_row_down 함수에 resetCount만큼 값을 전달하여 호출
    spawn_block() # spawn_block 함수를 호출해 다음 블록 생성

def move_row_down(repeat): # 행 아래로 이동
    while repeat: # reset_row 함수에서 행 초기화 횟수만큼 수행
        for i in range(len(board)-1, 1, -1): # 행 조회(아래에서 위로 세번째 행 까지 역순)
            if board[i].count(backgroundTile) == 10: # 행의 모든 값이 배경 타일이면
                board[i] = board[i-1] # 위에 행을 현재 행으로 변경
                board[i-1] = [backgroundTile for i in range(10)] # 위에 행은 모든 값을 배경 타일로 초기화
        repeat -= 1 # 수행이 끝날 때마다 횟수 차감

def mark_silhouette(): # 블록 실루엣 표시
    global silhouettePos
    for pos in silhouettePos: # 실루엣의 행, 열 번호 조회
        row, col = pos[0], pos[1]
        if board[row][col] == silhouetteTile: # 실루엣 타일이면
            board[row][col] = backgroundTile # 배경 타일로 변경
    silhouettePos = deepcopy(blockPos) # 현재 블록 위치 정보 복사
    while True:
        copy_silhouettePos = deepcopy(silhouettePos) # 현재 실루엣 위치 정보 복사
        movable = True
        for i, pos in enumerate(silhouettePos): # 실루엣의 행, 열 번호 조회
            row, col = pos[0], pos[1]
            if row != len(board)-1: # 보드의 마지막 행 번호가 아니면
                lowerSpace = board[row+1][col]
                if lowerSpace == backgroundTile or lowerSpace == silhouetteTile or (row+1, col) in silhouettePos:
                    copy_silhouettePos[i] = (row+1, col)
                else:
                    movable = False
                    break
            else:
                movable = False
                break
        
        if movable: # 이동 가능 상태가 유지 되었으면
            silhouettePos = copy_silhouettePos # 복사본의 변경사항을 적용
        else:
            for pos in silhouettePos: # 변경사항이 적용된 실루엣의 행, 열 번호 조회
                row, col = pos[0], pos[1]
                if board[row][col] == backgroundTile: # 배경 타일이면
                    board[row][col] = silhouetteTile # 실루엣 타일로 변경
            break

def handle_key_event(key): # 키 이벤트 관리
    if not key_processing: # 키 처리중이 아니면
        global pause
        if not pause and key.name == "left":
            global key_left
            key_left = True # 왼쪽 이동 기능 활성화
        elif not pause and key.name == "right":
            global key_right
            key_right = True # 오른쪽 이동 기능 활성화
        elif not pause and key.name == "down":
            global key_down
            key_down = True # 아래쪽 이동 기능 활성화
        elif not pause and key.name == "space":
            global key_space
            key_space = True # 빠른 낙하 기능 활성화
        elif not pause and key.name == "z": # z키
            global key_z
            key_z = True # 회전 기능 활성화
        elif key.name == "f1":
            pause = not pause # 일시 중지/재개
            if pause:
                print("Pause")
        elif key.name == "f2":
            print("Restarting...")
            global reset
            reset = True # 재시작
        elif key.name == "f3":
            global gameOver
            gameOver = True # 종료
        
        global request_key_process
        request_key_process = True # 키 처리 요청

keyList = ["left", "right", "down", "z", "space", "f1", "f2", "f3"] # 키 종류
for key in keyList:
    keyboard.on_press_key(key, handle_key_event) # 위 키들을 누르면 handle_key_event 함수 호출

spawn_block()

move_down_coolTime = 1 # 블록 아래로 자동 이동 쿨타임
pastTime = int(time.time()) # 과거 시간

while not gameOver:
    if not pause: # 일시 중지 상태가 아니면
        currentTime = int(time.time()) # 현재 시간
        if currentTime - pastTime >= move_down_coolTime: # (현재 시간 - 과거 시간)이 쿨타임 이상이면
            move_block_down()
            request_update_board = True
            pastTime = currentTime

        if request_update_board: # 보드 업데이트 요청 처리
            os.system('cls') # 이전 출력 모두 제거
            mark_silhouette()
            update_board()
            request_update_board = False
        
        if request_key_process: # 키 처리 요청 처리
            key_processing = True # 키 처리중
            if key_left:
                move_block_left()
                key_left = False
            elif key_right:
                move_block_right()
                key_right = False
            elif key_down:
                move_block_down()
                key_down = False
            elif key_space:
                move_block_down(moveKeyX=True) # moveKeyX의 기본값을 True로 변경해서 호출
                key_space = False
            elif key_z:
                rotate_block()
                key_z = False
            request_update_board = True
            request_key_process = False
            key_processing = False # 키 처리 끝남
    
    if reset: # 초기화 작업(재시작)
        key_processing = True
        board = [[backgroundTile for _ in range(10)] for _ in range(21)]
        randomArrange = []
        score = 0
        spawn_block()
        request_update_board = True
        pause = False
        reset = False
        time.sleep(1)
        key_processing = False
    
    time.sleep(0.017) # 루프 속도

print("Game Over")