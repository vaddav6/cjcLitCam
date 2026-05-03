import sys
import cv2
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QPushButton, QSlider, QLabel, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtMultimedia import QMediaDevices


class CameraApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("USB Camera with Overlay (Centered, 50% opacity)")
        self.setMinimumSize(800, 600)

        # Переменные состояния
        self.capture = None          # объект VideoCapture OpenCV
        self.timer = QTimer()        # таймер для обновления кадров
        self.is_streaming = False    # идёт ли трансляция
        self.current_pixmap = None   # текущий QPixmap кадра
        self.pixmap_item = None      # графический элемент для видео
        self.overlay_item = None     # графический элемент для оверлея
        self.overlay_pixmap = None   # исходный QPixmap оверлея

        # Создание интерфейса
        self.init_ui()

        # Загрузка оверлея (измените путь при необходимости)
        # self.load_overlay("resor/rgbSq.png")  # файл должен лежать в папке с программой

        # Заполнение списка камер
        self.populate_cameras()

        # Автоматический запуск первой камеры, если она есть
        # if self.combo.count() > 0:
        #     self.combo.setCurrentIndex(0)
        #     self.start_stream()
        self.is_streaming = False
        self.timer.stop()

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

        # QGraphicsView для отображения видео и оверлея
        self.graphics_view = QGraphicsView()
        self.graphics_view.setAlignment(Qt.AlignCenter)
        self.graphics_view.setBackgroundBrush(Qt.black)
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)

        # Элемент для видео
        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)

        main_layout.addWidget(self.graphics_view)

        # Подключение сигналов
        self.btn_start.clicked.connect(self.start_stream)
        self.btn_stop.clicked.connect(self.stop_stream)
        self.slider_zoom.valueChanged.connect(self.zoom_changed)
        self.combo.currentIndexChanged.connect(self.on_camera_changed)

    def load_overlay(self, filepath):
        """Загружает изображение оверлея (PNG, JPG), устанавливает прозрачность 50% и центрирует"""
        pixmap = QPixmap(filepath)
        if pixmap.isNull():
            print(f"Предупреждение: не удалось загрузить оверлей '{filepath}'. Работаем без оверлея.")
            self.overlay_item = None
            return
        self.overlay_pixmap = pixmap
        self.overlay_item = QGraphicsPixmapItem(pixmap)
        self.overlay_item.setOpacity(0.5)   # 50% прозрачности
        self.scene.addItem(self.overlay_item)
        # Z-порядок: оверлей поверх видео (чем выше число, тем выше)
        self.overlay_item.setZValue(1)
        self.pixmap_item.setZValue(0)
        print(f"Оверлей загружен: {filepath} (размер {pixmap.width()}x{pixmap.height()}, прозрачность 50%)")

    def update_overlay_position(self, video_width, video_height):
        """Центрирует оверлей относительно текущего размера видео"""
        if self.overlay_item is None or self.overlay_pixmap is None:
            return
        ow = self.overlay_pixmap.width()
        oh = self.overlay_pixmap.height()
        x = (video_width - ow) // 2
        y = (video_height - oh) // 2
        self.overlay_item.setPos(x, y)

    def populate_cameras(self):
        """Получение списка всех видеоустройств"""
        devices = QMediaDevices.videoInputs()
        for device in devices:
            self.combo.addItem(device.description())
        if self.combo.count() == 0:
            print("Не найдено ни одной USB-камеры")

    def on_camera_changed(self, index):
        """Переключение камеры"""
        if index < 0:
            return
        self.stop_stream()
        if self.capture is not None:
            self.capture.release()
            self.capture = None
        self.capture = cv2.VideoCapture(index)
        if not self.capture.isOpened():
            print(f"Не удалось открыть камеру: {self.combo.currentText()}")
            self.capture = None
        else:
            self.start_stream()

    def start_stream(self):
        """Запуск или возобновление трансляции"""
        if self.capture is None or not self.capture.isOpened():
            idx = self.combo.currentIndex()
            if idx < 0:
                return
            self.capture = cv2.VideoCapture(idx)
            if not self.capture.isOpened():
                return
        if not self.is_streaming:
            self.is_streaming = True
            self.timer.start(30)  # ~33 fps

    def stop_stream(self):
        """Остановка трансляции (кадры не читаются)"""
        self.is_streaming = False
        self.timer.stop()

    def zoom_changed(self, value):
        """Изменение масштаба через ползунок"""
        scale_factor = value / 100.0
        self.zoom_label.setText(f"{scale_factor:.1f}x")
        # Применяем масштаб к QGraphicsView (относительно текущего центра)
        self.graphics_view.resetTransform()
        self.graphics_view.scale(scale_factor, scale_factor)

    def update_frame(self):
        """Чтение кадра из камеры, наложение оверлея (уже на сцене) и отображение"""
        if not self.is_streaming or self.capture is None or not self.capture.isOpened():
            return

        ret, frame = self.capture.read()
        if ret:
            # Конвертируем BGR -> RGB (OpenCV использует BGR)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            qimage = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimage)
            self.current_pixmap = pixmap.copy()
            self.pixmap_item.setPixmap(pixmap)

            # Обновляем сцену под размер видео
            self.scene.setSceneRect(0, 0, w, h)

            # Центрируем оверлей (если он есть)
            if self.overlay_item is not None:
                self.update_overlay_position(w, h)
        else:
            self.stop_stream()
            if self.capture:
                self.capture.release()
                self.capture = None

    def closeEvent(self, event):
        """Освобождение ресурсов"""
        self.stop_stream()
        if self.capture is not None:
            self.capture.release()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraApp()
    window.show()
    sys.exit(app.exec())