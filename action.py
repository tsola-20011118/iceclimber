import pyxel

class App:
    def __init__(self):
        pyxel.init(224, 16 * 3 * 8, fps=30)  # 224/12=18 16 * 3 * 8
        pyxel.load("action.pyxres")
        self.window = [];
        self.window.append(Window(0));
        self.window.append(Window(-16 * 3 * 8))
        self.windowNum = 1;
        self.player = Player();
        self.gameMode = 0
        self.score = 0
        self.scoreFlag = False
        self.enemy1Flag = False
        pyxel.play(1,10, loop=True)
        pyxel.run(self.update, self.draw);

    def update(self):
        if self.gameMode == 0:
            if pyxel.btnp(pyxel.KEY_SPACE, 1, 1):
                self.gameMode = 1
        elif self.gameMode == 1:
            if self.player.currentWindow != 0 :
                self.player.update(self.window[self.player.currentWindow], self.window[self.player.currentWindow - 1])
            else:
                self.player.update(self.window[self.player.currentWindow], None)
            if self.player.currentWindow + 1 > self.windowNum:
                self.window.append(Window(-16 * 3 * 8))
                self.windowNum += 1;
            if self.player.windowChangeUP == True:
                if self.player.currentWindow != 0:
                    self.window[self.player.currentWindow - 1].update(self.player.windowChangeUP, self.player.windowChangeDOWN)
            if self.player.windowChangeDOWN == True:
                if self.player.currentWindow + 1 <= self.windowNum: self.window[self.player.currentWindow + 1].update(self.player.windowChangeUP, self.player.windowChangeDOWN)
            self.Get(self.window[self.player.currentWindow].jem)
            self.Bump(self.window[self.player.currentWindow].enemy, 2)
            self.Attack(self.window[self.player.currentWindow].enemy)
            self.Bump(self.window[self.player.currentWindow].moveenemy, 1)
            self.Bump(self.window[self.player.currentWindow].moveenemy2, 1)
            if self.player.life <= 0:
                self.gameMode = 2
        if self.gameMode == 2:
            if pyxel.btnp(pyxel.KEY_SPACE, 1, 1):
                self.gameMode = 0
                self.window = []
                self.window.append(Window(0))
                self.window.append(Window(-16 * 3 * 8))
                self.windowNum = 1
                self.player = Player()
                self.gameMode = 0
                self.score = 0
                self.scoreFlag = False
                self.enemy1Flag = False
        self.window[self.player.currentWindow].update(self.player.windowChangeUP, self.player.windowChangeDOWN)
        return 0

    def draw(self):
        pyxel.cls(1);
        if self.player.currentWindow != 0: self.window[self.player.currentWindow - 1].draw()
        self.window[self.player.currentWindow].draw()
        self.window[self.player.currentWindow + 1].draw()
        # if self.gameMode == 0:
        #     pyxel.rect(10, 150, 224 - 20, 80, 0)
        #     pyxel.rect(10, 250, 224 - 20, 40, 0)
        #     pyxel.text(90, 170, "ICE CRIMER", 7)
        #     pyxel.text(40, 200, "Collect coins while avoiding enemies!!", 7)
        #     pyxel.text(70, 270, "press space to start!!", 7)
        # elif self.gameMode == 1:
        #     self.player.draw()
        #     pyxel.text(224 - len(str(self.score)) * 4, 4, str(self.score), 8)
        # elif self.gameMode == 2:
        #     pyxel.rect(10, 150, 224 - 20, 80, 0)
        #     pyxel.rect(10, 250, 224 - 20, 40, 0)
        #     pyxel.text(95, 170, "ICE CRIMER", 7)
        #     pyxel.text(60, 200, "GAME OVER : YORU SCORE is "+ str(self.score) , 7)
        #     pyxel.text(60, 270, "press space to REstart!!", 7)

    def Bump(self, currentenemy, num):
        enemy = currentenemy.sum[self.player.floor]
        if self.player.y == self.player.floor * 16 * 3 + 16:
            if enemy.aliveFlag == False and enemy.x - 6 < self.player.x and self.player.x < enemy.x + 16 - 6 and self.player.actionFlag == False:
                self.enemy1Flag = True
                pyxel.play(0, 4, loop=False)
            if self.enemy1Flag == True :
                self.player.life -= num
                self.enemy1Flag = False
                enemy.drawFlag = False
                enemy.aliveFlag = True

    def Attack(self, currentenemy):
        enemy = currentenemy.sum[self.player.floor]
        if self.player.y == self.player.floor * 16 * 3 + 16:
            if enemy.aliveFlag == False and enemy.x - 12 - 4 < self.player.x and self.player.x < enemy.x + 16 + 4 and self.player.actionFlag == True:
                if (enemy.x + 8 >= self.player.x and self.player.face == 1) or (enemy.x + 8 <= self.player.x and self.player.face == -1):
                    self.enemy1Flag = True
            if self.enemy1Flag == True:
                enemy.life -= 1
                self.enemy1Flag = False
        if enemy.life == 0 and enemy.drawFlag == True:
            self.player.life += 1
            enemy.drawFlag = False
            enemy.aliveFlag = True

    def Get(self, currentjem):
        jem = currentjem.jem[self.player.floor]
        if self.player.y == self.player.floor * 16 * 3 + 16:
            if currentjem.jemFlag[self.player.floor] == False and jem * 16 - 12 <= self.player.x and self.player.x <= jem * 16 + 16 + 12 and self.player.actionFlag == True:
                if (jem * 16 + 8 >= self.player.x and self.player.face == 1) or (jem * 16 + 8 <= self.player.x and self.player.face == -1):
                    self.scoreFlag = True
            if self.scoreFlag == True:
                currentjem.life[self.player.floor] -= 1
                self.scoreFlag = False
        if currentjem.life[self.player.floor] == 0 and currentjem.jemFlag[self.player.floor] == False:
            currentjem.jemFlag[self.player.floor] = True
            self.score += 100
            pyxel.play(0, 3, loop=False)


