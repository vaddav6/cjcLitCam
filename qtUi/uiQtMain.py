# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui1.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QFrame,
    QGraphicsView, QHBoxLayout, QLabel, QMainWindow,
    QProgressBar, QPushButton, QSizePolicy, QSlider,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(640, 618)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setMaximumSize(QSize(16777215, 300))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.formLayout = QFormLayout(self.frame)
        self.formLayout.setObjectName(u"formLayout")
        self.comboBox = QComboBox(self.frame)
        self.comboBox.setObjectName(u"comboBox")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.comboBox)

        self.pB_startCamera = QPushButton(self.frame)
        self.pB_startCamera.setObjectName(u"pB_startCamera")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.pB_startCamera)

        self.pB_stopCamera = QPushButton(self.frame)
        self.pB_stopCamera.setObjectName(u"pB_stopCamera")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.pB_stopCamera)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)


        self.verticalLayout_2.addWidget(self.frame)

        self.horizontalSlider = QSlider(self.centralwidget)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setMinimum(10)
        self.horizontalSlider.setMaximum(400)
        self.horizontalSlider.setSingleStep(5)
        self.horizontalSlider.setPageStep(5)
        self.horizontalSlider.setSliderPosition(100)
        self.horizontalSlider.setOrientation(Qt.Orientation.Horizontal)
        self.horizontalSlider.setTickPosition(QSlider.TickPosition.TicksBothSides)
        self.horizontalSlider.setTickInterval(10)

        self.verticalLayout_2.addWidget(self.horizontalSlider)

        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMaximumSize(QSize(275, 16777215))
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_5 = QFrame(self.frame_4)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.formLayout_2 = QFormLayout(self.frame_5)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_4 = QLabel(self.frame_5)
        self.label_4.setObjectName(u"label_4")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_4)

        self.label_5 = QLabel(self.frame_5)
        self.label_5.setObjectName(u"label_5")

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_5)

        self.label_6 = QLabel(self.frame_5)
        self.label_6.setObjectName(u"label_6")

        self.formLayout_2.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_6)

        self.spinBox_2 = QSpinBox(self.frame_5)
        self.spinBox_2.setObjectName(u"spinBox_2")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.spinBox_2)

        self.spinBox_3 = QSpinBox(self.frame_5)
        self.spinBox_3.setObjectName(u"spinBox_3")

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.FieldRole, self.spinBox_3)

        self.spinBox_4 = QSpinBox(self.frame_5)
        self.spinBox_4.setObjectName(u"spinBox_4")

        self.formLayout_2.setWidget(3, QFormLayout.ItemRole.FieldRole, self.spinBox_4)

        self.pushButton_2 = QPushButton(self.frame_5)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.pushButton_2)

        self.pushButton_3 = QPushButton(self.frame_5)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.pushButton_3)


        self.verticalLayout.addWidget(self.frame_5)

        self.pushButton = QPushButton(self.frame_4)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)

        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.label_3 = QLabel(self.frame_4)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.progressBar = QProgressBar(self.frame_4)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.verticalLayout.addWidget(self.progressBar)


        self.horizontalLayout.addWidget(self.frame_4)

        self.graphicsView = QGraphicsView(self.frame_2)
        self.graphicsView.setObjectName(u"graphicsView")

        self.horizontalLayout.addWidget(self.graphicsView)


        self.verticalLayout_2.addWidget(self.frame_2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pB_startCamera.setText(QCoreApplication.translate("MainWindow", u"\u25b6 \u0421\u0442\u0430\u0440\u0442", None))
        self.pB_stopCamera.setText(QCoreApplication.translate("MainWindow", u"\u23f8 \u0421\u0442\u043e\u043f", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u041a\u0430\u043c\u0435\u0440\u0430:", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0440\u0435\u043c\u044f \u0442\u0440\u0430\u043d\u0441\u043b\u044f\u0446\u0438\u0438 (\u043c\u0441):", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0440\u0435\u043c\u044f \u043f\u0430\u0443\u0437\u044b (\u043c\u0441):", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0446\u0438\u043a\u043b\u043e\u0432:", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u0448\u0430\u0431\u043b\u043e\u043d", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
    # retranslateUi

