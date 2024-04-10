import pygame as pg # 1. pygame 선언

pg.init() # 2. pygame 초기화

# 3. pygame에 사용되는 전역변수 선언
boardColor = (255, 255, 255) # 게임판 컬러
boardSize = [400, 300] # 게임판 사이즈
board = pg.display.set_mode(boardSize) # 게임판 선언

run = True # 게임 실행 변수
clock= pg.time.Clock() # 초당 프레임 변수 선언

# 4. pygame 무한루프
def runGame():
    global run
    while run:
        clock.tick(10) # 초당 프레임 설정
        board.fill(boardColor) # 게임판 컬러 적용

        for event in pg.event.get(): # 게임 내에서 발생한 이벤트들을 리스트 형태로 가져와 참조
            if event.type == pg.QUIT: # pg.QUIT: 게임창을 닫았을 때 발생하는 이벤트
                run = False # 게임 실행 중단
        pg.display.update() # 게임 상태 업데이트

runGame()

print("종료")
pg.quit() # pygame 종료