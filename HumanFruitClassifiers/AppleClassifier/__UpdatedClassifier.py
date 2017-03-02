
# Copyright (c) 2017, Brendon Matusch. All rights reserved
# __UpdatedClassifier.py

# This program is the human interface used in sorting fruit. It displays one image at a time on screen beside eight example images. When the user presses a number key 1-8, the image is updated and data is written to __Output.csv.

import sys
from PyQt5.QtWidgets import QLabel, QWidget, QApplication
from PyQt5.QtGui import QPixmap, QPalette
from PyQt5.QtCore import Qt

class ImageClassifier(QWidget):

    i = 0
    lbl = None
    f = open("__Output.csv", "w")
    completion = None
    total = 2141
    prefix = "HalfApple"

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.update_ui()

    def init_ui(self):

        xmplImg0 = QPixmap("_ex0.png")
        xmplImg1 = QPixmap("_ex1.png")
        xmplImg2 = QPixmap("_ex2.png")
        xmplImg3 = QPixmap("_ex3.png")
        xmplImg4 = QPixmap("_ex4.png")
        xmplImg5 = QPixmap("_ex5.png")
        xmplImg6 = QPixmap("_ex6.png")
        xmplImg7 = QPixmap("_ex7.png")

        self.setFixedSize(1536, 544)

        self.lbl = QLabel(self)
        self.lbl.setFixedSize(512, 512)
        lbl0 = QLabel(self)
        lbl0.setFixedSize(256, 256)
        lbl1 = QLabel(self)
        lbl1.setFixedSize(256, 256)
        lbl2 = QLabel(self)
        lbl2.setFixedSize(256, 256)
        lbl3 = QLabel(self)
        lbl3.setFixedSize(256, 256)
        lbl4 = QLabel(self)
        lbl4.setFixedSize(256, 256)
        lbl5 = QLabel(self)
        lbl5.setFixedSize(256, 256)
        lbl6 = QLabel(self)
        lbl6.setFixedSize(256, 256)
        lbl7 = QLabel(self)
        lbl7.setFixedSize(256, 256)
        self.completion = QLabel(self)
        self.completion.setFixedSize(1536, 32)
        self.completion.setAlignment(Qt.AlignCenter)

        lbl0.setPixmap(xmplImg0)
        lbl1.setPixmap(xmplImg1)
        lbl2.setPixmap(xmplImg2)
        lbl3.setPixmap(xmplImg3)
        lbl4.setPixmap(xmplImg4)
        lbl5.setPixmap(xmplImg5)
        lbl6.setPixmap(xmplImg6)
        lbl7.setPixmap(xmplImg7)

        self.lbl.move(0, 0)
        lbl0.move(512, 0)
        lbl1.move(768, 0)
        lbl2.move(1024, 0)
        lbl3.move(1280, 0)
        lbl4.move(512, 256)
        lbl5.move(768, 256)
        lbl6.move(1024, 256)
        lbl7.move(1280, 256)
        self.completion.move(0, 512)

        palette = QPalette()
        palette.setColor(QPalette.Background, Qt.white)
        palette.setColor(QPalette.Foreground, Qt.black)
        self.completion.setPalette(palette)

        self.move(0, 0)
        self.setWindowTitle('Fruit Classifier')
        self.show()

    def update_ui(self):
        self.i += 1
        self.mainImg = QPixmap(self.prefix + " (" + str(self.i) + ")")
        self.lbl.setPixmap(self.mainImg)
        self.completion.setText("Done " + str(self.i) + " of " + str(self.total))

    def keyPressEvent(self, e):

        if e.key() == Qt.Key_1:
            n = 1
        elif e.key() == Qt.Key_2:
            n = 2
        elif e.key() == Qt.Key_3:
            n = 3
        elif e.key() == Qt.Key_4:
            n = 4
        elif e.key() == Qt.Key_5:
            n = 5
        elif e.key() == Qt.Key_6:
            n = 6
        elif e.key() == Qt.Key_7:
            n = 7
        elif e.key() == Qt.Key_8:
            n = 8
        else:
            return
        self.f.write(str(self.i) + "," + str(n) + "\n")
        if self.i >= self.total:
            self.f.close()
            sys.exit()
        self.update_ui()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ic = ImageClassifier()
    sys.exit(app.exec_())
