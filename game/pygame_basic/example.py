import pygame as pg

pg.init()

boardColor = "#99ccff"
boardSize = [800, 500]
board = pg.display.set_mode(boardSize)

run = True
clock = pg.time.Clock()

airplane = pg.image.load("airplane.png") # 게임판 내 이미지 생성
airplane = pg.transform.scale(airplane, (60, 45)) # 크기 조절

def run_game():
    global run, airplane
    x, y = 0, 0
    moveUp = False
    moveDown = False
    moveLeft = False
    moveRight = False

    while run:
        clock.tick(60)
        board.fill(boardColor)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            # 움직임 구현
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    moveUp = True
                elif event.key == pg.K_DOWN:
                    moveDown = True
                elif event.key == pg.K_LEFT:
                    moveLeft = True
                elif event.key == pg.K_RIGHT:
                    moveRight = True
            elif event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    moveUp = False
                elif event.key == pg.K_DOWN:
                    moveDown = False
                elif event.key == pg.K_LEFT:
                    moveLeft = False
                elif event.key == pg.K_RIGHT:
                    moveRight = False
        
        # 맵 밖으로 나가지 못하게
        if moveUp and y > 0:
            y -= 5
        if moveDown and y < boardSize[1] - airplane.get_rect().size[1]: # 보드 사이즈의 최대 y좌표 - airplane의 높이
            y += 5
        if moveLeft and x > 0:
            x -= 5
        if moveRight and x < boardSize[0] - airplane.get_rect().size[0]: # 보드 사이즈의 최대 x좌표 - airplane의 너비
            x += 5

        board.blit(airplane, (x, y)) # airplane 이미지 배치
        pg.display.update()

run_game()

print("종료")
pg.quit()