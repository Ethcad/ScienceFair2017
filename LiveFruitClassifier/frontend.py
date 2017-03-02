import sys
import cv2
from os import system, path
from PyQt5.QtWidgets import QLabel, QWidget, QApplication, QPushButton
from PyQt5.QtGui import QPixmap, QPalette, QImage, QFont
from PyQt5.QtCore import Qt
from threading import Thread, Event

class TimerThread(Thread):

    front_end = None

    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        while not self.stopped.wait(0.02):
            FrontEnd.update_ui(self.front_end)


class FrontEnd (QWidget):

    using_banana = True
    take_picture = False
    results_pending = False

    banana_class_meanings = ['fairly good!',
                             'fairly good!',
                             'a little past its prime.',
                             'over-ripe.',
                             'probably inedible.',
                             'inedible.',
                             'in later stages of decomposition.',
                             'absolutely disgusting!']

    apple_class_meanings = ['almost perfect!',
                            'fairly good!',
                            'edible.',
                            'over-ripe.',
                            'probably inedible.',
                            'inedible.',
                            'in later stages of decomposition.',
                            'absolutely disgusting!']

    def __init__(self):
        super().__init__()

        if self.using_banana:
            self.class_meanings = self.banana_class_meanings
        else:
            self.class_meanings = self.apple_class_meanings

        self.init_ui()

        stop_flag = Event()
        timer_thread = TimerThread(stop_flag)
        timer_thread.daemon = True
        timer_thread.start()
        timer_thread.front_end = self

    def init_ui(self):
        font = QFont('Source Sans Pro', 30)

        self.details_button = QPushButton('View raw output', self)
        self.details_button.setToolTip('View neural network\'s raw classification of image')
        self.details_button.setFixedSize(400, 60)
        self.details_button.move(20, 815)
        self.details_button.setFont(font)
        self.details_button.clicked.connect(self.view_details)
        self.details_button.setEnabled(False)

        classify_button = QPushButton('Classify image', self)
        classify_button.setToolTip('Capture image and display classification')
        classify_button.setFixedSize(400, 60)
        classify_button.move(440, 815)
        classify_button.setFont(font)
        classify_button.clicked.connect(self.take_picture_button)

        exit_button = QPushButton('Exit application', self)
        exit_button.setFixedSize(400, 60)
        exit_button.move(860, 815)
        exit_button.setFont(font)
        exit_button.clicked.connect(self.exit_program)

        self.cam_capture = cv2.VideoCapture(0)
        self.cam_capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.cam_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cam_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        palette = QPalette()
        palette.setColor(QPalette.Foreground, Qt.white)
        palette.setColor(QPalette.Background, Qt.darkGray)

        self.setFixedSize(1280, 940)
        self.move(100, 100)
        self.setWindowTitle('Live Fruit Classifier')
        self.setPalette(palette)

        self.user_prompt = QLabel(self)
        self.user_prompt.setAlignment(Qt.AlignCenter)
        self.user_prompt.setFixedSize(1280, 60)
        self.user_prompt.move(0, 880)
        self.user_prompt.setText('Click "Classify image" when ready')
        self.user_prompt.setPalette(palette)
        self.user_prompt.setFont(font)

        title = QLabel(self)
        title.setAlignment(Qt.AlignCenter)
        title.setFixedSize(1280, 60)
        title.move(0, 10)
        title.setText('Live Fruit Classifier')
        title.setPalette(palette)
        title.setFont(font)

        self.video_frame = QLabel(self)
        self.video_frame.setAlignment(Qt.AlignCenter)
        self.video_frame.setFixedSize(1280, 720)
        self.video_frame.move(0, 75)

        self.show()

    def update_ui(self):
        ret, frame = self.cam_capture.read()

        if self.results_pending:
            if not path.isfile('output2.jpg'):
                self.results_pending = False
                with open('.out') as content_file:
                    l = content_file.readlines()
                    self.handle_image_classification(l[2].strip(), l[3].strip())

        if self.take_picture:
            cv2.imwrite('output2.jpg', frame)
            self.user_prompt.setText('Please wait...')
            system('convert -modulate 125,125,100 output2.jpg output.jpg && ./classifyimage.py --nogpu --mean mean.binaryproto --labels labels.txt model.caffemodel deploy.prototxt output.jpg > .out && cp output.jpg output1.jpg && rm output.jpg output2.jpg')
            self.take_picture = False
            self.results_pending = True

        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888).rgbSwapped()
        pix = QPixmap.fromImage(image)
        self.video_frame.setPixmap(pix)

    def handle_image_classification(self, raw_output_line_0, raw_output_line_1):
        line_0_val = float(int(raw_output_line_0[12]))
        line_1_val = float(int(raw_output_line_1[12]))
        line_0_weight = float(raw_output_line_0[:-7].strip()) / 100
        line_1_weight = float(raw_output_line_1[:-7].strip()) / 100
        factor = 1 / (line_0_weight + line_1_weight)
        line_0_val *= line_0_weight * factor
        line_1_val *= line_1_weight * factor
        class_val = int(round(line_0_val + line_1_val)) - 1

        if self.using_banana:
            word = "banana"
        else:
            word = "apple"

        self.details_button.setEnabled(True)
        self.user_prompt.setText('The last classified ' + word + ' was ' + self.class_meanings[class_val])

    def exit_program(self):
        sys.exit()

    def view_details(self):
        system('gedit .out')

    def take_picture_button(self):
        if not self.results_pending:
            self.take_picture = True

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ic = FrontEnd()
    sys.exit(app.exec_())
