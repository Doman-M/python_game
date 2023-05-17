import pygame as pg, sys
import random
pg.init()
pg.init()
screen = pg.display.set_mode((800, 600))
#プレイヤーデータ
myimgR = pg.image.load("images/playerR.png")
myimgR = pg.transform.scale(myimgR, (40, 50))
myimgL = pg.transform.flip(myimgR, True, False)
myrect = pg.Rect(50, 200, 40, 50)
#障害物
walls = [pg.Rect(0, 0, 800, 20),
        pg.Rect(0, 0, 20, 600),
        pg.Rect(780, 0, 20, 600),
        pg.Rect(0, 580, 800, 20)]

#ワナ
trapimg = pg.image.load("images/trap.png")
trapimg = pg.transform.scale(trapimg, (30, 30))
traps = []
for i in range(20):
    wx = 150 + i * 30
    wy = random.randint(20, 550)
    traps.append(pg.Rect(wx,wy,30,30))
#メインループで使う変数
rightFlag = True
#ゲームステージ
def gamestage():
    global rightFlag
    #画面の初期化
    screen.fill(pg.Color("DEEPSKYBLUE"))
    vx = 0
    vy = 0
    #ユーザーからの入力を調べる
    key = pg.key.get_pressed()
    #描画と判定
    if key[pg.K_RIGHT]:
        vx = 4
        rightFlag = True
    if key[pg.K_LEFT]:
        vx = -4
        rightFlag = False
    if key[pg.K_UP]:
        vy = -4
    if key[pg.K_DOWN]:
        vy = 4

    #プレイヤーの処理
    myrect.x += vx
    myrect.y += vy
    if myrect.collidelist(walls) != -1:
        myrect.x -= vx
        myrect.y -= vy

    if rightFlag:
        screen.blit(myimgR, myrect)
    else:
        screen.blit(myimgL, myrect)

    #壁の処理
    for wall in walls:
        pg.draw.rect(screen, pg.Color("DARKGREEN"), wall)
    #ワナの処理
    for trap in traps:
        screen.blit(trapimg, trap)

while True:
    gamestage()
    #画面の表示
    pg.display.update()
    pg.time.Clock().tick(60)
    #ゲームの終了
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()