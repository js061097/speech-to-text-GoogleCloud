import sys
import webbrowser
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit
from google.cloud import speech

class AssistantGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        # Set up the GUI layout
        self.button = QPushButton('Start Command', self)
        self.button.setFixedSize(150,40)
        self.button.move(100, 70)
        self.button.clicked.connect(self.startListening)

        self.textEdit = QTextEdit(self)
        self.textEdit.move(20, 150)
        self.textEdit.resize(300, 100)

        # Set window properties
        self.setGeometry(300, 300, 300, 250)
        self.setWindowTitle('Desktop Assistant')
        self.show()

    def startListening(self):
        # Function to handle voice command
        text = self.transcribeVoice()
        self.processCommand(text)

    def transcribeVoice(self):
        # Function to transcribe voice using Google Cloud Speech-to-Text
        client = speech.SpeechClient()
        # Add code to capture audio and transcribe
        # For simplicity, let's assume the transcription result is stored in `transcript`
        transcript = "search for Voice not recognized!"
        return transcript

    def processCommand(self, text):
        # Function to process the command and perform actions
        if 'search for' in text:
            query = text.split('search for')[-1].strip()
            url = f"https://www.google.com/search?q={query}"
            webbrowser.open(url)
            self.textEdit.setText(f"Searching for: {query}")
        else:
            self.textEdit.setText("Command not recognized.")

def main():
    app = QApplication(sys.argv)
    ex = AssistantGUI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
