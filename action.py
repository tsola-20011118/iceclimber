import pyxel

class App:
    def __init__(self):
        pyxel.init(224, 16 * 3 * 8, fps=30)  # 224/12=18 16 * 3 * 8
        pyxel.load("action.pyxres")
        self.window = [];
        self.window.append(Window(0));
        # self.window.append(Window(-16 * 3 * 8))
        self.windowNum = 0;
        self.player = Player();
        pyxel.run(self.update, self.draw);

    def update(self):
        if self.player.currentWindow != 0 :
            self.player.update(self.window[self.player.currentWindow], self.window[self.player.currentWindow - 1])
        else:
            self.player.update(self.window[self.player.currentWindow], None)
        if self.player.currentWindow + 1 > self.windowNum:
            self.window.append(Window(-16 * 3 * 8))
            self.windowNum += 1;
        # if self.player.windowChangeUP == True:
        #     if self.player.currentWindow != 0 : self.window[self.player.currentWindow - 1].update(self.player.windowChangeUP, self.player.windowChangeDOWN)
        # if self.player.windowChangeDOWN == True:
        #     if self.player.currentWindow + 1 <= self.windowNum: self.window[self.player.currentWindow + 1].update(self.player.windowChangeUP, self.player.windowChangeDOWN)
        self.window[self.player.currentWindow].update(self.player.windowChangeUP, self.player.windowChangeDOWN)

    def draw(self):
        pyxel.cls(0);
        for i in range(8 * 3):
            if i % 3 == 0:
                pyxel.line(0, i * 16-1, 224, i * 16-1, 0);
            else:
                pyxel.line(0, i * 16-1, 224, i * 16-1, 11);
        if self.player.currentWindow != 0: self.window[self.player.currentWindow - 1].draw()
        self.window[self.player.currentWindow].draw()
        # self.window[self.player.currentWindow + 1].draw()
        self.player.draw()




class Player:
    def __init__(self):
        self.x = 224 / 2 - 6  # 102
        self.y = 16 * 3 * 8 - 32
        self.y = 16
        # playerが右端にはみ出ている時のflag
        self.moveOutR = False
        # playerが左端にはみ出ている時のflag
        self.moveOutL = False
        # imageのnum
        self.imageNumX = 48
        self.imageNumY = 0
        # 攻撃状態か否かのflag;
        self.actionFlag = False
        # 攻撃状態の経過時間
        self.actionTime = 0
        # playerの向き
        self.face = 0
        # playerの向き
        self.head = 0
        # playerの画面遷移化の確認
        self.windowChangeUP = False
        # playerの画面遷移化の確認
        self.windowChangeDOWN = False
        self.currentWindow = 0
        self.moveUP = False
        self.moveDOWN = False
        # 今いる階数を把握
        self.floor = False
        self.ladderUP = False
        self.ladderDOWN = False
        self.tempY = 0

    def update(self, window, downwindow):
        self.windowMove()
        # 常に行う処理
        if self.windowChangeUP == False and self.windowChangeDOWN == False:
            self.floor = int(self.y / 16 / 3)
            self.ladderCheck(window, downwindow)
            if self.floor != False:
                self.action()
            if self.actionFlag == False:
                # 上に上がる
                self.moveUD()
                # 右左に動く
                self.moveRL(window)
                # 左右にはみ出た時反対側に移動する
                moveOut(self, 12)
            self.imageChange()

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.imageNumX, self.imageNumY, 16, 16, 0)
        if self.moveOutL == True:
            pyxel.blt(224 + self.x, self.y, 0, self.imageNumX,
                      self.imageNumY, 16, 16, 0)
        if self.moveOutR == True:
            pyxel.blt(self.x - 224, self.y, 0, self.imageNumX,
                      self.imageNumY, 16, 16, 0)

    def ladderCheck(self, window, downwindow):
        if self.ladderDOWN == False or self.ladderUP == False:
            # 上に上がる判定
            if window.back.ladder[int(self.floor)] * 16 < self.x and window.back.ladder[int(self.floor)] * 16 + 16 > self.x:
                self.ladderUP = True
            else:
                self.ladderUP = False
            if int(self.floor) != 7 and window.back.ladder[int(self.floor + 1)] * 16 < self.x and window.back.ladder[int(self.floor + 1)] * 16 + 16 > self.x:
                self.ladderDOWN = True
            elif int(self.floor) == 7 and downwindow != None and downwindow.back.ladder[0] * 16 < self.x and downwindow.back.ladder[0] * 16 + 16 > self.x:
                self.ladderDOWN = True
            else:
                self.ladderDOWN = False

    # TODO self.headを0に戻す処理
    def moveUD(self):
        if self.head == 0 and self.ladderUP == True:
            if pyxel.btnp(pyxel.KEY_UP, 1, 1):
                self.head = -1
                self.ladderUP = False
                self.tempY = self.y
        if self.head == -1:
            if self.y == self.tempY - 48:
                self.head = 0
            else:
                self.y -= 4
        if self.head == 0 and self.ladderDOWN == True:
            if pyxel.btnp(pyxel.KEY_DOWN, 1, 1):
                self.head = 1
                self.ladderDOWN = False
                self.tempY = self.y
        if self.head == 1:
            if self.y == self.tempY + 48:
                self.head = 0
            else:
                self.y += 4

    def moveRL(self, window):
        if self.head == 0:
            if pyxel.btnp(pyxel.KEY_RIGHT, 1, 1):
                self.x += 4
                self.face = 1
            if pyxel.btnp(pyxel.KEY_LEFT, 1, 1):
                self.x -= 4
                self.face = -1



    def action(self):
        if pyxel.btnp(pyxel.KEY_SPACE, 1, 1):
            self.actionFlag = True
        if self.actionFlag == True:
            self.actionTime += 1
            if self.actionTime == 6 * 4 + 4:
                self.actionFlag = False
                self.actionTime = 0

    def windowMove(self):
        # 動いてない時
        if self.moveUP == False and self.windowChangeDOWN == False and self.windowChangeUP == False:
            if self.y <= 0:
                self.windowChangeUP = True
                self.currentWindow += 1
                self.moveUP = True
                self.head = 0
            if self.y >= 16 * 3 * 8:
                self.windowChangeDOWN = True
                self.currentWindow -= 1
                self.moveDOWN = True
                self.head = 0
        if self.moveUP == True and self.moveDOWN == False:
            if self.windowChangeDOWN == False:
                if self.windowChangeUP == True:
                    if 16 * 3 * 8 == self.y:
                        self.windowChangeUP = False
                    else:
                        self.y += 8
                if self.windowChangeUP == False:
                    self.y -= 4
                    if self.y <= 16 * 3 * 8 - 32:
                        self.moveUP = False
        if self.moveDOWN == True and self.moveUP == False:
            if self.windowChangeUP == False:
                if self.windowChangeDOWN == True:
                    if 0 == self.y:
                        self.windowChangeDOWN = False
                    else:
                        self.y -= 8
                if self.windowChangeDOWN == False:
                    self.y += 4
                    if self.y >= 16:
                        self.moveDOWN = False

    def imageChange(self):
        if self.head != 0:
            self.imageNumX = 48
            self.imageNumY = 16
        else:
            if self.face == 1:
                self.imageNumX = 32
                self.imageNumY = 0
            if self.face == -1:
                self.imageNumX = 32
                self.imageNumY = 16
            if self.actionFlag == True:
                if self.face == 1:
                    if self.actionTime % 6 <= 2:
                        self.imageNumX = 0
                        self.imageNumY = 0
                    else:
                        self.imageNumX = 16
                        self.imageNumY = 0
                if self.face == -1:
                    if self.actionTime % 6 <= 2:
                        self.imageNumX = 0
                        self.imageNumY = 16
                    else:
                        self.imageNumX = 16
                        self.imageNumY = 16


