import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from qtUi.uiQtMain import Ui_MainWindow
from qtUi.uiQtBlack import Ui_Form

import sys
import cv2
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QPushButton, QSlider, QLabel, QSizePolicy, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtMultimedia import QMediaDevices

class BlackScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.original_pixmap = None

    def setup_ui(self):
        self.setWindowTitle("Projection Window")
        self.setStyleSheet("background-color: black;")
        self.setGeometry(0, 0, 1920, 1080)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("background-color: black;")
        self.image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.image_label)
        self.setLayout(layout)

    def show_image(self, pixmap):
        if pixmap.isNull():
            return

        self.original_pixmap = pixmap
        self.update_image()

    def update_image(self):
        if not self.original_pixmap or self.original_pixmap.isNull():
            return

        # Используем физический размер виджета вместо QLabel
        widget_size = self.size()
        # scaled_pixmap = self.original_pixmap.scaled(
        #     widget_size,
        #     Qt.IgnoreAspectRatio,
        #     Qt.FastTransformation
        # )
        scaled_pixmap = self.original_pixmap.scaled(1920, 1080)
        # print(widget_size)
        self.image_label.setPixmap(scaled_pixmap)
        # self.image_label.setPixmap(self.original_pixmap)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.original_pixmap and not self.original_pixmap.isNull():
            self.update_image()

    def clear(self):
        self.image_label.clear()
        self.image_label.setStyleSheet("background-color: black;")
        self.original_pixmap = None

class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.fullscreen_window = BlackScreen()
        self.fullscreen_window.showFullScreen()

        self.capture = None
        self.is_streaming = False
        self.index = None

        self.scene = QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)
        self.ui.graphicsView.setBackgroundBrush(Qt.black)  # чёрный фон

        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)
        # self.update_frame()
        self.cam_list_update()

        self.timer = QTimer()  # таймер для обновления кадров
        self.timer.timeout.connect(self.update_frame)

        self.init_ui()
        # self.uiBlack.setupUi(self)
        self.show_image()

    def init_ui(self):
        """Инициализация виджетов и компоновка"""
        self.ui.comboBox.currentIndexChanged.connect(self.cam_select)
        self.ui.pB_stopCamera.clicked.connect(self.cam_stop_stream)
        self.ui.pB_startCamera.clicked.connect(self.cam_start_stream)
        self.ui.horizontalSlider.valueChanged.connect(self.main_zoom_changed)

    def show_image(self):
        # pixmap = QPixmap("resor/rgbSq.png").toImage().mirrored(True, False)
        pixmap = QPixmap("resor/rgbSq.png").toImage()
        pixmap = QPixmap.fromImage(pixmap)
        #pixmap = QPixmap(self.image_path)

        if not pixmap.isNull():
            self.fullscreen_window.show_image(pixmap)

    def cam_select(self, idx):
        if idx < 0:
            return
        self.index = idx
        self.capture = cv2.VideoCapture(self.index)
        print(idx)

    def main_zoom_changed(self, scale):
        """Изменение масштаба через ползунок"""
        scale_factor = scale / 100.0
            # self.zoom_label.setText(f"{scale_factor:.1f}x")
        # Применяем масштаб к QGraphicsView (относительно текущего центра)
        self.ui.graphicsView.resetTransform()
        self.ui.graphicsView.scale(scale_factor, scale_factor)

    def cam_list_update(self):
        """Получение списка всех видеоустройств"""
        devices = QMediaDevices.videoInputs()
        for device in devices:
            self.ui.comboBox.addItem(device.description())
        if self.ui.comboBox.count() == 0:
            print("Не найдено ни одной USB-камеры")

        if self.ui.comboBox.count() > 0:
            self.ui.comboBox.setCurrentIndex(0)
            self.cam_select(self.ui.comboBox.currentIndex())
            print(self.ui.comboBox.currentIndex())

    def cam_start_stream(self):
        """Остановка трансляции (кадры не читаются)"""
        self.is_streaming = True
        self.timer.start(30)

    def cam_stop_stream(self):
        """Остановка трансляции (кадры не читаются)"""
        self.is_streaming = False
        self.timer.stop()

    def closeEvent(self, event):
        self.fullscreen_window.close()
        event.accept()

    def update_frame(self):
        """Чтение кадра из камеры, наложение оверлея (уже на сцене) и отображение"""
        # self.capture = cv2.VideoCapture(self.index)
        if self.capture is not None:
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

            self.ui.graphicsView.setScene(self.scene)



if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = App()
    window.show()

    sys.exit(app.exec())