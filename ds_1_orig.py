import sys
import cv2
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QPushButton, QSlider, QLabel, QScrollArea, QMessageBox
)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtMultimedia import QMediaDevices


class CameraApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("USB Camera Viewer")
        self.setMinimumSize(800, 600)

        # Переменные состояния
        self.capture = None          # объект VideoCapture OpenCV
        self.timer = QTimer()        # таймер для обновления кадров
        self.is_streaming = False    # идёт ли трансляция
        self.scale_factor = 1.0      # текущий масштаб
        self.last_qimage = None      # последний полученный кадр (для масштабирования на паузе)

        # Создание интерфейса
        self.init_ui()

        # Заполнение списка камер
        self.populate_cameras()

        # Автоматический запуск первой камеры, если она есть
        if self.combo.count() > 0:
            self.combo.setCurrentIndex(0)
            self.start_stream()

        # Подключение таймера
        self.timer.timeout.connect(self.update_frame)

    def init_ui(self):
        """Инициализация виджетов и компоновка"""
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # Строка выбора камеры
        cam_layout = QHBoxLayout()
        cam_layout.addWidget(QLabel("Камера:"))
        self.combo = QComboBox()
        cam_layout.addWidget(self.combo)
        main_layout.addLayout(cam_layout)

        # Кнопки управления
        btn_layout = QHBoxLayout()
        self.btn_start = QPushButton("▶ Старт")
        self.btn_stop = QPushButton("⏸ Стоп")
        btn_layout.addWidget(self.btn_start)
        btn_layout.addWidget(self.btn_stop)
        main_layout.addLayout(btn_layout)

        # Ползунок масштаба
        zoom_layout = QHBoxLayout()
        zoom_layout.addWidget(QLabel("Масштаб:"))
        self.slider_zoom = QSlider(Qt.Horizontal)
        self.slider_zoom.setMinimum(10)   # 0.1 * 100
        self.slider_zoom.setMaximum(300)  # 3.0 * 100
        self.slider_zoom.setValue(100)
        self.slider_zoom.setTickInterval(10)
        self.zoom_label = QLabel("1.0x")
        zoom_layout.addWidget(self.slider_zoom)
        zoom_layout.addWidget(self.zoom_label)
        main_layout.addLayout(zoom_layout)

        # Область для отображения видео (с прокруткой)
        self.scroll_area = QScrollArea()
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet("background-color: black;")
        self.scroll_area.setWidget(self.video_label)
        self.scroll_area.setWidgetResizable(False)  # чтобы появлялись полосы прокрутки
        main_layout.addWidget(self.scroll_area)

        # Подключение сигналов
        self.btn_start.clicked.connect(self.start_stream)
        self.btn_stop.clicked.connect(self.stop_stream)
        self.slider_zoom.valueChanged.connect(self.zoom_changed)
        self.combo.currentIndexChanged.connect(self.on_camera_changed)

    def populate_cameras(self):
        """Получение списка всех видеоустройств через QtMultimedia"""
        devices = QMediaDevices.videoInputs()
        for device in devices:
            self.combo.addItem(device.description())
        if self.combo.count() == 0:
            QMessageBox.warning(self, "Нет камер", "Не найдено ни одной USB-камеры.")

    def on_camera_changed(self, index):
        """Обработка смены камеры в комбобоксе"""
        if index < 0:
            return
        # Останавливаем текущую трансляцию
        self.stop_stream()
        # Освобождаем старую камеру
        if self.capture is not None:
            self.capture.release()
            self.capture = None
        # Очищаем последний кадр
        self.last_qimage = None
        self.video_label.clear()
        # Пытаемся открыть новую камеру и запустить трансляцию
        self.capture = cv2.VideoCapture(index)
        if not self.capture.isOpened():
            QMessageBox.warning(self, "Ошибка", f"Не удалось открыть камеру: {self.combo.currentText()}")
            self.capture = None
        else:
            self.start_stream()

    def start_stream(self):
        """Запуск или возобновление трансляции"""
        # Если камера ещё не открыта, пробуем открыть
        if self.capture is None or not self.capture.isOpened():
            idx = self.combo.currentIndex()
            if idx < 0:
                QMessageBox.warning(self, "Ошибка", "Камера не выбрана")
                return
            self.capture = cv2.VideoCapture(idx)
            if not self.capture.isOpened():
                QMessageBox.warning(self, "Ошибка", "Не удалось открыть камеру")
                return
        # Запускаем поток кадров, если он ещё не активен
        if not self.is_streaming:
            self.is_streaming = True
            self.timer.start(30)  # ~33 fps

    def stop_stream(self):
        """Остановка трансляции (кадры не читаются, камера остаётся открытой)"""
        self.is_streaming = False
        self.timer.stop()

    def zoom_changed(self, value):
        """Обработка изменения ползунка масштаба"""
        self.scale_factor = value / 100.0
        self.zoom_label.setText(f"{self.scale_factor:.1f}x")
        self.redisplay_last_frame()   # применяем новый масштаб к текущему кадру

    def redisplay_last_frame(self):
        """Перерисовка последнего кадра с новым масштабом (для паузы)"""
        if self.last_qimage is not None:
            pixmap = QPixmap.fromImage(self.last_qimage)
            self.display_pixmap(pixmap)

    def display_pixmap(self, pixmap):
        """Масштабирование pixmap и отображение в QLabel с учётом прокрутки"""
        if pixmap.isNull():
            return
        w = int(pixmap.width() * self.scale_factor)
        h = int(pixmap.height() * self.scale_factor)
        scaled = pixmap.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.video_label.setPixmap(scaled)
        self.video_label.resize(scaled.size())  # важно для работы ScrollArea

    def update_frame(self):
        """Чтение кадра из камеры и отображение (вызывается по таймеру)"""
        if not self.is_streaming or self.capture is None or not self.capture.isOpened():
            return

        ret, frame = self.capture.read()
        if ret:
            # Конвертируем BGR -> RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            # Создаём QImage и сохраняем копию для масштабирования на паузе
            qimage = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888).copy()
            self.last_qimage = qimage.copy()
            # Отображаем
            pixmap = QPixmap.fromImage(qimage)
            self.display_pixmap(pixmap)
        else:
            # Ошибка чтения (камера отключена)
            self.stop_stream()
            if self.capture:
                self.capture.release()
                self.capture = None
            QMessageBox.warning(self, "Ошибка", "Потерян поток с камеры")

    def closeEvent(self, event):
        """Освобождение ресурсов при закрытии окна"""
        self.stop_stream()
        if self.capture is not None:
            self.capture.release()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraApp()
    window.show()
    sys.exit(app.exec())