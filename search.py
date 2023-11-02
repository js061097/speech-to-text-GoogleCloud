import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from voice_handler import record_audio, transcribe_audio

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Desktop Assistant'
        self.left = 100
        self.top = 100
        self.width = 320
        self.height = 200
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        layout = QVBoxLayout()

        self.label = QLabel('Press the button and speak', self)
        layout.addWidget(self.label)

        self.button = QPushButton('Start Command', self)
        self.button.setFixedSize(200, 40)
        self.button.clicked.connect(self.on_click)
        layout.addWidget(self.button)

        self.setLayout(layout)
        self.show()

    def on_click(self):
        self.label.setText("Listening...")
        record_audio("recorded.wav")
        transcript = transcribe_audio("recorded.wav")
        self.label.setText(transcript)
        os.remove("recorded.wav")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
