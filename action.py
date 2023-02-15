import pyxel
import math
import webbrowser

windowSizeX = 16 * 14
windowSizeY = 16 * 3 * 6
floorNum = 6

class App:
    def __init__(self):
        pyxel.init(windowSizeX, windowSizeY + 100, fps=30)
        pyxel.load("action.pyxres")
        pyxel.play(1,10, loop=True)
        self.player = self.Player(0)
        self.currentWindow = 0
        self.window = []
        self.window.append(self.Window(0, 0))
        self.windowNum = 0
        self.changeSpeed = 8
        self.windowChange = 0
        self.gameMode = 0
        self.gameStarttime = 0
        pyxel.run(self.update, self.draw);

    def update(self):
        if self.windowChange == self.changeSpeed: self.window[self.currentWindow + 1].update(self.windowChange)
        self.window[self.currentWindow].update(self.windowChange)
        if self.currentWindow != 0: self.window[self.currentWindow - 1].update(self.windowChange)
        if self.gameMode == 0:
            if (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT, 1, 1) and (40 - 4 + 8 <= pyxel.mouse_x <= 40 - 4 + 8 + 16 * 7) and (106 + 16 * 5 <= pyxel.mouse_y <= 106 + 16 * 5 + 16)):
                self.gameMode = 1
        if self.gameMode == 1:
            if self.windowNum < self.currentWindow + 1:
                self.window.append(self.Window(-1 * windowSizeY, self.currentWindow + 1))
                self.windowNum += 1
            if self.currentWindow == 0:
                self.player.update(self.windowChange, self.window[self.currentWindow], 0)
            else:
                self.player.update(self.windowChange, self.window[self.currentWindow],  self.window[self.currentWindow - 1])
            self.windowMove(self.player.data)
            if self.player.data.life <= 0:
                self.gameMode = 2
        if self.gameMode == 2:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT, 1, 1) and (windowSizeX - 32 - 8 - 32 + 4 <= pyxel.mouse_x <= windowSizeX - 32 - 8 - 32 + 4 + 32) and (106 + 16 * 5 + 8 <= pyxel.mouse_y <= 106 + 16 * 5 + 8 + 16):
                template_link = "https://twitter.com/intent/tweet?text=PyxelGame%22iceClimber%22%E3%81%A7%E9%81%8A%E3%82%93%E3%81%A7%E3%81%BF%E3%81%9F%E3%82%88%EF%BC%81%0A%E7%A7%81%E3%81%AEscore%E3%81%AF{}%E7%82%B9%E3%81%A7%E3%81%97%E3%81%9F%EF%BC%81%0A%E4%B8%80%E7%B7%92%E3%81%AB%E9%81%8A%E3%82%93%E3%81%A7%E3%81%BF%E3%82%8B%E2%87%A9%0Ahttps%3A%2F%2Ftsola-20011118.github.io%2Ficecrimer%2F"
                webbrowser.open(template_link.format(self.player.data.score))
            if (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT, 1, 1) and (40 - 4 + 8 <= pyxel.mouse_x <= 40 - 4 + 8 + 16 * 9) and (106 + 16 * 7 <= pyxel.mouse_y <= 106 + 16 * 7 + 16)):
                self.player = self.Player(0)
                self.window = []
                self.window.append(self.Window(0, 0))
                self.currentWindow = 0
                self.windowNum = 0
                self.changeSpeed = 8
                self.windowChange = 0
                self.gameMode = 1
                self.gameStarttime = 0

    def draw(self):
        pyxel.cls(1);
        self.window[self.currentWindow].draw()
        if self.windowChange == self.changeSpeed: self.window[self.currentWindow + 1].draw()
        if self.currentWindow != 0: self.window[self.currentWindow - 1].draw()
        self.player.draw()
        if self.gameMode == 0:
            blty = self.gameStarttime * 10
            if blty > 106:
                if blty > 106 + 16 * (4 + 2 + 2 + 1):
                    blty =  106 + 16 * (4 + 2 + 2 + 1)
                pyxel.rect(32, 106, windowSizeX - 64, blty - 106, 7)
                if blty  > 106 + 16 * 4:
                    if blty > 106 + 16 * 4 + 16:
                        blty = 106 + 16 * 4 + 16
                    ImageBank(40 - 4 + 8, blty, 101)
                    ImageBank(40 - 4 + 8, blty + 16 * 2, 103)
                    if (40 - 4 + 8 <= pyxel.mouse_x <= 40 + 8 + 16 * 5) and (blty <= pyxel.mouse_y <= blty + 16):
                        ImageBank(40 - 4 + 8, blty, 102)
                    if (40 - 4 + 8 <= pyxel.mouse_x <= 40 + 8 + 16 * 9) and (blty + 32 <= pyxel.mouse_y <= blty + 48):
                        ImageBank(40 - 4 + 8, blty + 16 * 2, 104)
                if blty > 110:
                    blty = 110
            ImageBank(40 - 4, blty, 105)
            self.gameStarttime += 1
            pyxel.rect(pyxel.mouse_x - 1, pyxel.mouse_y - 1, 2, 2, 8)
        if self.gameMode == 1:
            self.Number(windowSizeX, windowSizeY)
            ImageBank(0, 0, (1000 + self.player.data.life))
        if self.gameMode == 2:
            blty = self.gameStarttime * 10
            if blty > 106:
                if blty > 106 + 16 * (4 + 2 + 2 + 1):
                    blty =  106 + 16 * (4 + 2 + 2 + 1)
                pyxel.rect(32, 106, windowSizeX - 64, blty - 106, 7)
                if blty  > 106 + 16 * 4:
                    if blty > 106 + 16 * 4 + 16:
                        blty = 106 + 16 * 4 + 16
                    ImageBank(40 - 4 + 8, blty - 8, 107)
                    self.Number(windowSizeX - 32 - 8 - 32, blty - 8 + 16 + 16)
                    ImageBank(windowSizeX - 32 - 8 - 32 + 4, blty - 8 + 16, 108)
                    ImageBank(40 - 4 + 8, blty + 16 * 2, 109)
                    if (40 - 4 + 8 <= pyxel.mouse_x <= 40 + 8 + 16 * 9) and (blty + 32 <= pyxel.mouse_y <= blty + 48):
                        ImageBank(40 - 4 + 8, blty + 16 * 2, 110)
                if blty > 110:
                    blty = 110
            ImageBank(40 - 4, blty, 106)
            self.gameStarttime += 1
            pyxel.rect(pyxel.mouse_x - 1, pyxel.mouse_y - 1, 2, 2, 8)
        ImageBank(0, 0, 100)
    def windowMove(self, data):
        if self.windowChange == 0:
            if data.y == -16:
                self.windowChange = self.changeSpeed
            if self.currentWindow != 0 and data.y > windowSizeY - 16:
                data.y = windowSizeY - 16
                self.windowChange = -1 * self.changeSpeed
        elif self.windowChange == self.changeSpeed:
            if data.y >= 16 * 3 * floorNum - 16:
                data.y = 16 * 3 * floorNum - 16
                self.currentWindow += 1
                self.windowChange = 0
        elif self.windowChange == -1 * self.changeSpeed:
            if data.y <= -16:
                data.tempY = -16
                data.y = 0
                self.currentWindow -= 1
                self.windowChange = 0

    def Number(self, x, y):
        score = str(self.player.data.score)
        digit = len(score)
        i = 0
        while i < digit:
            ImageBank(x - 16 * (int(digit) - int(i)), y - 16, int(score[i]))
            i += 1




    class Player:

        def __init__(self, y):
            self.y = y
            self.data = self.Database()
            self.time = 0

        def update(self, y, window, behindWindow):
            self.data.y += y
            if y == 0:
                self.data.currentFloor = int((self.data.y) / 16 / 3)
                self.actionMove(self.data)
                self.data.canMove = [True, True]
                if self.data.currentFloor != 5:
                    self.checkMove(self.data, window.floor[self.data.currentFloor + 1].jem.data)
                    self.actionBump(self.data, window.floor[self.data.currentFloor + 1].jem.data, 3, 100, 0)
                    self.actionBump(self.data, window.floor[self.data.currentFloor + 1].fire.data, 2, 0, 1)
                    self.enemyBump(self.data, window.floor[self.data.currentFloor + 1].fire.data, 2)
                    for enemy in window.floor[self.data.currentFloor + 1].moveEnemy:
                        self.enemyBump(self.data, enemy.data, 1)
                    for item in window.floor[self.data.currentFloor + 1].item:
                        self.actionBump(self.data, item.data, 30, 0, 0)
                if self.data.currentFloor == 5 and behindWindow:
                    self.checkMove(self.data, behindWindow.floor[0].jem.data)
                    self.actionBump(self.data, behindWindow.floor[0].jem.data, 3, 100, 0)
                    self.actionBump(self.data, behindWindow.floor[0].fire.data, 2, 0, 1)
                    self.enemyBump(self.data, behindWindow.floor[0].fire.data, 2)
                    for enemy in behindWindow.floor[0].moveEnemy:
                        self.enemyBump(self.data, enemy.data, 1)
                    for item in behindWindow.floor[0].item:
                        self.actionBump(self.data, item.data, 30, 0, 0)
                self.moveRL(self.data)
                self.moveUD(self.data)
                if self.data.currentFloor == floorNum - 1:
                    if not behindWindow:
                        self.ladder(window.floor[self.data.currentFloor].ladder, 0)
                    else:
                        self.ladder(window.floor[self.data.currentFloor].ladder, behindWindow.floor[0].ladder)
                else:
                    self.ladder(window.floor[self.data.currentFloor].ladder, window.floor[self.data.currentFloor + 1].ladder)
                if self.data.canBaster == True:
                    self.time += 1
                    if self.time >= 1200:
                        self.data.canBaster = False

        def draw(self):
            if self.data.direction == 0:
                ImageBank(self.data.x, self.y + self.data.y, 28)
            elif self.data.up != 0:
                ImageBank(self.data.x, self.y + self.data.y, 35)
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
                self.life = 100
                self.x = windowSizeX / 2 - 8
                self.y = floorNum * 16 * 3 - 32
                self.direction = 0
                self.ladderUP = False
                self.ladderDOWN = False
                self.speed = 2
                self.up = 0
                self.currentFloor = int((self.y) / 16 / 3)
                self.tempY = 0
                self.action = False
                self.canMove = [True, True]
                self.score = 0
                self.canBaster = False

        def moveRL(self, data):
            if data.up == 0:
                if pyxel.btnp(pyxel.KEY_RIGHT, 1, 1):
                    if data.canMove[1]:
                        data.x += data.speed
                    data.direction = 1
                    if data.x >= windowSizeX:
                        data.x -= windowSizeX
                if data.canMove[0] and pyxel.btnp(pyxel.KEY_LEFT, 1, 1):
                    if data.canMove[0]:
                        data.x -= data.speed
                    data.direction = -1
                    if data.x <= -12:
                        data.x += windowSizeX

        def moveUD(self, data):
            if pyxel.btnp(pyxel.KEY_UP, 1, 1):
                if data.up == 0 and data.ladderUP == True:
                    data.up = -1
                    data.tempY = data.y
                    pyxel.play(0, 0, loop=False)
                if data.up == 2 or data.up == -2:
                    data.up = -3
                    data.tempY = data.y
                    pyxel.play(0, 0, loop=False)
            if pyxel.btnp(pyxel.KEY_DOWN, 1, 1):
                if data.up == 0 and data.ladderDOWN == True:
                    data.up = 1
                    data.tempY = data.y
                    pyxel.play(0, 1, loop=False)
                if data.up == 2 or data.up == -2:
                    data.up = 3
                    data.tempY = data.y
                    pyxel.play(0, 1, loop=False)

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
            if self.data.up == 0 and ladder * 16 - 8 <= self.data.x and self.data.x <= ladder * 16 + 16:
                self.data.ladderUP = True
            else:
                self.data.ladderUP = False
            if self.data.up == 0 and behindLadder * 16 - 8 <= self.data.x and self.data.x <= behindLadder * 16 + 16:
                self.data.ladderDOWN = True
            else:
                self.data.ladderDOWN = False

        def actionMove(self, data):
            if data.up == 0:
                if pyxel.btnp(pyxel.KEY_SPACE, 1, 1):
                    if data.action % 20 == 0:
                        pyxel.play(0, 2, loop=False)
                    data.action += 1
                else:
                    data.action = 0

        def actionBump(self, player, sum, damege, score, life):
            if sum.aliveFlag == True and player.action != 0:
                if player.x < sum.x and player.x + player.speed + 12 + 8 > sum.x:
                    sum.life -= damege
                if player.x > sum.x and player.x - player.speed - 4 < sum.x + 16:
                    sum.life -= damege
                if sum.life < 0:
                    player.score += score
                    player.life += life
                    pyxel.play(0, 3, loop=False)
                    sum.aliveFlag = False
                    if damege == 30:
                        player.canBaster = True
                        self.time = 0

        def checkMove(self, data, jem):
            if data.x < jem.x and data.x + data.speed + 12 > jem.x and jem.life >= 0:
                data.canMove[1] = False
            else:
                data.canMove[1] = True
            if data.x > jem.x and data.x - data.speed < jem.x + 16 and jem.life >= 0:
                data.canMove[0] = False
            else:
                data.canMove[0] = True
            # pass

        def enemyBump(self, player, sum, damege):
            if sum.aliveFlag == True and (player.y / 16) % 3 == 1:
                if player.x > sum.x - 8 and player.x < sum.x + 12:
                    if player.canBaster == True and damege == 1:
                        sum.life = 20
                        sum.aliveFlag = False
                        pyxel.play(0, 5, loop=False)
                    else:
                        player.life -= damege
                        pyxel.play(0, 4, loop=False)
                        sum.aliveFlag = False
                        sum.life = 0

    class Window:
        def __init__(self, y, windowNum):
            self.y = y;
            self.floor = []
            self.ladderSame = -1
            self.randomFloor = pyxel.rndi(1,5)
            for i in range(floorNum):
                self.floor.append(self.Floor(self.y, windowNum, self.ladderSame, i, self.randomFloor))
                self.ladderSame = self.floor[i].ladder

        def update(self, y):
            self.y += y
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
                self.item =[]
                self.moveEnemy = []
                if self.windowNum > 5 and self.floorNum == self.randomFloor:
                    self.item.append(self.Static(self.y, self.same))
                    self.same.append(self.item[0].data.place)
                self.moveEnemy.append(self.Dynamic(self.y, self.same))
                if self.windowNum > 2:
                    self.moveEnemy.append(self.Dynamic(self.y, self.same))

            def update(self, y):
                self.y = y
                self.fire.update(self.y)
                self.jem.update(self.y)
                for item in self.item:
                    item.update(self.y)
                for enemy in self.moveEnemy:
                    enemy.update(self.y)

            def draw(self, floorNum):
                for x in range(14):
                    if x == self.ladder:
                        ImageBank(x * 16, self.y + ((floorNum * 16 * 3) - 24), 12)
                    ImageBank(x * 16, self.y + ((floorNum * 16 * 3) + 16 * 2), 11)
                self.fire.draw(13, floorNum)
                self.jem.draw(16, floorNum)
                for item in self.item:
                    item.draw(19, floorNum)
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
                        self.place = pyxel.rndi(0, 12)
                        self.i = 0
                        while self.i != len(same):
                            for s in same:
                                if self.place != s and self.place != s + 1:
                                    self.i += 1
                                else:
                                    self.i = 0
                                    self.place = pyxel.rndi(0, 12)
                                    break
                        self.life = 30 * 2
                        self.aliveFlag = True
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
                    elif self.data.life >= 20:
                        ImageBank(self.data.x, self.y + ((num * 16 * 3) -32 - 8), image + 1)
                        self.data.life -= 2
                    elif self.data.life > 0:
                        self.data.life -= 2
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
                    if self.data.x % 70 == pyxel.rndi(1, 70):
                        self.data.direction *= -1

