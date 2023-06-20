import random
import sys
from sys import argv, executable
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
import os

margin = 0
platforms = []
platforms_position = {}
platforms_count_start = 1
platforms_count = 1
y_platform = []
x1_platform = []
x2_platform = []
position = []
x_possition = 0
y_position = 0
a = "ф"
d = "в"

class Window(QMainWindow):
    def __init__(self):
        global x_possition
        global y_position
        global position
        global mass
        global speed
        global des_func
        super().__init__()
        self.x_position = 300
        self.y_position = 500
        position.append(x_possition)
        position.append(y_position)
        self.speed = 8
        self.mass = 1
        self.jump = True
        self.des_func = True

        self.fon = QLabel(self)
        self.fon.setStyleSheet('QLabel {border-image: url(C:/Users/User/Desktop/DJ/fon.jpg)}')
        self.fon_width = 500
        self.fon_height = 720
        self.fon.setGeometry(0, 0, self.fon_width, self.fon_height)


        res = QPushButton(self)
        res.setGeometry(5,5,40,40)
        res.setStyleSheet('QPushButton {border-image: url(C:/Users/User/Desktop/DJ/perezspusk.png)}')
        res.clicked.connect(self.restart)

        global platforms
        for p in range(7):
            platform = self.create_platform()
            platforms.append(platform)

        self.doodle = QLabel(self)
        self.doodle.setStyleSheet('QLabel {border-image: url(C:/Users/User/Desktop/DJ/zwezda.png)}')
        self.doodle_width = 40
        self.doodle_height = 40
        self.doodle.setGeometry(self.x_position, self.y_position, self.doodle_width, self.doodle_height)

        timerj = QTimer(self)
        timerj.start(40)
        timerj.timeout.connect(self.jump_doodle)
        timer2 = QTimer(self)
        timer2.start(1)
        timer2.timeout.connect(self.col2)
        timer3 = QTimer(self)
        timer3.start(1)
        timer3.timeout.connect(self.Hide_Unhide)

        self.setWindowIcon(QtGui.QIcon('C:/Users/User/Desktop/DJ/zwezda.png'))
        self.setFixedSize(500, 720)
        self.setWindowTitle('Doodle Jump')
        self.w_width = 500
        self.w_height = 720
        self.setGeometry(300, 100, self.w_width, self.w_height)

        self.endl = QLabel(self)
        self.endl.setStyleSheet('QLabel {border-image: url(C:/Users/User/Desktop/DJ/zwizdets.png)}')
        self.endl_width = 450
        self.endl_height = 300
        self.endl.setGeometry(25, 210, self.endl_width, self.endl_height)

    def create_platform(self):
        platform = QLabel(self)
        platform.setStyleSheet('border: 2px solid black; '
                               'background: ''#3EB489''; '
                               'max-width: 90px; '  
                               'max-height: 15px')
        global platforms_count
        global platforms_count_start
        global platforms_position
        global y_platform
        global x1_platform
        global x2_platform
        px = self.generate_px()
        x1_platform.append(px)
        px += 30
        x2_platform.append(px)
        py = self.generate_py()
        y_platform.append(py)
        platform.move(px, py)
        platforms_position[platforms_count] = [px, py]
        platforms_count += 1

        if platforms_count > 10:
            platforms_position.pop(platforms_count - 10)
            platforms_count_start += 1
        return platform

    def Hide_Unhide(self):
        y = self.doodle.y()
        if y >= 790:
            self.endl.show()
        else: self.endl.hide()
        return self.endl

    def generate_px(self):
        px = random.randint(30, 380)
        if platforms_count > 1:
            if list(reversed(platforms))[0].x() + 170 >= px >= list(reversed(platforms))[0].x() - 120:
                return self.generate_px()
            else:
                return px
        else:
            return px

    def generate_py(self):
        if platforms_count > 1:
            py = random.randint(list(reversed(platforms))[0].y() - 130, list(reversed(platforms))[0].y())
            if py >= list(reversed(platforms))[0].y() - 120:
                return self.generate_py()
            else:
                return py
        else:
            py = random.randint(590, 690)
            return py

    def jump_doodle(self):
        y = self.doodle.y()
        if self.jump:
            position = y
            force = self.mass * (self.speed ** 2)
            y -= force
            self.doodle.move(self.x_position, y)
            self.speed = self.speed -1
            on_platform = False
            for platform in platforms:
                if self.check_collision(platform):
                    on_platform = True
                    break
            if not on_platform:
                y += 8
                self.doodle.move(self.x_position, y)
        if self.speed < 0:
            self.mass = -1
        if self.speed == -90:
            self.speed = 45
            self.mass = 1
        global platforms_position
        y2 = self.doodle.y()
        if y2 <= 200:
            for p in range(len(platforms)):
                x = platforms[p].x()
                y1 = platforms[p].y()
                y1 += 30
                y2 += 15
                self.doodle.move(self.x_position, position)
                platforms[p].move(x, y1)
                platforms_position[p + 1] = [x, y1]
            global margin
            margin += 30
            if margin >= 90 and margin % 90 == 0:
                platform = self.create_platform()
                platform.show()
                platforms.append(platform)
    def col2(self):
        y = self.doodle.y()
        for i in range(len(platforms)):
            platform = platforms[i]
            if self.check_collision(platform):
                self.speed = 8
                self.mass = 1
                y = platform.y() - self.doodle_height
                break

    def check_collision(self, platform):
        doodle_rect = self.doodle.geometry()
        platform_rect = platform.geometry()
        return doodle_rect.intersects(platform_rect)
        if self.speed < 0:
            # отрицательная скорость
            self.mass = -1
        if self.speed == -90:
            self.jump = True
            self.speed = 8
            self.mass = 1

    def move_doodle(self, direction):
        if direction == 'left':
            self.x_position = self.x_position - 25
            self.doodle.move(self.x_position, self.doodle.y())
            if self.x_position < 500:
                self.x_position = self.x_position + 620
                self.doodle.move(self.x_position, self.doodle.y())
        if direction == 'right':
            self.x_position = self.x_position + 25
            self.doodle.move(self.x_position, self.doodle.y())
        if self.x_position > 500:
            self.x_position = self.x_position - 620
            self.doodle.move(self.x_position, self.doodle.y())

    def restart(self):
            os.execl(executable, os.path.abspath(__file__), *argv)

    def keyPressEvent(self, event):
        if event.text() == 'ф' or event.text() == 'a':
            self.move_doodle('left')
        if event.text() == 'в' or event.text() == 'd':
            self.move_doodle('right')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())