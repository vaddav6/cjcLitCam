import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLineEdit, QLabel, QFileDialog, QMessageBox, QSizePolicy)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer


class FullScreenWindow(QWidget):
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
        scaled_pixmap = self.original_pixmap.scaled(
            widget_size,
            Qt.IgnoreAspectRatio,
            Qt.FastTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.original_pixmap and not self.original_pixmap.isNull():
            self.update_image()

    def clear(self):
        self.image_label.clear()
        self.image_label.setStyleSheet("background-color: black;")
        self.original_pixmap = None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_connections()
        self.fullscreen_window = FullScreenWindow()
        self.fullscreen_window.showFullScreen()
        self.image_path = ""
        self.projection_cycle_active = False
        self.remaining_cycles = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.cycle_step)

    def setup_ui(self):
        self.setWindowTitle("Литография")
        self.setGeometry(10, 300, 450, 550)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Control buttons
        buttons_layout = QHBoxLayout()
        self.start_button = QPushButton("Старт")
        self.stop_button = QPushButton("Стоп")
        self.stop_button.setEnabled(False)
        buttons_layout.addWidget(self.start_button)
        buttons_layout.addWidget(self.stop_button)
        main_layout.addLayout(buttons_layout)

        # Settings
        settings_layout = QVBoxLayout()

        # Display time
        display_layout = QHBoxLayout()
        display_layout.addWidget(QLabel("Время трансляции (мс):"))
        self.display_time_edit = QLineEdit("1000")
        display_layout.addWidget(self.display_time_edit)
        settings_layout.addLayout(display_layout)

        # Pause time
        pause_layout = QHBoxLayout()
        pause_layout.addWidget(QLabel("Время паузы (мс):"))
        self.pause_time_edit = QLineEdit("1000")
        pause_layout.addWidget(self.pause_time_edit)
        settings_layout.addLayout(pause_layout)

        # Cycles count
        cycles_layout = QHBoxLayout()
        cycles_layout.addWidget(QLabel("Количество циклов:"))
        self.cycles_edit = QLineEdit("1")
        cycles_layout.addWidget(self.cycles_edit)
        settings_layout.addLayout(cycles_layout)

        main_layout.addLayout(settings_layout)

        # Image selection
        image_layout = QVBoxLayout()
        self.select_button = QPushButton("Выбрать изображение")
        image_layout.addWidget(self.select_button)

        self.thumbnail_label = QLabel()
        self.thumbnail_label.setFixedSize(442, 250)
        self.thumbnail_label.setAlignment(Qt.AlignCenter)
        self.thumbnail_label.setStyleSheet("border: 1px solid gray;")
        image_layout.addWidget(self.thumbnail_label)

        self.filename_label = QLabel("Файл не выбран")
        self.filename_label.setAlignment(Qt.AlignCenter)
        image_layout.addWidget(self.filename_label)

        main_layout.addLayout(image_layout)

    def setup_connections(self):
        self.start_button.clicked.connect(self.start_projection)
        self.stop_button.clicked.connect(self.stop_projection)
        self.select_button.clicked.connect(self.select_image)

    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите изображение",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )

        if file_path:
            self.image_path = file_path
            self.filename_label.setText(os.path.basename(file_path))

            # Load and scale thumbnail
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                thumbnail = pixmap.scaled(
                    150, 225,
                    Qt.KeepAspectRatioByExpanding,
                    Qt.FastTransformation
                )
                self.thumbnail_label.setPixmap(thumbnail)
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось загрузить изображение")
                self.thumbnail_label.clear()
                self.filename_label.setText("Файл не выбран")
                self.image_path = ""

    def validate_inputs(self):
        try:
            display_time = int(self.display_time_edit.text())
            pause_time = int(self.pause_time_edit.text())
            cycles = int(self.cycles_edit.text())

            if display_time <= 0 or pause_time <= 0 or cycles <= 0:
                raise ValueError("Значения должны быть положительными")

            return display_time, pause_time, cycles

        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите корректные числовые значения")
            return None

    def start_projection(self):
        if not self.image_path:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите изображение")
            return

        inputs = self.validate_inputs()
        if not inputs:
            return

        self.display_time, self.pause_time, self.total_cycles = inputs
        self.remaining_cycles = self.total_cycles

        self.projection_cycle_active = True
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.select_button.setEnabled(False)

        # Start first cycle
        self.show_image()
        self.current_state = "display"
        self.timer.start(self.display_time)

    def stop_projection(self):
        self.projection_cycle_active = False
        self.timer.stop()
        self.fullscreen_window.clear()
        self.reset_controls()

    def cycle_step(self):
        self.timer.stop()

        if not self.projection_cycle_active:
            return

        if self.current_state == "display":
            # Switch to pause
            self.hide_image()
            self.current_state = "pause"
            self.timer.start(self.pause_time)

        elif self.current_state == "pause":
            # Finish current cycle
            self.remaining_cycles -= 1

            if self.remaining_cycles > 0:
                # Start next cycle
                self.show_image()
                self.current_state = "display"
                self.timer.start(self.display_time)
            else:
                # All cycles completed
                self.fullscreen_window.clear()
                self.reset_controls()

    def show_image(self):
        pixmap = QPixmap(self.image_path).toImage().mirrored(True, False)
        pixmap = QPixmap.fromImage(pixmap)
        #pixmap = QPixmap(self.image_path)

        if not pixmap.isNull():
            self.fullscreen_window.show_image(pixmap)

    def hide_image(self):
        self.fullscreen_window.clear()

    def reset_controls(self):
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.select_button.setEnabled(True)
        self.projection_cycle_active = False

    def closeEvent(self, event):
        self.fullscreen_window.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())