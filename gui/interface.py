from PySide6.QtWidgets import QApplication, QMainWindow
from gui.tabs import FaceTabs

def launch_app():
    app = QApplication([])
    window = QMainWindow()
    window.setWindowTitle("Reconocimiento Facial")
    window.setCentralWidget(FaceTabs())
    window.resize(600, 400)
    window.show()
    app.exec()