class Player:
    def __init__(self):
        self.x = 224 / 2 - 6  # 102
        self.y = 16 * 3 * 8 - 32
        # playerが右端にはみ出ている時のflag
        self.moveOutR = False
        # playerが左端にはみ出ている時のflag
        self.moveOutL = False
        # imageのnum
        self.imageNumX = 48
        self.imageNumY = 0
        self.actionX = 0
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
        self.life = 16

    def update(self, window, downwindow):
        self.windowMove()
        # 常に行う処理
        if self.windowChangeUP == False and self.windowChangeDOWN == False:
            self.floor = int(self.y / 16 / 3)
            self.ladderCheck(window, downwindow)
            # if self.floor != False:
            self.action()
            if self.actionFlag == False and self.moveUP == False and self.moveDOWN == False:
                # 上に上がる
                self.moveUD()
                # 右左に動く
                self.moveRL(window)
                # 左右にはみ出た時反対側に移動する
                moveOut(self, 12)
            self.imageChange()

    def draw(self):
        pyxel.blt(self.x + self.actionX, self.y, 0, self.imageNumX, self.imageNumY, 16, 16, 0)
        if self.moveOutL == True:
            pyxel.blt(224 + self.x + self.actionX, self.y, 0, self.imageNumX,self.imageNumY, 16, 16, 0)
        if self.moveOutR == True:
            pyxel.blt(self.x - 224 + self.actionX, self.y, 0, self.imageNumX,self.imageNumY, 16, 16, 0)
        if self.life >= 0:
            pyxel.blt(0, 0, 0, 0, 32,  8 * self.life, 16, 0)

    def ladderCheck(self, window, downwindow):
        # if self.ladderDOWN == False or self.ladderUP == False:
            # 上に上がる判定
            if window.back.ladder[int(self.floor)] * 16 - 6  < self.x and window.back.ladder[int(self.floor)] * 16 + 24 - 6 > self.x:
                self.ladderUP = True
            else:
                self.ladderUP = False
            if int(self.floor) != 7 and window.back.ladder[int(self.floor + 1)] * 16 - 6 < self.x and window.back.ladder[int(self.floor + 1)] * 16 + 18 > self.x:
                self.ladderDOWN = True
            elif int(self.floor) == 7 and downwindow != None and downwindow.back.ladder[0] * 16 - 6 < self.x and downwindow.back.ladder[0] * 16 + 18 > self.x:
                self.ladderDOWN = True
            else:
                self.ladderDOWN = False

    def moveUD(self):
        if self.head == 0 and self.ladderUP == True:
            if pyxel.btnp(pyxel.KEY_UP, 1, 1):
                self.head = -10
                self.ladderUP = False
                self.tempY = self.y
                pyxel.play(0, 0, loop=False)
        if self.head == -10:
            if self.y == self.tempY - 32:
                self.head = -5
                self.tempY = self.y
            else:
                self.y -= 4
        if self.head == 0 and self.ladderDOWN == True:
            if pyxel.btnp(pyxel.KEY_DOWN, 1, 1):
                self.head = 10
                self.ladderDOWN = False
                self.tempY = self.y
                pyxel.play(0, 1, loop=False)
        if self.head == 10:
            if self.y == self.tempY + 16:
                self.head = 5
                self.tempY = self.y
            else:
                self.y += 4
        if self.head == -5 or self.head == 5:
            if pyxel.btnp(pyxel.KEY_UP, 1, 1):
                self.head = -1
                self.ladderUP = False
                pyxel.play(0, 0, loop=False)
            if pyxel.btnp(pyxel.KEY_DOWN, 1, 1):
                self.head = 1
                self.ladderDOWN = False
                pyxel.play(0, 1, loop=False)
        if self.head == -1:
            if self.y == self.tempY - 16:
                self.head = 0
            else:
                self.y -= 4
        if self.head == 1:
            if self.y == self.tempY + 32:
                self.head = 0
            else:
                self.y += 4

    def moveRL(self, window):
        if self.head == 0:
            if pyxel.btnp(pyxel.KEY_RIGHT, 1, 1):
                self.x += 2
                self.face = 1
            if pyxel.btnp(pyxel.KEY_LEFT, 1, 1):
                self.x -= 2
                self.face = -1

    def action(self):
        if pyxel.btnp(pyxel.KEY_SPACE, 1, 1):
            self.actionFlag = True
            pyxel.play(0, 2, loop=False)
        if self.actionFlag == True:
            self.actionTime += 1
            if self.actionTime == 6 * 2 + 4:
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
            self.actionX = 0
            self.imageNumX = 48
            self.imageNumY = 16
        else:
            if self.face == 1:
                self.actionX = 0
                self.imageNumX = 32
                self.imageNumY = 0
            if self.face == -1:
                self.actionX = 0
                self.imageNumX = 32
                self.imageNumY = 16
            if self.actionFlag == True:
                if self.face == 1:
                    if self.actionTime % 6 <= 2:
                        self.actionX = 0
                        self.imageNumX = 0
                        self.imageNumY = 0
                    else:
                        self.actionX = 0
                        self.imageNumX = 16
                        self.imageNumY = 0
                if self.face == -1:
                    if self.actionTime % 6 <= 2:
                        self.actionX = -4;
                        self.imageNumX = 0
                        self.imageNumY = 16
                    else:
                        self.actionX = -4
                        self.imageNumX = 16
                        self.imageNumY = 16


