import cv2
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QTabWidget
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap, QImage

from core.face_logic import register_user, delete_user, recognize_face
from core.database import load_access_log

def convert_cv_qt(cv_img):
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    qt_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
    return QPixmap.fromImage(qt_img)

class RegisterTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre")
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("ID de usuario")
        self.register_button = QPushButton("Registrar")

        self.camera_label = QLabel()
        self.camera_label.setFixedSize(400, 300)

        layout.addWidget(self.name_input)
        layout.addWidget(self.id_input)
        layout.addWidget(self.camera_label)
        layout.addWidget(self.register_button)

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: No se pudo abrir la cámara.")
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.register_button.clicked.connect(self.save_face)
        self.current_frame = None

    def update_frame(self):
        if not self.cap.isOpened():
            return
        ret, frame = self.cap.read()
        if not ret or frame is None:
            print("No se pudo capturar frame válido en RegisterTab")
            self.current_frame = None
            return
        self.current_frame = frame.copy()
        self.camera_label.setPixmap(convert_cv_qt(frame))

    def save_face(self):
        name = self.name_input.text().strip()
        user_id = self.id_input.text().strip()
        if not name or not user_id:
            print("Ingrese nombre e ID válidos.")
            return
        if self.current_frame is None:
            print("No hay frame para registrar.")
            return
        success = register_user(name, user_id, self.current_frame)
        if success:
            print(f"Usuario {name} registrado con éxito.")
        else:
            print("Error al registrar usuario, no se detectó rostro.")

    def closeEvent(self, event):
        if self.cap.isOpened():
            self.cap.release()
        super().closeEvent(event)

class LoginTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        self.camera_label = QLabel()
        self.camera_label.setFixedSize(400, 300)

        layout.addWidget(self.camera_label)

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: No se pudo abrir la cámara.")
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        if not self.cap.isOpened():
            return
        ret, frame = self.cap.read()
        if not ret or frame is None:
            print("No se pudo capturar frame válido en LoginTab")
            return
        try:
            _, _, result_frame = recognize_face(frame)
            self.camera_label.setPixmap(convert_cv_qt(result_frame))
        except Exception as e:
            print("Error en recognize_face:", e)

    def closeEvent(self, event):
        if self.cap.isOpened():
            self.cap.release()
        super().closeEvent(event)

class DeleteTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre")
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("ID de usuario")
        self.delete_button = QPushButton("Eliminar Usuario")

        layout.addWidget(self.name_input)
        layout.addWidget(self.id_input)
        layout.addWidget(self.delete_button)

        self.delete_button.clicked.connect(self.delete_user)

    def delete_user(self):
        name = self.name_input.text().strip()
        user_id = self.id_input.text().strip()
        if not name or not user_id:
            print("Ingrese nombre e ID válidos para eliminar.")
            return
        delete_user(name, user_id)
        print(f"Usuario {name} eliminado.")

class HistoryTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        self.history_display = QTextEdit()
        self.history_display.setReadOnly(True)
        self.refresh_button = QPushButton("Refrescar Historial")

        layout.addWidget(self.history_display)
        layout.addWidget(self.refresh_button)

        self.refresh_button.clicked.connect(self.load_history)
        self.load_history()

    def load_history(self):
        log_entries = load_access_log()
        self.history_display.clear()
        for entry in log_entries:
            self.history_display.append(f"{entry['timestamp']} - {entry['name']} ({entry['user_id']})")

class FaceTabs(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(RegisterTab(), "Registrar")
        self.addTab(LoginTab(), "Ingresar")
        self.addTab(DeleteTab(), "Eliminar")
        self.addTab(HistoryTab(), "Historial")
