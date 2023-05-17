from tkinter import font
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

#ボタン
replay_img = pg.image.load("images/replaybtn.png")
replay_img = pg.transform.scale(replay_img, (180, 90))
goalrect = pg.Rect(750,250,30,100)

#敵データ
enemyimgR = pg.image.load("images/cat.png")
enemyimgR = pg.transform.scale(enemyimgR, (50, 50))
enemyimgL = pg.transform.flip(enemyimgR, True, False)
enemyrect = pg.Rect(650, 200, 50, 50)


#メインループで使う変数
rightFlag = True
pushFlag = False
page = 1

#btnを押したらnewpageにジャンぷする
def button_to_jump(btn, newpage):
    global page, pushFlag
    #ユーザーからの入力を調べる
    mdown = pg.mouse.get_pressed()
    (mx, my) = pg.mouse.get_pos()
    if mdown[0]:
        if btn.collidepoint(mx, my) and pushFlag == False:
            #pg.mixer.Sound("sounds/pi.wav").play()
            page = newpage
            pushFlag = True
    else:
        pushFlag = False

#ゲームステージ
def gamestage():
    global rightFlag
    global page
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
    if myrect.collidelist(traps) != -1:
        #pg.mixer.Sound("sounds/down.wav").play()
        page = 2

    #ゴールの処理
    pg.draw.rect(screen, pg.Color("GOLD"), goalrect)
    if myrect.colliderect(goalrect):
        #pg.mixer.Sound("sounds/up.wav").play()
        page = 3

    #てきのしょり
    ovx = 0
    ovy = 0
    if enemyrect.x < myrect.x:
        ovx = 1
    else:
        ovx = -1
    if enemyrect.y < myrect.y:
        ovy = 1
    else:
        ovy = -1
    enemyrect.x += ovx
    enemyrect.y += ovy
    if ovx > 0:
        screen.blit(enemyimgR, enemyrect)
    else:
        screen.blit(enemyimgL, enemyrect)
    if myrect.colliderect(enemyrect):
        #pg.mixer.Sound("sounds/down.wav").play()
        page = 2

#ゲームデータのリセット
def gamereset():
    myrect.x = 50
    myrect.y = 100
    for d in range(20):
        traps[d].x = 150 + d * 30
        traps[d].y = random.randint(20,550)
    enemyrect.x = 650
    enemyrect.y = 200

def gameover():
    gamereset()
    screen.fill(pg.Color("NAVY"))
    font = pg.font.Font(None, 150)
    text = font.render("GAMEOVER", True, pg.Color("RED"))
    screen.blit(text, (100,200))
    btn1 = screen.blit(replay_img,(320, 480))
    #描画と判定
    button_to_jump(btn1, 1)

def gameclear():
    gamereset()
    screen.fill(pg.Color("GOLD"))
    font = pg.font.Font(None, 150)
    text = font.render("GAMECLEAR", True, pg.Color("RED"))
    screen.blit(text, (60,200))
    btn1 = screen.blit(replay_img,(320, 480))
    #描画と判定
    button_to_jump(btn1, 1)

while True:
    if page == 1:
        gamestage()
    elif page == 2:
        gameover()
    elif page == 3:
        gameclear()
    #画面の表示
    pg.display.update()
    pg.time.Clock().tick(60)
    #ゲームの終了
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()