import pyxel

class App:
    def __init__(self):
        pyxel.init(224, 16 * 3 * 8, fps=30);#224/12=18
        pyxel.load("action.pyxres")
        self.window = [];
        self.window.append(Window(0));
        # self.window.append(Window(-16 * 3 * 8))
        self.windowNum = 0;
        
        self.player = Player();
        pyxel.run(self.update, self.draw);

    def update(self):
        if self.player.currentWindow + 1 >= self.windowNum:
            self.window.append(Window(-1 * 16 * 3 * 8))
            self.windowNum += 1;
        self.player.update()
        if self.player.windowChange == True:
            if self.player.currentWindow != 0 : self.window[self.player.currentWindow - 1].update()
            self.window[self.player.currentWindow].update()
            if self.player.currentWindow + 1 <= self.windowNum: self.window[self.player.currentWindow + 1].update()

    def draw(self):
        pyxel.cls(0);
        pyxel.text(0, 0, str(self.player.currentWindow), 8)
        pyxel.text(0, 10, str(self.windowNum), 8)
        for i in range(8 * 3):
            if i % 3 == 0:
                pyxel.line(0, i * 16-1, 224, i * 16-1, 0);
            else:
                pyxel.line(0, i * 16-1, 224, i * 16-1, 11);
        # if self.window[self.currentWindow].y >= -1 * 16 * 3 * 8 and self.window[self.player.currentWindow].y <= 16 * 3 * 8:
        # if self.player.currentWindow != 0: self.window[self.player.currentWindow - 1].draw()
        self.window[self.player.currentWindow].draw()
        # if self.player.currentWindow + 1 <= self.windowNum:self.window[self.player.currentWindow + 1].draw()
        self.player.draw()


