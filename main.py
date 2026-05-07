# from PySide6.QtWidgets import QApplication, QMainWindow, QStyleFactory

from qtUi.uiQtMain import Ui_MainWindow
# from qtUi.uiQtBlack import Ui_Form
from prjBlackScreen import BlackScreen

import sys
import os
import cv2
# import numpy

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox,
    QComboBox, QPushButton, QSlider, QLabel, QSizePolicy, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
)
# from PySide6 import QtCore
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtMultimedia import QMediaDevices


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        # self.setWindowFlags(Qt.FramelessWindowHint)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.fullscreen_window = BlackScreen()
        self.fullscreen_window.setStyleSheet("background-color: black;")
        # self.fullscreen_window.showFullScreen()
        self.fullscreen_window.show()

        self.capture = None
        self.is_streaming = False
        self.index = None

        self.display_time = 0
        self.pause_time = 0
        self.total_cycles = 0
        self.remaining_cycles = 0
        self.projection_cycle_active = False
        self.timerLitho = QTimer()
        self.timerLitho.timeout.connect(self.cycle_step)
        self.current_state = None

        self.mask_filePath = None
        self.maskFileName = None
        self.mask = None
        self.maskMini = None
        self.maskAlign = QGraphicsPixmapItem()
        self.maskAlignOrigin = None

        self.maskAlignShift_v = None
        self.maskAlignShift_h = None
        self.maskAlignShow = None
        self.maskAlignScale = None
        self.maskAlignOpacity = 50

        self.video_width = 3840
        self.video_height = 2160
        # self.video_width = 1080
        # self.video_height = 1920

        self.pBTimer = QTimer()
        self.pBTimer.timeout.connect(self.pb_change)
        self.pBVal = 0
        self.pBTime = None
        self.pBMinTik = 1

        self.current_pixmap = None

        self.scene = QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)
        self.ui.graphicsView.setBackgroundBrush(Qt.black)  # чёрный фон

        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)
        # self.scene.addItem(self.maskAlign)
        # self.update_frame()
        self.cam_list_update()
        self.maskAlign.setZValue(1)
        self.pixmap_item.setZValue(0)

        self.timer = QTimer()  # таймер для обновления кадров
        self.timer.timeout.connect(self.update_frame)

        self.init_ui()
        # self.uiBlack.setupUi(self)
        # self.show_image()

    def init_ui(self):
        """Инициализация виджетов и компоновка"""
        self.ui.comboBox.currentIndexChanged.connect(self.cam_select)
        self.ui.pB_stopCamera.clicked.connect(self.cam_stop_stream)
        self.ui.pB_startCamera.clicked.connect(self.cam_start_stream)
        self.ui.horizontalSlider.valueChanged.connect(self.main_zoom_changed)
        self.ui.pushButton.clicked.connect(self.mask_select)

        self.ui.pushButton_2.clicked.connect(self.start_projection)
        self.ui.horizontalSlider_3.valueChanged.connect(self.change_mask_opacity)
        self.ui.horizontalSlider_2.valueChanged.connect(self.change_mask_scale)
        self.ui.checkBox.checkStateChanged.connect(self.change_mask_show)

    def change_mask_show(self, state):
        if self.ui.checkBox.isChecked():
            self.maskAlign.setOpacity(self.ui.horizontalSlider_3.value() / 100)
        else:
            self.maskAlign.setOpacity(0)

    def change_mask_opacity(self, opacity):
        self.maskAlign.setOpacity(opacity/100)

    def change_mask_scale(self, scale):
        scale = float(scale)/100

        print(self.maskAlignOrigin.width())
        print(self.maskAlignOrigin.height())

        w = int(float(self.maskAlignOrigin.width())*scale)
        h = int(float(self.maskAlignOrigin.height())*scale)

        pixmap = self.maskAlignOrigin.scaled(
            w, h,
            Qt.KeepAspectRatioByExpanding,  # IgnoreAspectRatio
            Qt.FastTransformation
        )

        self.maskAlign.setPixmap(pixmap)

        # scale_factor = scale / 100.0
        # self.maskAlign.scale(scale_factor)

        # self.mask = QPixmap(file_path)
        # if not self.mask.isNull():
        #     self.maskMini = self.mask.scaled(
        #         250, 100,
        #         Qt.KeepAspectRatioByExpanding,  # IgnoreAspectRatio
        #         Qt.FastTransformation
        #     )
        #     self.ui.label_2.setPixmap(self.maskMini)


    def validate_inputs(self):
        try:
            display_time = int(self.ui.spinBox_2.text())
            pause_time = int(self.ui.spinBox_3.text())
            cycles = int(self.ui.spinBox_4.text())

            # if display_time <= 0 or pause_time <= 0 or cycles <= 0:
            if display_time <= 0 or cycles <= 0:
                raise ValueError("Значения должны быть положительными")

            self.pBTime = int((cycles * (display_time + pause_time))/(100/self.pBMinTik))
            self.pBTimer.start(self.pBTime)

            return display_time, pause_time, cycles

        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите корректные числовые значения")
            return None

    def stop_controls(self):
        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton_3.setEnabled(True)
        self.ui.pushButton.setEnabled(False)

    def reset_controls(self):
        self.ui.pushButton_2.setEnabled(True)
        self.ui.pushButton_3.setEnabled(False)
        self.ui.pushButton.setEnabled(True)
        self.projection_cycle_active = False

        self.pBVal = 0
        self.ui.progressBar.setValue(self.pBVal)
        self.pBTimer.stop()

    def pb_change(self):
        self.pBVal += self.pBMinTik
        self.ui.progressBar.setValue(self.pBVal)

    def start_projection(self):
        if not self.mask_filePath:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите изображение")
            return

        inputs = self.validate_inputs()
        if not inputs:
            return

        self.display_time, self.pause_time, self.total_cycles = inputs
        self.remaining_cycles = self.total_cycles

        self.projection_cycle_active = True
        self.stop_controls()

        # Start first cycle
        self.show_image()
        self.current_state = "display"
        self.timerLitho.start(self.display_time)

    def cycle_step(self):
        self.timerLitho.stop()

        if not self.projection_cycle_active:
            return

        if self.current_state == "display":
            # Switch to pause
            self.hide_image()
            self.current_state = "pause"
            self.timerLitho.start(self.pause_time)

        elif self.current_state == "pause":
            # Finish current cycle
            self.remaining_cycles -= 1

            if self.remaining_cycles > 0:
                # Start next cycle
                self.show_image()
                self.current_state = "display"
                self.timerLitho.start(self.display_time)

                total_time = self.total_cycles * (self.display_time + self.pause_time)
                remaining_time = self.remaining_cycles * (self.display_time + self.pause_time)
                self.pBVal = 100 - int((remaining_time / total_time) * 100)
                self.ui.progressBar.setValue(self.pBVal)
            else:
                # All cycles completed
                self.fullscreen_window.clear()
                self.reset_controls()

    def show_image(self):
        # pixmap = QPixmap("resor/rgbSq.png").toImage().mirrored(True, False)
        # pixmap = QPixmap("resor/rgbSq.png").toImage()
        # pixmap = QPixmap.fromImage(pixmap)
        # pixmap = QPixmap(self.image_path)
        pixmap = self.mask

        if not pixmap.isNull():
            self.fullscreen_window.show_image(pixmap)

    def hide_image(self):
        self.fullscreen_window.clear()

    def cam_select(self, idx):
        if idx < 0:
            return
        self.index = idx
        self.capture = cv2.VideoCapture(self.index)
        print(idx)

    # def load_overlay(self, filepath):
    def load_overlay(self, qpixmap):
        """Загружает изображение оверлея (PNG, JPG), устанавливает прозрачность 50% и центрирует"""
        # self.scene.clear()
        # self.scene.addItem(self.pixmap_item)
        self.ui.graphicsView.setBackgroundBrush(Qt.black)  # чёрный фон
        pixmap = qpixmap
        if pixmap.isNull():
            print(f"Предупреждение: не удалось загрузить оверлей. Работаем без оверлея.")
            self.maskAlign = None
            return

        self.maskAlignOrigin = pixmap
        # self.maskAlign = QGraphicsPixmapItem(pixmap)
        # self.maskAlign.setPixmap(pixmap)
        self.change_mask_scale(100)
        self.ui.horizontalSlider_2.setValue(100)
        self.maskAlign.setOpacity(0.5)   # 50% прозрачности
        self.ui.horizontalSlider_3.setValue(50)


        self.scene.addItem(self.maskAlign)
        # Z-порядок: оверлей поверх видео (чем выше число, тем выше)
        # self.maskAlign.setZValue(1)
        # self.pixmap_item.setZValue(0)

        # начальная запись координат в комбобокс
        self.start_mask_position()

    def update_overlay_position(self, video_width, video_height):
        """Центрирует оверлей относительно текущего размера видео"""
        if self.maskAlign is None:
            return
        # ow = self.maskAlignOrigin.width()
        # oh = self.maskAlignOrigin.height()
        # x = (video_width - ow) // 2
        # y = (video_height - oh) // 2

        # self.ui.horizontalSlider_2.valueChanged.connect(self.change_mask_scale)
        scale_factor = self.ui.horizontalSlider_2.value() / 100.0

        # x = self.ui.spinBox_5.value() * scale_factor
        # y = self.ui.spinBox.value() * scale_factor

        ow = self.maskAlignOrigin.width() * scale_factor
        oh = self.maskAlignOrigin.height() * scale_factor
        x = (self.ui.spinBox_5.value() - ow) // 2
        y = (self.ui.spinBox.value() - oh) // 2
        self.maskAlign.setPos(int(x), int(y))
        return x, y

    def mask_select(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите изображение",
            "C:/Users/Daniil/YandexDisk-vad.varganov/Компьютер DESKTOP-09T6CET/univer/аспер/приборы проекты/литографПроектор-------------/шаблоны/калибровка 854", # C:\Users\Daniil\YandexDisk-vad.varganov\Компьютер DESKTOP-09T6CET\univer\аспер\приборы проекты\литографПроектор-------------\шаблоны\калибровка 854
            "Images (*.png)"
        )

        if file_path:
            self.mask_filePath = file_path
            self.ui.label_3.setText(os.path.basename(file_path))

            # Load and scale thumbnail
            self.mask = QPixmap(file_path)
            if not self.mask.isNull():
                self.maskMini = self.mask.scaled(
                    250, 100,
                    Qt.KeepAspectRatioByExpanding, # IgnoreAspectRatio
                    Qt.FastTransformation
                )
                self.ui.label_2.setPixmap(self.maskMini)

                self.load_overlay(self.mask)

                self.ui.frame_5.setEnabled(True)
                self.ui.frame_3.setEnabled(True)
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось загрузить изображение")
                self.ui.label_2.clear()
                self.ui.label_3.setText("Файл не выбран")
                self.mask_filePath = ""

    def start_mask_position(self):
        if self.maskAlign is None:
            return
        ow = self.maskAlignOrigin.width()
        oh = self.maskAlignOrigin.height()
        # x = (self.video_width - ow) // 2
        # y = (self.video_height - oh) // 2

        x = (self.video_width) // 2
        y = (self.video_height) // 2

        self.ui.spinBox.setValue(y)
        self.ui.spinBox_5.setValue(x)

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
                qimage = qimage.mirrored(True, False)
                # Создаём QPixmap из QImage
                pixmap = QPixmap.fromImage(qimage)
                # pixmap = QPixmap(self.image_path).toImage().mirrored(True, False)
                # pixmap.mirrored(True, False)
                self.current_pixmap = pixmap.copy()
                # Обновляем сцену
                self.pixmap_item.setPixmap(pixmap)
                # Подгоняем размер сцены под pixmap, чтобы виды корректно работали
                # self.scene.setSceneRect(0, 0, pixmap.width(), pixmap.height())
                self.scene.setSceneRect(0, 0, self.video_width/2, self.video_height/2)

                # Центрируем оверлей (если он есть)
                if self.mask is not None:
                    self.update_overlay_position(self.video_width, self.video_height)

            # self.ui.graphicsView.setScene(self.scene)



if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = App()
    window.show()

    sys.exit(app.exec())