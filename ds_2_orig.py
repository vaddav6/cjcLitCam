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
        self.setWindowTitle("USB Camera Viewer (QGraphicsView)")
        self.setMinimumSize(800, 600)

        # Переменные состояния
        self.capture = None          # объект VideoCapture OpenCV
        self.timer = QTimer()        # таймер для обновления кадров
        self.is_streaming = False    # идёт ли трансляция
        self.current_pixmap = None   # текущий QPixmap кадра (для масштабирования на паузе)
        self.pixmap_item = None      # графический элемент на сцене

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

        # QGraphicsView для отображения видео
        self.graphics_view = QGraphicsView()
        self.graphics_view.setAlignment(Qt.AlignCenter)  # центрирование содержимого
        self.graphics_view.setBackgroundBrush(Qt.black)  # чёрный фон
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)

        # Добавляем пустой элемент-картинку (пока без pixmap)
        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)

        main_layout.addWidget(self.graphics_view)

        # Подключение сигналов
        self.btn_start.clicked.connect(self.start_stream)
        self.btn_stop.clicked.connect(self.stop_stream)
        self.slider_zoom.valueChanged.connect(self.zoom_changed)
        self.combo.currentIndexChanged.connect(self.on_camera_changed)

    def populate_cameras(self):
        """Получение списка всех видеоустройств"""
        devices = QMediaDevices.videoInputs()
        for device in devices:
            self.combo.addItem(device.description())
        if self.combo.count() == 0:
            QLabel("Не найдено ни одной USB-камеры").show()  # упрощённо, можно через QMessageBox

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
            self.timer.start(30)  # 33 fps

    def stop_stream(self):
        """Остановка трансляции (кадры не читаются)"""
        self.is_streaming = False
        self.timer.stop()

    def zoom_changed(self, value):
        """Изменение масштаба через ползунок"""
        scale_factor = value / 100.0
        self.zoom_label.setText(f"{scale_factor:.1f}x")
        # Применяем масштаб к QGraphicsView (относительно центра)
        self.graphics_view.resetTransform()  # сбрасываем старый масштаб
        self.graphics_view.scale(scale_factor, scale_factor)
        # Дополнительно центрируем видимую область (чтобы текущий центр оставался)
        # При масштабировании через scale центр остаётся на месте

        # Если видео на паузе, перерисовываем картинку с новым масштабом? Не нужно, т.к. масштабирует сам view
        # Но можно обновить сцену
        self.scene.update()

    def update_frame(self):
        """Чтение кадра из камеры и отображение"""
        if not self.is_streaming or self.capture is None or not self.capture.isOpened():
            return

        ret, frame = self.capture.read()
        if ret:
            # Конвертируем BGR -> RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            qimage = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            # Создаём QPixmap из QImage
            pixmap = QPixmap.fromImage(qimage)
            self.current_pixmap = pixmap.copy()
            # Обновляем сцену
            self.pixmap_item.setPixmap(pixmap)
            # Подгоняем размер сцены под pixmap, чтобы виды корректно работали
            self.scene.setSceneRect(0, 0, pixmap.width(), pixmap.height())
            # При масштабировании через ползунок transform уже применён, но если масштаб иной, то вид сам отмасштабирует
            # Чтобы изображение всегда было видно целиком при первом показе, можно сделать:
            # self.graphics_view.fitInView(self.pixmap_item, Qt.KeepAspectRatio)
            # Но это конфликтует с ручным масштабированием. Лучше не трогать fitInView.
            # Дополнительно: если пользователь ещё не менял масштаб, можно один раз подогнать под размер.
            # Сделаем проверку - если текущий масштаб = 1.0 (ползунок 100), то вызовем zoom_changed(100) для синхронизации
        else:
            self.stop_stream()
            if self.capture:
                self.capture.release()
                self.capture = None

    def resizeEvent(self, event):
        """При изменении размера окна корректируем позицию, чтобы изображение было по центру"""
        super().resizeEvent(event)
        self.center_view()

    def center_view(self):
        """Центрирование содержимого в QGraphicsView (при необходимости)"""
        if self.pixmap_item and self.pixmap_item.pixmap():
            self.graphics_view.centerOn(self.pixmap_item)
        # Однако при масштабировании центрирование будет сохраняться автоматически, если установлен alignment

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