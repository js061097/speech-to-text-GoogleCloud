import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
import pyaudio
import wave
import os
from google.cloud import speech

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
        
        # Create a QVBoxLayout instance
        layout = QVBoxLayout()

        # Create label
        self.label = QLabel('Press the button and speak', self)
        layout.addWidget(self.label)

        # Create a button in the window
        self.button = QPushButton('Start Command', self)
        self.button.setFixedSize(200, 40)
        
        # Connect button to function on_click
        self.button.clicked.connect(self.on_click)
        layout.addWidget(self.button)

        # Set the layout for the main window
        self.setLayout(layout)

        self.show()

    def on_click(self):
        self.label.setText("Listening...")
        self.record_audio("recorded.wav")
        transcript = self.transcribe_audio("recorded.wav")
        self.label.setText(transcript)
        os.remove("recorded.wav")  # Clean up the recorded file

    def record_audio(self, output_file):
        # Set chunk size of 1024 samples per data frame
        chunk = 1024  
        # 16 bit rate
        sample_format = pyaudio.paInt16  
        channels = 1
        fs = 44100  # Record at 44100 samples per second
        seconds = 5  # Duration of recording

        p = pyaudio.PyAudio()  # Create an interface to PortAudio

        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)

        frames = []  # Initialize array to store frames

        # Store data in chunks for 5 seconds
        for i in range(0, int(fs / chunk * seconds)):
            data = stream.read(chunk)
            frames.append(data)

        # Stop and close the stream 
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        p.terminate()

        # Save the recorded data as a WAV file
        wf = wave.open(output_file, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()

    def transcribe_audio(self, audio_file):
        client = speech.SpeechClient()

        with open(audio_file, "rb") as audio:
            content = audio.read()

        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=44100,
            language_code="en-US",
        )

        response = client.recognize(config=config, audio=audio)

        transcript = ""
        for result in response.results:
            transcript += result.alternatives[0].transcript

        return transcript

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