class Window:
    def __init__(self, y):
        self.x = 0
        self.y = y
        self.back = self.Background(self.x, self.y)
        self.jem = self.Jem(self.x, self.y, self.back.ladder)
        self.enemy = self.Enemy(self.x, self.y, self.back.ladder, self.jem.jem)
        self.moveenemy = self.MovingEnemy(
            self.x, self.y, self.back.ladder, self.jem.jem, self.enemy.place)
        self.moveenemy2 = self.MovingEnemy(
            self.x, self.y, self.back.ladder, self.jem.jem, self.enemy.place)

    def update(self, up, down):
        if up == True:
            self.y += 8
        if down == True:
            self.y -= 8
        self.back.update(self.y)
        self.jem.update(self.y)
        self.enemy.update(self.y)
        self.moveenemy.update(self.y, self.back.ladder)
        self.moveenemy2.update(self.y, self.back.ladder)

    def draw(self):
        self.back.draw()
        self.jem.draw()
        self.enemy.draw()
        self.moveenemy.draw()
        self.moveenemy2.draw()

    class Background:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.ladder = [pyxel.rndi(1, 12), pyxel.rndi(1, 12), pyxel.rndi(1, 12), pyxel.rndi(
                1, 12), pyxel.rndi(1, 12), pyxel.rndi(1, 12), pyxel.rndi(1, 12), pyxel.rndi(1, 12)]

        def update(self, y):
            self.y = y

        def draw(self):
            for y in range(24):
                if y % 3 == 2:
                    for x in range(14):
                        if x == self.ladder[int((y - 2) / 3)]:
                            pyxel.blt(self.x + x * 16, self.y + y *
                                      16 - 56, 1, 48, 0, 24, 56, 8)
                        pyxel.blt(self.x + x * 16, self.y +
                                  y * 16, 1, 0, 0, 16, 16, 0)

    class Jem:
        def __init__(self, x, y, ladder):
            self.x = x
            self.y = y
            self.jem = [pyxel.rndi(1, 13), pyxel.rndi(1, 13), pyxel.rndi(1, 13), pyxel.rndi(
                1, 13), pyxel.rndi(1, 13), pyxel.rndi(1, 13), pyxel.rndi(1, 13), pyxel.rndi(1, 13)]
            for p in range(8):
                if self.jem[p] == ladder[p]:
                    self.jem[p] = pyxel.rndi(0, 1)
                    self.jem[p] *= 13

        def update(self, y):
            self.y = y

        def draw(self):
            for y in range(24):
                if y % 3 == 1:
                    for x in range(14):
                        if x == self.jem[int(y / 3)]:
                            pyxel.blt(self.x + x * 16, self.y +
                                      y * 16, 1, 0, 16, 16, 16, 0)

    class Enemy:
        def __init__(self, x, y, ladder, jem):
            self.x = x
            self.y = y
            self.place = [pyxel.rndi(1, 13), pyxel.rndi(1, 13), pyxel.rndi(1, 13), pyxel.rndi(
                1, 13), pyxel.rndi(1, 13), pyxel.rndi(1, 13), pyxel.rndi(1, 13), pyxel.rndi(1, 13)]
            for p in range(8):
                if self.place[p] == ladder[p] or self.place[p] == jem[p]:
                    while self.place[p] == ladder[p] or self.place[p] == jem[p]:
                        self.place[p] = pyxel.rndi(1, 13)

        def update(self, y):
            self.y = y

        def draw(self):
            for y in range(24):
                if y % 3 == 1:
                    for x in range(14):
                        if x == self.place[int(y / 3)]:
                            pyxel.blt(self.x + x * 16, self.y +
                                      y * 16, 2, 0, 0, 16, 16, 0)

    class MovingEnemy:
        def __init__(self, x, y, ladder, jem, enemy):
            self.x = x
            self.y = y
            self.sum = [self.Enemy(), self.Enemy(), self.Enemy(), self.Enemy(), self.Enemy(), self.Enemy(), self.Enemy(), self.Enemy(),]
            for p in range(8):
                if self.sum[p].x == ladder[p] or self.sum[p].x == jem[p] or self.sum[p].x == enemy[p]:
                    while self.sum[p].x == ladder[p] or self.sum[p].x == jem[p] or self.sum[p].x == enemy[p]:
                        self.sum[p].x = pyxel.rndi(1, 13)
                    self.sum[p].x *= 16
            self.speed = 1.5

        def update(self, y, ladder):
            self.y = y
            for p in range(8):
                if self.sum[p].time % 100 == 13:
                    if self.sum[p].flag == 1:
                        self.sum[p].flag = 2
                    else:
                        self.sum[p].flag = 1
                if self.sum[p].flag == 1:
                    self.sum[p].x -= self.speed
                else:
                    self.sum[p].x += self.speed
                moveOut(self.sum[p], 16)
                self.sum[p].time += 1

        def draw(self):
            for y in range(24):
                if y % 3 == 1:
                    if self.sum[int(y / 3)].flag == 1:
                        pyxel.blt(self.x + self.sum[int(y / 3)].x, self.y + y * 16 - 8, 2, 16, 0, 16, 16, 0)
                        if self.sum[int(y / 3)].moveOutL == True:
                            pyxel.blt(224 + self.sum[int(y / 3)].x, self.y + y * 16 - 8, 2, 16, 0, 16, 16, 0)
                        if self.sum[int(y / 3)].moveOutR == True:
                            pyxel.blt(self.sum[int(y / 3)].x - 224, self.y + y * 16 - 8, 2, 16, 0, 16, 16, 0)
                    else:
                        pyxel.blt(self.x + self.sum[int(y / 3)].x, self.y + y * 16 - 8, 2, 32, 0, 16, 16, 0)
                        if self.sum[int(y / 3)].moveOutL == True:
                            pyxel.blt(224 + self.sum[int(y / 3)].x, self.y + y * 16 - 8, 2, 32, 0, 16, 16, 0)
                        if self.sum[int(y / 3)].moveOutR == True:
                            pyxel.blt(self.sum[int(y / 3)].x - 224, self.y + y * 16 - 8, 2, 32, 0, 16, 16, 0)
            pyxel.text(0, 30, str(self.sum[0].flag), 8)
            pyxel.text(0, 40, str(self.sum[0].moveOutL), 8)

        
        class Enemy:
            def __init__(self):
                self.x = pyxel.rndi(1, 13) * 16;
                self.flag = pyxel.rndi(1, 2);
                # playerが右端にはみ出ている時のflag
                self.moveOutR = False
                # playerが左端にはみ出ている時のflag
                self.moveOutL = False
                self.time = pyxel.rndi(1,60)

def moveOut(chara, size):
    if chara.x < 0 and chara.x + size > 0:
        chara.moveOutL = True
    if chara.moveOutL == True:
        if chara.x < -1 * size:
            chara.x = 224 + chara.x
            chara.moveOutL = False
        if chara.x > 0:
            chara.moveOutL = False
    if chara.x < 224 and chara.x + size > 224:
        chara.moveOutR = True
    if chara.moveOutR == True:
        if chara.x > 224:
            chara.x = chara.x - 224
            chara.moveOutR = False
        if chara.x < 224 - size:
            chara.moveOutR = False


App()