def ImageBank(x, y, num):
    if num >= 0 and num <= 9:
        pyxel.blt(x, y, 0, 16 * num, 0, 16, 16, 0)
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
    if num == 14 or num == 15:
        pyxel.blt(x, y, 2, 16, 96, 16, 16, 0)
    # jem(初期)
    if num == 16:
        pyxel.blt(x, y, 2, 0, 80, 16, 16, 0)
    # jem（後期）
    if num == 17 or num == 18:
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
    if num == 35:
        moveOut(x, y, 32, 32, 16, 16, 12)
        pyxel.blt(x, y, 2, 32, 32, 16, 16, 0)
    if num == 100:
        pyxel.blt(0, 16 * 3 * floorNum, 1, 0, 16 * 9, 16 * 14, 100,  0)
    #play
    if num == 101:
        pyxel.blt(x, y, 0, 0, 16,  16, 16, 3)
        pyxel.blt(x + 16, y, 0, 16 * 3, 16,  16 * 4, 16, 3)
    if num == 102:
        pyxel.blt(x, y, 0, 0, 32,  16, 16, 3)
        pyxel.blt(x + 16, y, 0, 16 * 3, 32,  16 * 4, 16, 3)
    #tutorial
    if num == 103:
        pyxel.blt(x, y, 0, 0, 16,  16, 16, 3)
        pyxel.blt(x + 16, y, 0, 16 * 7, 16,  16 * 8, 16, 3)
    if num == 104:
        pyxel.blt(x, y, 0, 0, 32,  16, 16, 3)
        pyxel.blt(x + 16, y, 0, 16 * 7, 32,  16 * 8, 16, 3)
    if num == 105:
        pyxel.blt(x, y, 0, 0, 48,  16 * 10 - 8, 16 * 4, 3)
    if num == 106:
        pyxel.blt(x, y, 0, 0, 16 * (3 + 4),  16 * 10 - 8, 16 * 4, 3)
    if num == 107:
        pyxel.blt(x, y, 0, 16 * (9.5), 16 * 3,  16 * 4, 16, 3)
        pyxel.blt(x + 16 * 4, y, 0, 16 * (9.5), 16 * 4,  16 * 5, 16, 3)
    if num == 108:
        pyxel.blt(x, y, 0, 16 * 13, 0,  32, 16, 8)
    if num == 109:
        pyxel.blt(x, y, 0, 0, 16,  16 * 7 , 16, 3)
    if num == 110:
        pyxel.blt(x, y, 0, 0, 32,  16 * 7, 16, 3)
    if num > 1000:
        temp = num - 1000
        for i in range(temp):
            pyxel.blt(x + i * 16, y, 0, 16 * 10,0,  16, 16, 0)

def moveOut(x, y, ix, iy, iw ,ih,width):
    if -2 * width <= x and x <= 0:
        pyxel.blt(windowSizeX + x, y, 2, ix, iy, iw, ih, 0)
    if windowSizeX - 2 * width <= x and x <= windowSizeX:
        pyxel.blt(x - windowSizeX, y, 2, ix, iy, iw, ih, 0)


App()
