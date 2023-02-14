import pyxel
import math
import webbrowser

windowSizeX = 16 * 14
windowSizeY = 16 * 3 * 6
floorNum = 6

class App:
    def __init__(self):
        pyxel.init(windowSizeX, windowSizeY + 100, fps=30)
        pyxel.load("action2.pyxres")
        pyxel.play(1,10, loop=True)
        self.player = self.Player(0)
        self.window = []
        self.window.append(self.Window(0, 5));
        self.currentWindow = 0
        pyxel.run(self.update, self.draw);

    def update(self):
        if self.currentWindow == 0:
            self.player.update(0, self.window[self.currentWindow], 0)
        else:
            self.player.update(0, self.window[self.currentWindow],  self.window[self.currentWindow - 1])
        self.window[self.currentWindow].update()


    def draw(self):
        pyxel.cls(1);
        self.window[self.currentWindow].draw()
        self.player.draw()
        ImageBank(0, 0, 100)
        # pyxel.text(0, 0, str(self.player.data.ladderUP), 0)
        # pyxel.text(0, 16, str(self.player.data.ladderDOWN), 0)
        # pyxel.text(0, 16, str(self.player.data.up), 0)
        # pyxel.text(0, 32, str(self.player.data.currentFloor), 0)
        # pyxel.text(0,16, str(self.window[0].floor[0].jem.data.place),0)

    def windowChange(self):

    class Player:

        def __init__(self, y):
            self.y = y
            self.data = self.Database()

        def update(self, y, window, behindWindow):
            self.y = y
            self.data.currentFloor = int((self.data.y + 16) / 16 / 3)
            self.moveRL(self.data)
            self.moveUD(self.data)
            if self.data.currentFloor == floorNum - 1:
                if not behindWindow:
                    self.ladder(window.floor[self.data.currentFloor].ladder, 0)
                else:
                    self.ladder(window.floor[self.data.currentFloor].ladder, behindWindow.floor[0].ladder)
            else:
                self.ladder(window.floor[self.data.currentFloor].ladder, window.floor[self.data.currentFloor + 1].ladder)
            self.actionMove(self.data)

        def draw(self):
            # pyxel.text(0,  0, str(self.data.direction), 0)
            if self.data.direction == 0:
                ImageBank(self.data.x, self.y + self.data.y, 28)
            elif self.data.direction == 1:
                if self.data.action == 0:
                    ImageBank(self.data.x, self.y + self.data.y, 29)
                elif self.data.action % 6 < 3:
                    ImageBank(self.data.x, self.y + self.data.y, 30)
                else:
                    ImageBank(self.data.x, self.y + self.data.y, 31)
            elif self.data.direction == -1:
                if self.data.action == 0:
                    ImageBank(self.data.x, self.y + self.data.y, 32)
                elif self.data.action % 6 < 3:
                    ImageBank(self.data.x - 4, self.y + self.data.y, 33)
                else:
                    ImageBank(self.data.x - 4, self.y + self.data.y, 34)
                

        class Database:
            def __init__(self):
                self.place = pyxel.rndi(0, 13)
                self.life = 16
                self.x = windowSizeX / 2 - 8
                self.y = floorNum * 16 * 3 - 32
                self.direction = 0
                self.ladderUP = False
                self.ladderDOWN = False
                self.speed = 2
                self.up = 0
                self.currentFloor = int((self.y + 16) / 16 / 3)
                self.tempY = 0
                self.action = False

        def moveRL(self, data):
            if data.up == 0:
                if pyxel.btnp(pyxel.KEY_RIGHT, 1, 1):
                    data.x += data.speed
                    data.direction = 1
                    if data.x >= windowSizeX:
                        data.x -= windowSizeX
                if pyxel.btnp(pyxel.KEY_LEFT, 1, 1):
                    data.x -= data.speed
                    data.direction = -1
                    if data.x <= -12:
                        data.x += windowSizeX

        def moveUD(self, data):
            if pyxel.btnp(pyxel.KEY_UP, 1, 1):
                if data.up == 0 and data.ladderUP == True:
                    data.up = -1
                    data.tempY = data.y
                if data.up == 2 or data.up == -2:
                    data.up = -3
                    data.tempY = data.y
            if pyxel.btnp(pyxel.KEY_DOWN, 1, 1):
                if data.up == 0 and data.ladderDOWN == True:
                    data.up = 1
                    data.tempY = data.y
                if data.up == 2 or data.up == -2:
                    data.up = 3
                    data.tempY = data.y

            if data.up == -1:
                data.y -= 6
                if data.tempY - 32 >= data.y:
                    data.y = data.tempY - 32
                    data.up = -2
            elif data.up == -3:
                data.y -= 6
                if data.tempY - 16 >= data.y:
                    data.y = data.tempY - 16
                    data.up = 0
            elif data.up == 1:
                data.y += 6
                if data.tempY + 16 <= data.y:
                    data.y = data.tempY + 16
                    data.up = 2
            elif data.up == 3:
                data.y += 6
                if data.tempY + 32 <= data.y:
                    data.y = data.tempY + 32
                    data.up = 0

        def ladder(self, ladder, behindLadder):
            if self.data.up == 0 and ladder * 16 <= self.data.x and self.data.x <= ladder * 16 + 16:
                self.data.ladderUP = True
            else:
                self.data.ladderUP = False
            if self.data.up == 0 and behindLadder * 16 <= self.data.x and self.data.x <= behindLadder * 16 + 16:
                self.data.ladderDOWN = True
            else:
                self.data.ladderDOWN = False

        def actionMove(self, data):
            if data.up == 0:
                if pyxel.btnp(pyxel.KEY_SPACE, 1, 1):
                    data.action += 1
                else:
                    data.action = 0



    class Window:
        def __init__(self, y, windowNum):
            self.y = y;
            self.floor = []
            self.ladderSame = -1
            self.randomFloor = pyxel.rndi(0, 5)
            for i in range(floorNum):
                self.floor.append(self.Floor(self.y, windowNum, self.ladderSame, i, self.randomFloor))
                self.ladderSame = self.floor[i].ladder

        def update(self):
            for i in range(floorNum):
                self.floor[i].update(self.y)

        def draw(self):
            for i in range(floorNum):
                self.floor[i].draw(i)

        class Floor:
            def __init__(self, y, windowNum, ladderSame, floorNum,  randomFloor):
                self.y = y
                self.windowNum = windowNum
                self.floorNum = floorNum
                self.randomFloor = randomFloor
                self.same = []
                self.ladder = pyxel.rndi(0, 12)
                while self.ladder - 2 <= ladderSame and ladderSame <= self.ladder + 2:
                    self.ladder = pyxel.rndi(0, 12)
                self.same.append(self.ladder)
                self.fire = self.Static(self.y, self.same)
                self.same.append(self.fire.data.place)
                self.jem = self.Static(self.y, self.same)
                self.same.append(self.jem.data.place)
                if self.windowNum > 4 and self.floorNum == self.randomFloor:
                    self.item = self.Static(self.y, self.same)
                    self.same.append(self.item.data.place) #TODO いる？
                self.moveEnemy = []
                self.moveEnemy.append(self.Dynamic(self.y, self.same))

            def update(self, y):
                self.y = y
                self.fire.update(self.y)
                self.jem.update(self.y)
                if self.windowNum > 4 and self.floorNum == self.randomFloor:
                    self.item.update(self.y)
                for enemy in self.moveEnemy:
                    enemy.update(self.y)

            def draw(self, floorNum):
                for x in range(14):
                    if x == self.ladder:
                        ImageBank(x * 16, self.y + ((floorNum * 16 * 3) - 24), 12)
                    ImageBank(x * 16, self.y + ((floorNum * 16 * 3) + 16 * 2), 11)
                self.fire.draw(13, floorNum)
                self.jem.draw(16, floorNum)
                if self.windowNum > 4 and self.floorNum == self.randomFloor:
                    self.item.draw(19, floorNum)
                for enemy in self.moveEnemy:
                    if enemy.data.direction == -1:
                        enemy.draw(22, floorNum)
                    else:
                        enemy.draw(25, floorNum)


            class Static:
                def __init__(self, y, same):
                    self.y = y
                    self.data = self.Database(same)

                def update(self, y):
                    self.y = y

                def draw(self, image, num):
                    for x in range(14):
                        if self.data.place == x:
                            if self.data.life > 40:
                                ImageBank(x * 16, self.y + ((num * 16 * 3) -32), image)
                            elif self.data.life > 20:
                                ImageBank(x * 16, self.y + ((num * 16 * 3) -32), image + 1)
                            elif self.data.life > 0:
                                ImageBank(x * 16, self.y + ((num * 16 * 3) -32), image + 2)

                class Database:
                    def __init__(self, same):
                        self.place = pyxel.rndi(0, 13)
                        self.i = 0
                        while self.i != len(same):
                            for s in same:
                                if self.place != s and self.place != s + 1:
                                    self.i += 1
                                else:
                                    self.i = 0
                                    self.place = pyxel.rndi(0, 13)
                                    break
                        self.life = 30 * 2
                        self.x = self.place * 16
                        self.direction = pyxel.rndi(-1,1)
                        while self.direction == 0:
                            self.direction = pyxel.rndi(-1,1)
                        self.speed = pyxel.rndi(1, 2)


            class Dynamic(Static):

                def update(self, y):
                    super().update(y)
                    self.move()

                def draw(self, image, num):
                    if self.data.life > 40:
                        ImageBank(self.data.x, self.y + ((num * 16 * 3) -32 - 8), image)
                    elif self.data.life > 20:
                        ImageBank(self.data.x, self.y + ((num * 16 * 3) -32 - 8), image + 1)
                    elif self.data.life > 0:
                        ImageBank(self.data.x, self.y + ((num * 16 * 3) -32 - 8), image + 2)

                def move(self):
                    if self.data.direction == -1:
                        self.data.x -= self.data.speed
                    else:
                        self.data.x += self.data.speed
                    if self.data.x < -16:
                        self.data.x += windowSizeX
                    if self.data.x > windowSizeX:
                        self.data.x -= windowSizeX
                    if self.data.x % 100 == pyxel.rndi(1, 100):
                        self.data.direction *= -1