class Player:
    def __init__(self):
        self.x = 224 / 2 - 6; #102
        self.y = 16 * 3 * 8 - 32;
        self.tempY = 0;
        # playerが右端にはみ出ている時のflag
        self.moveOutR = False;
        # playerが左端にはみ出ている時のflag
        self.moveOutL = False;
        # imageのnum
        self.imageNumX = 48;
        self.imageNumY = 0;
        # 攻撃状態か否かのflag;
        self.actionFlag = False;
        # 攻撃状態の経過時間
        self.actionTime = 0;
        # playerの向き
        self.face = 0;
        # playerの向き
        self.head = 0
        # playerの画面遷移化の確認
        self.windowChange = False;
        self.currentWindow = 0


    def update(self):
        self.windowMove()
        # 常に行う処理
        if self.windowChange == False:
            self.action()
            if self.actionFlag == False:
                # 上に上がる
                self.moveUD()
                # 右左に動く
                self.moveRL();
                # 左右にはみ出た時反対側に移動する
                self.moveOut();
            self.imageChange();

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.imageNumX, self.imageNumY, 16, 16, 0)
        if self.moveOutL == True:
            pyxel.blt(224 + self.x, self.y, 0, self.imageNumX, self.imageNumY, 16, 16, 0);
        if self.moveOutR == True:
            pyxel.blt(self.x - 224, self.y, 0, self.imageNumX, self.imageNumY, 16, 16, 0);
        

    #TODO self.headを0に戻す処理
    def moveUD(self):
        if pyxel.btnp(pyxel.KEY_UP, 1, 1):
            self.y -= 4
            self.head = -1
        if pyxel.btnp(pyxel.KEY_DOWN, 1, 1):
            self.y += 4
            self.head = 1

    def moveRL(self):
        if pyxel.btnp(pyxel.KEY_RIGHT, 1, 1):
            self.x += 4
            self.face = 1;
        if pyxel.btnp(pyxel.KEY_LEFT, 1, 1):
            self.x -= 4
            self.face = -1;

    def moveOut(self):
        if self.x < 0 and self.x + 12 > 0:
            self.moveOutL = True;
        if self.moveOutL == True:
            if self.x < -12:
                self.x = 224 + self.x;
                self.moveOutL = False;
            if self.x > 0:
                self.moveOutL = False;
        if self.x < 224 and self.x + 12 > 224:
            self.moveOutR = True;
        if self.moveOutR == True:
            if self.x > 224:
                self.x = self.x - 224
                self.moveOutR = False;
            if self.x < 224 - 12:
                self.moveOutR = False;

    def action(self):
        if pyxel.btnp(pyxel.KEY_SPACE, 1, 1):
            self.actionFlag = True
        if self.actionFlag == True:
            self.actionTime += 1
            if self.actionTime == 6 * 4 + 4:
                self.actionFlag = False
                self.actionTime = 0

    def windowMove(self):
        if self.windowChange == False and self.y <= 0:
            self.windowChange = True
            self.currentWindow += 1;
            self.tempY = self.y
        if self.windowChange == True:
            if 16 * 3 * 8 == self.y:
                self.windowChange = False
            else:
                self.y += 8
        if self.windowChange == False and self.y > 16 * 3 * 8 - 32:
            self.y -= 4

    def imageChange(self):
        # if self.head != 0:
        #     self.imageNumX = 48
        #     self.imageNumY = 16
        if pyxel.btnp(pyxel.KEY_RIGHT, 1, 1):
            self.imageNumX = 32
            self.imageNumY = 0
        if pyxel.btnp(pyxel.KEY_LEFT, 1, 1):
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
        self.x = 0;
        self.y = y;
        self.back = self.Background(self.x, self.y)
        self.jem = self.Jem(self.x, self.y, self.back.ladder)
        self.enemy = self.Enemy(self.x, self.y, self.back.ladder, self.jem.jem);

    def update(self):
        self.y += 8;
        self.back.update(self.y);
        self.jem.update(self.y)
        self.enemy.update(self.y);

    def draw(self):
        self.back.draw()
        self.jem.draw()
        self.enemy.draw();

    class Background:
        def __init__(self, x, y):
            self.x = x;
            self.y = y;
            self.ladder = [pyxel.rndi(1, 13), pyxel.rndi(1, 13), pyxel.rndi(1, 13), pyxel.rndi(1, 13), pyxel.rndi(1, 13), pyxel.rndi(1, 13), pyxel.rndi(1, 13), 13]

        def update(self,y):
            self.y = y

        def draw(self):
            for y in range(24):
                if y % 3 == 2:
                    for x in range(14):
                        if x == self.ladder[int((y - 2) / 3)]:
                            pyxel.blt(self.x + x * 16, self.y + y * 16  - 56, 1, 48, 0, 16, 56, 8);
                        pyxel.blt(self.x + x * 16, self.y + y * 16, 1, 0, 0, 16, 16, 0);


    class Jem:
        def __init__(self, x, y, ladder):
            self.x = x
            self.y = y
            self.jem = [pyxel.rndi(1, 13), pyxel.rndi(1, 13), pyxel.rndi(1, 13), pyxel.rndi(1, 13), pyxel.rndi(1, 13), pyxel.rndi(1, 13), pyxel.rndi(1, 13), pyxel.rndi(1, 13)]
            for p in range(8):
                if self.jem[p] == ladder[p]:
                    self.jem[p] = pyxel.rndi(0,1)
                    self.jem[p] *= 13

        def update(self, y):
            self.y = y

        def draw(self):
            for y in range(24):
                if y % 3 == 1:
                    for x in range(14):
                        if x == self.jem[int(y / 3)]:
                            pyxel.blt(self.x + x * 16, self.y + y * 16, 1, 0, 16, 16, 16, 0)

    class Enemy:
        def __init__(self, x, y, ladder, jem):
            self.x = x
            self.y = y
            self.jem = [pyxel.rndi(1, 13), pyxel.rndi(1, 13), pyxel.rndi(1, 13), pyxel.rndi(
                1, 13), pyxel.rndi(1, 13), pyxel.rndi(1, 13), pyxel.rndi(1, 13), pyxel.rndi(1, 13)]
            for p in range(8):
                if self.jem[p] == ladder[p] or self.jem[p] == jem[p]:
                    while self.jem[p] == ladder[p] or self.jem[p] == jem[p]:
                        self.jem[p] = pyxel.rndi(1, 13);

        def update(self, y):
            self.y = y

        def draw(self):
            for y in range(24):
                if y % 3 == 1:
                    for x in range(14):
                        if x == self.jem[int(y / 3)]:
                            pyxel.blt(self.x + x * 16, self.y + y * 16, 2, 0, 0, 16, 16, 0);


App();
