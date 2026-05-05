from PySide6.QtWidgets import QApplication, QMainWindow, QStyleFactory

from qtUi.uiQtMain import Ui_MainWindow
from qtUi.uiQtBlack import Ui_Form

import sys
import os
import cv2
import numpy
from ctypes import windll, c_int, byref

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox,
    QComboBox, QPushButton, QSlider, QLabel, QSizePolicy, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
)
from PySide6 import QtCore
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtMultimedia import QMediaDevices

def disable_window_rounding(hwnd):
    """Отключает скругление углов окна (только для Windows)."""
    try:
        DWMWA_WINDOW_CORNER_PREFERENCE = 33
        DWMWCP_DONOTROUND = 1
        windll.dwmapi.DwmSetWindowAttribute(
            hwnd,
            DWMWA_WINDOW_CORNER_PREFERENCE,
            byref(c_int(DWMWCP_DONOTROUND)),
            c_int(4)  # размер параметра
        )
    except Exception as e:
        print(f"Не удалось отключить скругление: {e}")

class BlackScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setup_ui()
        self.original_pixmap = None

    def showEvent(self, event):
        """Событие показа окна: получаем HWND и отключаем скругление."""
        super().showEvent(event)
        if sys.platform == "win32":
            hwnd = int(self.winId())  # получаем HWND окна
            disable_window_rounding(hwnd)

    def setup_ui(self):
        self.setWindowTitle("Projection Window")
        # self.setStyleSheet("background-color: black;")
        # self.setStyleSheet("border: 5px solid red;")
        # self.setStyle(QStyleFactory.create("Windows"))
        # self.setStyle(QStyleFactory.create('fusion'))
        # self.setStyleSheet("margin: 6px;")
        # self.setStyleSheet("margin: 6px; border: 5px solid red;")
        self.setGeometry(0, 0, 1920, 1080)
        # self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        # self.setWindowFlags(Qt.FramelessWindowHint)

        # self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)

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
        scaled_pixmap = self.original_pixmap.scaled(1920, 1080, Qt.IgnoreAspectRatio, Qt.FastTransformation)
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