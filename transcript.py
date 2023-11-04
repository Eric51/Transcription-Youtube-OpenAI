from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit
from PyQt5.QtCore import QThread, pyqtSignal
from docx import Document
import yt_dlp
import sys
import openai
import tempfile
import os
from pydub import AudioSegment

class TranscriptionThread(QThread):
    textReady = pyqtSignal(str)

    def run(self):
        url = self.url
        options = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
            }],
            'ffmpeg_location': 'C:\\ffmpeg\\bin',  # Remplacez ceci par le chemin absolu vers ffmpeg
            'outtmpl': 'audio',
            'quiet': True,
            'extract_info': True
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            self.title = info_dict.get('title', None)
            ydl.download([url])

        doc = Document()
        if self.title:
            doc.add_heading(self.title, 0)
        else:
            doc.add_heading('Transcription YouTube', 0)

        audio = AudioSegment.from_wav("audio.wav")
        segments = [audio[i:i+30000] for i in range(0, len(audio), 30000)]

        full_text = ""
        current_speaker = 1
        current_time_seconds = 0

        for idx, segment in enumerate(segments):
            minutes, seconds = divmod(current_time_seconds, 60)
            timestamp = f"{minutes:02d}:{seconds:02d}"

            temp_filename = tempfile.mktemp(".wav")
            segment.export(temp_filename, format="wav")

            openai.api_key = "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"
            with open(temp_filename, "rb") as audio_file:
                transcript = openai.Audio.transcribe("whisper-1", audio_file)

            text = transcript["text"]

            doc.add_paragraph(f"[{timestamp}] Orateur {current_speaker}: {text}")  
            self.textReady.emit(f"[{timestamp}] Orateur {current_speaker}: {text}")

            current_speaker = 1 if current_speaker == 2 else 2

            current_time_seconds += 30

            full_text += text + " "
            os.remove(temp_filename)

        # Sauvegarde du fichier avec le titre de la vidéo
        if self.title:
            doc.save(f"{self.title}.docx")
            self.textReady.emit(f"Transcription sauvegardée dans '{self.title}.docx'.")
        else:
            doc.save('Transcription.docx')
            self.textReady.emit("Transcription sauvegardée dans 'Transcription.docx'.")

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Transcripteur YouTube')
        layout = QVBoxLayout()

        self.urlInput = QLineEdit(self)
        self.urlInput.setPlaceholderText('Entrez l\'URL de la vidéo YouTube ici...')
        layout.addWidget(self.urlInput)

        self.transcribeButton = QPushButton('Transcrire', self)
        self.transcribeButton.clicked.connect(self.transcribe)
        layout.addWidget(self.transcribeButton)

        self.outputArea = QTextEdit(self)
        self.outputArea.setReadOnly(True)
        layout.addWidget(self.outputArea)

        self.setLayout(layout)
        self.show()

        self.transcriptionThread = TranscriptionThread()
        self.transcriptionThread.textReady.connect(self.updateText)

    def transcribe(self):
        url = self.urlInput.text()
        if not url:
            self.outputArea.setText('Veuillez entrer une URL.')
            return

        self.transcriptionThread.url = url
        self.transcriptionThread.start()

    def updateText(self, text):
        self.outputArea.append(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