class Window:
    def __init__(self, y):
        self.x = 0
        self.y = y
        self.back = self.Background(self.x, self.y)
        self.jem = self.Jem(self.x, self.y, self.back.ladder)
        self.enemy = self.Enemy(self.x, self.y, self.back.ladder, self.jem.jem)
        self.moveenemy = self.MovingEnemy(self.x, self.y, self.back.ladder, self.jem.jem, self.enemy, 1.5)
        self.moveenemy2 = self.MovingEnemy(self.x, self.y, self.back.ladder, self.jem.jem, self.enemy , 2)

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
                            pyxel.blt(self.x + x * 16, self.y + y *16 - 56, 1, 48, 0, 24, 56, 8)
                        pyxel.blt(self.x + x * 16, self.y +y * 16, 1, 16, 0, 16, 16, 0)

    class Jem:
        def __init__(self, x, y, ladder):
            self.x = x
            self.y = y
            self.jem = [pyxel.rndi(1, 12), pyxel.rndi(1, 12), pyxel.rndi(1, 12), pyxel.rndi(
                1, 12), pyxel.rndi(1, 12), pyxel.rndi(1, 12), pyxel.rndi(1, 12), pyxel.rndi(1, 12)]
            for p in range(8):
                if self.jem[p] == ladder[p]:
                    self.jem[p] = pyxel.rndi(0, 1)
                    self.jem[p] *= 12
            self.jemFlag = [False, False, False, False, False, False, False, False]
            self.life = [6 * 4 + 3, 6 * 4 + 3, 6 * 4 + 3, 6 * 4 + 3, 6 * 4 + 3, 6 * 4 + 3, 6 * 4 + 3, 6 * 4 + 3]

        def update(self, y):
            self.y = y

        def draw(self):
            for y in range(24):
                if y % 3 == 1:
                    for x in range(14):
                        if x == self.jem[int(y / 3)] and self.jemFlag[int(y / 3)] == False:
                            if self.life[int(y / 3)] >= 6 * 2 + 3:
                                pyxel.blt(self.x + x * 16, self.y +  y * 16, 1, 16, 16, 16, 16, 0)
                            else:
                                pyxel.blt(self.x + x * 16, self.y +  y * 16, 1, 0, 16, 16, 16, 0)

    class Enemy:
        def __init__(self, x, y, ladder, jem):
            self.x = x
            self.y = y
            self.sum = [self.Enemy(), self.Enemy(), self.Enemy(), self.Enemy(), self.Enemy(), self.Enemy(), self.Enemy(), self.Enemy(),]
            for p in range(8):
                if self.sum[p].x == ladder[p] or (p != 7 and self.sum[p].x == ladder[p + 1]) or (p != 0 and (self.sum[p].x == ladder[p - 1] + 1 or self.sum[p].x == ladder[p - 1] - 1)) or self.sum[p].x == jem[p]:
                    while self.sum[p].x == ladder[p] or (p != 7 and self.sum[p].x == ladder[p + 1]) or (p != 0 and (self.sum[p].x == ladder[p - 1] + 1 or self.sum[p].x == ladder[p - 1] - 1)) or self.sum[p].x == jem[p]:
                        self.sum[p].x = pyxel.rndi(1, 12)
                self.sum[p].x *= 16

        def update(self, y):
            self.y = y

        def draw(self):
            for y in range(24):
                if y % 3 == 1:
                    for x in range(14):
                        if x == self.sum[int(y / 3)].x / 16:
                            if self.sum[int(y / 3)].drawFlag == True:
                                if self.sum[int(y / 3)].life >= 6 * 2 + 3 :
                                    pyxel.blt(self.x + self.sum[int(y / 3)].x , self.y + y * 16, 2, 0, 0, 16, 16, 0)
                                else:
                                    pyxel.blt(self.x + self.sum[int(y / 3)].x , self.y + y * 16, 2, 0, 16, 16, 16, 0)

        class Enemy:
            def __init__(self):
                self.enemyFlag = False
                self.x = pyxel.rndi(1, 12)
                self.flag = pyxel.rndi(1, 2)
                self.aliveFlag = False
                self.drawFlag = True
                self.life = 6 * 4 + 3

    class MovingEnemy:
        def __init__(self, x, y, ladder, jem, enemy, speed):
            self.x = x
            self.y = y
            self.sum = [self.Enemy(), self.Enemy(), self.Enemy(), self.Enemy(), self.Enemy(), self.Enemy(), self.Enemy(), self.Enemy()]
            for p in range(8):
                if self.sum[p].x == ladder[p] or self.sum[p].x == jem[p] or self.sum[p].x == enemy.sum[p].x:
                    while self.sum[p].x == ladder[p] or self.sum[p].x == jem[p] or self.sum[p].x == enemy.sum[p].x:
                        self.sum[p].x = pyxel.rndi(1, 13)
                    self.sum[p].x *= 16
            self.speed = speed

        def update(self, y, ladder):
            self.y = y
            for p in range(8):
                if self.sum[p].time % 100 == pyxel.rndi(0, 100):
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
                    if self.sum[int(y / 3)].drawFlag == True :
                        if self.sum[int(y / 3)].flag == 1:
                            pyxel.blt(
                                self.x + self.sum[int(y / 3)].x, self.y + y * 16 - 8, 2, 16, 0, 16, 16, 0)
                            if self.sum[int(y / 3)].moveOutL == True:
                                pyxel.blt(
                                    224 + self.sum[int(y / 3)].x, self.y + y * 16 - 8, 2, 16, 0, 16, 16, 0)
                            if self.sum[int(y / 3)].moveOutR == True:
                                pyxel.blt(
                                    self.sum[int(y / 3)].x - 224, self.y + y * 16 - 8, 2, 16, 0, 16, 16, 0)
                        else:
                            pyxel.blt(
                                self.x + self.sum[int(y / 3)].x, self.y + y * 16 - 8, 2, 32, 0, 16, 16, 0)
                            if self.sum[int(y / 3)].moveOutL == True:
                                pyxel.blt(
                                    224 + self.sum[int(y / 3)].x, self.y + y * 16 - 8, 2, 32, 0, 16, 16, 0)
                            if self.sum[int(y / 3)].moveOutR == True:
                                pyxel.blt(
                                    self.sum[int(y / 3)].x - 224, self.y + y * 16 - 8, 2, 32, 0, 16, 16, 0)

        class Enemy:
            def __init__(self):
                self.x = pyxel.rndi(1, 13) * 16
                self.flag = pyxel.rndi(1, 2)
                self.aliveFlag = False
                # playerが右端にはみ出ている時のflag
                self.moveOutR = False
                # playerが左端にはみ出ている時のflag
                self.moveOutL = False
                self.time = pyxel.rndi(1, 60)
                self.drawFlag = True
                self.life = 0


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