def ImageBank(x, y, num):
    # floorblue
    if num == 11:
        pyxel.blt(x, y, 1, 0, 0, 16, 16, 0)
    # ladder
    if num == 12:
        pyxel.blt(x, y, 1, 48, 0, 24, 56, 8)
    # fire(初期)
    if num == 13:
        pyxel.blt(x, y, 2, 0, 96, 16, 16, 0)
    # fire（後期）
    if num == 14 and num == 15:
        pyxel.blt(x, y, 2, 16, 96, 16, 16, 0)
    # jem(初期)
    if num == 16:
        pyxel.blt(x, y, 2, 0, 80, 16, 16, 0)
    # jem（後期）
    if num == 17 and num == 18:
        pyxel.blt(x, y, 2, 16, 80, 16, 16, 0)
    # item
    if 19 <= num and num <= 21:
        pyxel.blt(x, y, 2, 0, 112, 16, 16, 3)
    # enemy左向き（初期）
    if num == 22:
        moveOut(x, y, 0, 64, 16, 16, 16)
        pyxel.blt(x, y, 2, 0, 64, 16, 16, 0)
    # enemy左向き（初期）
    if num == 23:
        moveOut(x, y, 16, 64, 16, 16, 16)
        pyxel.blt(x, y, 2, 16, 64, 16, 16, 0)
    # enemy左向き（後期）
    if num == 24:
        moveOut(x, y, 32, 64, 16, 16, 16)
        pyxel.blt(x, y, 2, 32, 64, 16, 16, 0)
    # enemy右向き（初期）
    if num == 25:
        moveOut(x, y, 0, 48, 16, 16, 16)
        pyxel.blt(x, y, 2, 0, 48, 16, 16, 0)
    # enemy右向き（初期）
    if num == 26:
        moveOut(x, y, 16, 48, 16, 16, 16)
        pyxel.blt(x, y, 2, 16, 48, 16, 16, 0)
    # enemy右向き（後期）
    if num == 27:
        moveOut(x, y, 32, 48, 16, 16, 16)
        pyxel.blt(x, y, 2, 32, 48, 16, 16, 0)
    # player前向き
    if num == 28:
        moveOut(x, y, 0, 32, 16, 16, 12)
        pyxel.blt(x, y, 2, 0, 32, 16, 16, 0)
    # player右向き
    if num == 29:
        moveOut(x, y, 0, 0, 16, 16, 12)
        pyxel.blt(x, y, 2, 0, 0, 16, 16, 0)
    # 右向き action
    if num == 30:
        moveOut(x, y, 16, 0, 16, 16, 12)
        pyxel.blt(x, y, 2, 16, 0, 16, 16, 0)
    if num == 31:
        moveOut(x, y, 32, 0, 16, 16, 12)
        pyxel.blt(x, y, 2, 32, 0, 16, 16, 0)
    # player左向き
    if num == 32:
        moveOut(x, y, 0, 16, 16, 16, 12)
        pyxel.blt(x, y, 2, 0, 16, 16, 16, 0)
    if num == 33:
        moveOut(x, y, 16, 16, 16, 16, 12)
        pyxel.blt(x, y, 2, 16, 16, 16, 16, 0)
    if num == 34:
        moveOut(x, y, 32, 16, 16, 16, 12)
        pyxel.blt(x, y, 2, 32, 16, 16, 16, 0)
    if num == 100:
        pyxel.blt(0, 16 * 3 * floorNum, 1, 0, 16 * 9, 16 * 14, 100,  0)


def moveOut(x, y, ix, iy, iw ,ih,width):
    if -2 * width <= x and x <= 0:
        pyxel.blt(windowSizeX + x, y, 2, ix, iy, iw, ih, 0)
    if windowSizeX - 2 * width <= x and x <= windowSizeX:
        pyxel.blt(x - windowSizeX, y, 2, ix, iy, iw, ih, 0)


App()
