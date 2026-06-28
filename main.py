# from PySide6.QtWidgets import QApplication, QMainWindow, QStyleFactory

import os
import sys

import cv2
# from PySide6 import QtCore
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtMultimedia import QMediaDevices
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QMessageBox,
    QGraphicsScene, QGraphicsPixmapItem
)

# from qtUi.uiQtBlack import Ui_Form
from prjBlackScreen import BlackScreen
from qtUi.uiQtMain import Ui_MainWindow


# import numpy


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
        self.mirrorH = False
        self.mirrorV = False
        self.video_width = 3840
        self.video_height = 2160
        # self.video_width = 1080
        # self.video_height = 1920
        self.timer = QTimer()  # таймер для обновления кадров
        self.timer.timeout.connect(self.cam_update_frame)

        self.scene = QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)
        self.ui.graphicsView.setBackgroundBrush(Qt.black)  # чёрный фон

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


        self.align_mask = None
        self.alignMaskOriginPixmap = None
        self.alignMaskFormingPixmap = QGraphicsPixmapItem()
        self.alignMaskFormingPixmap.setZValue(1)

        self.pBTimer = QTimer()
        self.pBTimer.timeout.connect(self.pb_change)
        self.pBVal = 0
        self.pBTime = None
        self.pBMinTik = 1

        self.current_pixmap = None

        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)
        self.cam_list_update()

        self.pixmap_item.setZValue(0)

        self.init_ui()
        # self.uiBlack.setupUi(self)
        # self.show_image()

    def init_ui(self):
        """Инициализация виджетов и компоновка"""
        self.ui.cB_cameraName.currentIndexChanged.connect(self.cam_select)
        self.ui.pB_stopCamera.clicked.connect(self.cam_stop_stream)
        self.ui.pB_startCamera.clicked.connect(self.cam_start_stream)
        self.ui.dSB_scaleCamera.valueChanged.connect(self.main_zoom_changed)
        self.ui.chB_hMrirrorCamera.clicked.connect(self.cam_mirror_h)
        self.ui.chB_vMrirrorCamera.clicked.connect(self.cam_mirror_v)
        self.ui.pB_saveCamera.clicked.connect(self.cam_save_image)

        self.ui.pB_maskSelect.clicked.connect(self.align_mask_select)

        self.ui.dSB_align_scale.valueChanged.connect(self.align_mask_forming)
        self.ui.dSB_align_opacity.valueChanged.connect(self.align_mask_forming)
        self.ui.sB_align_coord_H.valueChanged.connect(self.align_mask_forming)
        self.ui.sB_align_coord_W.valueChanged.connect(self.align_mask_forming)
        self.ui.chB_align_show.stateChanged.connect(self.align_mask_forming)
        self.ui.chB_align_noFrame.stateChanged.connect(self.align_mask_remove_frame)
        self.ui.chB_align_mirrorH.stateChanged.connect(self.align_mirror_h)
        self.ui.chB_align_mirrorV.stateChanged.connect(self.align_mirror_v)

        self.ui.pushButton_2.clicked.connect(self.start_projection)

    def cam_list_update(self):
        """Получение списка всех видеоустройств"""
        devices = QMediaDevices.videoInputs()
        for device in devices:
            self.ui.cB_cameraName.addItem(device.description())
        if self.ui.cB_cameraName.count() == 0:
            print("Не найдено ни одной USB-камеры")

        if self.ui.cB_cameraName.count() > 0:
            self.ui.cB_cameraName.setCurrentIndex(0)
            self.cam_select(self.ui.cB_cameraName.currentIndex())
            print(self.ui.cB_cameraName.currentIndex())

    def cam_select(self, idx):
        if idx < 0:
            return

        self.index = idx
        self.capture = cv2.VideoCapture(self.index)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)

        self.main_zoom_changed(self.ui.dSB_scaleCamera.value())

    def cam_start_stream(self):
        """Запуск трансляции (кадры читаются)"""
        self.is_streaming = True
        self.timer.start(30)

    def cam_mirror_h(self, st):
        """Изменение параметра зеркалирования изображения камеры по горизонтали"""
        self.mirrorH = st

    def cam_mirror_v(self, st):
        """Изменение параметра зеркалирования изображения камеры по вертикали"""
        self.mirrorV = st

    def main_zoom_changed(self, scale):
        """Изменение масштаба через ползунок"""
        scale_factor = scale / 100.0
            # self.zoom_label.setText(f"{scale_factor:.1f}x")
        # Применяем масштаб к QGraphicsView (относительно текущего центра)
        self.ui.graphicsView.resetTransform()
        self.ui.graphicsView.scale(scale_factor, scale_factor)

    def cam_save_image(self):
        # 1. Захватываем кадр с камеры
        cap = self.capture
        ret, frame = cap.read()
        cap.release()

        if not ret:
            QMessageBox.warning(self, "Ошибка", "Не удалось захватить кадр с камеры")
            return

        # 2. Открываем диалог сохранения файла
        # Параметры: родитель, заголовок, начальная папка, фильтр типов файлов[reference:3]
        file_path, selected_filter = QFileDialog.getSaveFileName(
            self,
            "Сохранить изображение",
            "my_photo.png",  # имя файла по умолчанию
            "Изображения (*.jpg *.jpeg *.png *.bmp);;Все файлы (*.*)"
        )

        # 3. Если пользователь выбрал файл (не нажал "Отмена")
        if file_path:
            # Сохраняем изображение через OpenCV
            success = cv2.imwrite(file_path, frame)
            if not success:
                QMessageBox.warning(self, "Ошибка", "Не удалось сохранить файл")
                # QMessageBox.information(self, "Успех", f"Изображение сохранено:\n{file_path}")
            # else:
            #     QMessageBox.warning(self, "Ошибка", "Не удалось сохранить файл")
        else:
            QMessageBox.information(self, "Отмена", "Сохранение отменено")

    def cam_update_frame(self):
        """Чтение кадра из камеры и отображение"""
        if self.capture is not None:
            ret, frame = self.capture.read()
            if ret:
                # Конвертируем BGR -> RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame_rgb.shape
                bytes_per_line = ch * w
                qimage = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)

                if self.mirrorV:
                    qimage.flip(Qt.Vertical)
                if self.mirrorH:
                    qimage.flip(Qt.Horizontal)

                # pixmap = QPixmap.fromImage(qimage) # камера
                pixmap = QPixmap("resor/photoMicroStruct_4k.jpg") # DEB img вместо камеры
                self.current_pixmap = pixmap.copy()
                # Обновляем сцену
                self.pixmap_item.setPixmap(pixmap)
                self.scene.setSceneRect(0, 0, 0, 0)

    def cam_stop_stream(self):
        """Остановка трансляции (кадры не читаются)"""
        self.is_streaming = False
        self.timer.stop()

    def align_mask_select(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите изображение",
            "C:/Users/Daniil/YandexDisk-vad.varganov/Компьютер DESKTOP-09T6CET/univer/аспер/приборы проекты/литографПроектор-------------/шаблоны/калибровка 854",
            # C:\Users\Daniil\YandexDisk-vad.varganov\Компьютер DESKTOP-09T6CET\univer\аспер\приборы проекты\литографПроектор-------------\шаблоны\калибровка 854
            "Images (*.png)"
        )

        if file_path:
            self.mask_filePath = file_path
            self.ui.l_align_maskName.setText(os.path.basename(file_path))

            # Load and scale thumbnail
            self.align_mask = QPixmap(file_path)
            if not self.align_mask.isNull():
                self.maskMini = self.align_mask.scaled(
                    250, 100,
                    Qt.KeepAspectRatioByExpanding,  # IgnoreAspectRatio
                    Qt.FastTransformation
                )
                self.ui.l_align_maskMini.setPixmap(self.maskMini)

                self.align_load_mask(self.align_mask)

                self.ui.frame_3.setEnabled(True)
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось загрузить изображение")
                self.ui.l_align_maskMini.clear()
                self.ui.l_align_maskName.setText("Файл не выбран")
                self.mask_filePath = ""

    def align_load_mask(self, qpixmap): # DELL
        """Загружает изображение маски"""
        self.ui.graphicsView.setBackgroundBrush(Qt.black)  # чёрный фон

        if qpixmap.isNull():
            print(f"Предупреждение: не удалось загрузить оверлей. Работаем без оверлея.")
            self.alignMaskOriginPixmap = None
            self.alignMaskFormingPixmap = None
            return

        self.alignMaskOriginPixmap = qpixmap

        self.align_mask_forming()

        self.scene.addItem(self.alignMaskFormingPixmap)

    def align_mask_forming(self):
        """преобразует отображение маски для выравнивания"""
        self.align_mask_scale()

        if self.ui.chB_align_show.isChecked():
            self.alignMaskFormingPixmap.setOpacity(self.ui.dSB_align_opacity.value() / 100)
        else:
            self.alignMaskFormingPixmap.setOpacity(0)

        self.align_update_mask_position()

    def align_mask_remove_frame(self):
        """делает чёрный фон маски полностью прозрачным для выравнивания"""
        if self.ui.chB_align_noFrame.isChecked():
            pixmap = self.align_mask
            # Convert to QImage
            image = pixmap.toImage()
            # If not already with alpha, convert to format with alpha
            if image.format() != QImage.Format_ARGB32_Premultiplied and image.format() != QImage.Format_ARGB32:
                image = image.convertToFormat(QImage.Format_ARGB32)
            # Iterate pixels
            for y in range(image.height()):
                for x in range(image.width()):
                    color = image.pixelColor(x, y)
                    if color.red() == 0 and color.green() == 0 and color.blue() == 0:
                        color.setAlpha(0)
                        image.setPixelColor(x, y, color)
            # return QPixmap.fromImage(image)
            self.alignMaskOriginPixmap = QPixmap.fromImage(image)
        else:
            self.alignMaskOriginPixmap = self.align_mask

        self.align_mask_forming()

    def align_mask_scale(self):
        scale = float(self.ui.dSB_align_scale.value()) / 100

        w = int(float(self.alignMaskOriginPixmap.width()) * scale)
        h = int(float(self.alignMaskOriginPixmap.height()) * scale)

        pixmap = self.alignMaskOriginPixmap.scaled(
            w, h,
            Qt.KeepAspectRatioByExpanding,  # IgnoreAspectRatio
            Qt.FastTransformation
        )

        self.alignMaskFormingPixmap.setPixmap(pixmap)

    def align_update_mask_position(self):
        """Центрирует маску относительно текущего кадра с камеры с учётом масштабирования себя"""
        if self.alignMaskFormingPixmap is None:
            return

        q_rect = self.alignMaskFormingPixmap.boundingRect()

        w = self.ui.sB_align_coord_W.value() - (q_rect.width() // 2)
        h = self.ui.sB_align_coord_H.value() - (q_rect.height() // 2)

        self.alignMaskFormingPixmap.setPos(int(w), int(h))

    def align_mirror_h(self):
        al_image = self.alignMaskOriginPixmap.toImage()

        if self.ui.chB_align_mirrorH.isChecked():
            al_image. flip(Qt.Horizontal)
        else:
            al_image.flip(Qt.Horizontal)

        self.alignMaskOriginPixmap = QPixmap.fromImage(al_image)

        self.align_mask_forming()

    def align_mirror_v(self):
        al_image = self.alignMaskOriginPixmap.toImage()

        if self.ui.chB_align_mirrorV.isChecked():
            al_image. flip(Qt.Vertical)
        else:
            al_image.flip(Qt.Vertical)

        self.alignMaskOriginPixmap = QPixmap.fromImage(al_image)

        self.align_mask_forming()


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

    def reset_controls(self):
        self.ui.pushButton_2.setEnabled(True)
        self.ui.pushButton_3.setEnabled(False)
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

    def closeEvent(self, event):
        self.fullscreen_window.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = App()
    window.show()

    sys.exit(app.exec())