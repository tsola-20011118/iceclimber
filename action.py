import pyxel


class App:
    def __init__(self):
        pyxel.init(216, 16 * 3 * 8, fps=30);
        pyxel.load("player.pyxres");
        self.player = Player();
        pyxel.run(self.update, self.draw);
        

    def update(self):
        self.player.update();

    def draw(self):
        pyxel.cls(9);
        self.player.draw();
        for i in range(8 * 3):
            if i % 3 == 0:
                pyxel.line(0, i * 16-1, 216, i * 16-1, 0);
            else:
                pyxel.line(0, i * 16-1, 216, i * 16-1, 11);
        # pyxel.blt(0, 0, 0, 0, 0, 12, 16, 0)
        pyxel.text(0, 0, str(self.player.actionTime), 0);
        pyxel.text(0, 10, str(self.player.y), 0)


class Player:
    def __init__(self):
        self.x = 216 / 2 - 6; #102
        self.y = 16 * 3 * 8 - 16;
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

    def update(self):
        # 常に行う処理
        self.action()
        if self.actionFlag == False:
            # 上に上がる
            self.moveUD();
            # 右左に動く
            self.moveRL();
            # 左右にはみ出た時反対側に移動する
            self.moveOut();
        self.imageChange();

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.imageNumX, self.imageNumY, 16, 16, 0)
        if self.moveOutL == True:
            pyxel.blt(216 + self.x, self.y, 0, self.imageNumX, self.imageNumY, 16, 16, 0);
        if self.moveOutR == True:
            pyxel.blt(self.x - 216, self.y, 0, self.imageNumX, self.imageNumY, 16, 16, 0);

    #TODO self.headを0に戻す処理
    def moveUD(self):
        if pyxel.btnp(pyxel.KEY_UP, 1, 1):
            self.y -= 3
            self.head = -1
        if pyxel.btnp(pyxel.KEY_DOWN, 1, 1):
            self.y += 3
            self.head = 1

    def moveRL(self):
        if pyxel.btnp(pyxel.KEY_RIGHT, 1, 1):
            self.x += 3;
            self.face = 1;
        if pyxel.btnp(pyxel.KEY_LEFT, 1, 1):
            self.x -= 3;
            self.face = -1;

    def moveOut(self):
        if self.x < 0 and self.x + 16 > 0:
            self.moveOutL = True;
        if self.moveOutL == True:
            if self.x < -16:
                self.x = 216 + self.x;
                self.moveOutL = False;
            if self.x > 0:
                self.moveOutL = False;
        if self.x < 216 and self.x + 16 > 216:
            self.moveOutR = True;
        if self.moveOutR == True:
            if self.x > 216:
                self.x = self.x - 216
                self.moveOutR = False;
            if self.x < 216 - 16:
                self.moveOutR = False;

    def action(self):
        if pyxel.btnp(pyxel.KEY_SPACE, 1, 1):
            self.actionFlag = True
        if self.actionFlag == True:
            self.actionTime += 1
            if self.actionTime == 6 * 4 + 4:
                self.actionFlag = False
                self.actionTime = 0

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
    def __init__(self):
        self.x = 216 / 2 - 6

    def update(self):
        pass

    def draw(self):
        pass


App();
