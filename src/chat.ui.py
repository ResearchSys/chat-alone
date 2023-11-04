import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import QPalette, QColor, QTextCursor
from BlurWindow.blurWindow import blur
import time

from utils import Context

class CustomLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(CustomLineEdit, self).__init__(parent)
        self.setStyleSheet("border: none; color: white; font-size: 14px;")

class Worker(QThread):
    finished = Signal(str)

    def __init__(self, user_input):
        super(Worker, self).__init__()
        self.user_input = user_input

    def run(self):
        time.sleep(2)
        response = Context().chat(self.user_input)
        self.finished.emit(response)

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        system_palette = QPalette()
        system_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        system_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        system_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        system_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        system_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 220))
        system_palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
        system_palette.setColor(QPalette.Text, QColor(255, 255, 255))
        system_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        system_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        system_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        system_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        system_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        system_palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        self.setPalette(system_palette)

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(500, 400)

        self.text_input = CustomLineEdit(self)
        self.text_input.setGeometry(10, 10, 480, 30)

        self.text_output = QTextEdit(self)
        self.text_output.setGeometry(10, 50, 480, 300)
        self.text_output.setReadOnly(True)
        self.text_output.setStyleSheet("border: none; color: white; font-size: 13px")
        self.text_output.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.conversation_history = QTextEdit(self)
        self.conversation_history.setGeometry(10, 150, 480, 300)
        self.conversation_history.setReadOnly(True)
        self.conversation_history.setStyleSheet("border: none; color: white; font-size: 13px")
        self.conversation_history.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.text_input.returnPressed.connect(self.process_user_input)

        blur(self.winId())

        self.setStyleSheet("background-color: rgba(0, 0, 0, 0)")

        self.worker = None
        self.response_timer = QTimer(self)
        self.response_text = ""
        self.conversation_history_text = ""  # Variável para armazenar o histórico da conversa

        # Carregue o histórico da conversa quando o aplicativo é iniciado
        self.load_conversation_history()

    def process_user_input(self):
        user_input = self.text_input.text()
        if not self.worker:
            self.worker = Worker(user_input)
            self.worker.finished.connect(self.display_response)
            self.worker.start()

            # Adicione o texto de entrada do usuário ao histórico
            self.conversation_history_text += f"🐧 {user_input}\n"
            self.conversation_history.setPlainText(self.conversation_history_text)

            self.text_output.append("🐧 " + user_input)
            self.animate_processing(user_input)

        self.text_input.clear()

    def animate_processing(self, user_input):
        animation_text = "Processando"
        for i in range(15):
            animation_text += "."
            self.text_output.setPlainText("🐧 " + user_input + "\n" + animation_text)
            QApplication.processEvents()
            time.sleep(0.1)

    def display_response(self, response):
        self.text_output.clear()
        user_input = self.text_input.text()
        self.conversation_history_text += f"🐧 {user_input}\n🐼 {response}\n"
        self.conversation_history.setPlainText(self.conversation_history_text)
        self.response_text = response
        self.response_timer.timeout.connect(self.show_next_letter)
        self.response_timer.start(50)

    def show_next_letter(self):
        if self.response_text:
            cursor = QTextCursor(self.text_output.textCursor())
            cursor.movePosition(QTextCursor.End)
            cursor.insertText(self.response_text[0])
            self.response_text = self.response_text[1:]
        else:
            self.response_timer.stop()
            self.worker.quit()
            self.worker.wait()
            self.worker = None

    def load_conversation_history(self):
        # Carregue o histórico da conversa anterior aqui, se aplicável
        history = []
        self.conversation_history_text = "\n".join(history)
        self.conversation_history.setPlainText(self.conversation_history_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
