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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QFormLayout, QFrame, QGraphicsView, QHBoxLayout,
    QLabel, QMainWindow, QProgressBar, QPushButton,
    QScrollArea, QSizePolicy, QSpinBox, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1072, 895)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMaximumSize(QSize(300, 16777215))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 296, 873))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.frame = QFrame(self.scrollAreaWidgetContents)
        self.frame.setObjectName(u"frame")
        self.frame.setMaximumSize(QSize(16777215, 300))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.formLayout = QFormLayout(self.frame)
        self.formLayout.setObjectName(u"formLayout")
        self.pB_stopCamera = QPushButton(self.frame)
        self.pB_stopCamera.setObjectName(u"pB_stopCamera")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.pB_stopCamera)

        self.pB_startCamera = QPushButton(self.frame)
        self.pB_startCamera.setObjectName(u"pB_startCamera")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.pB_startCamera)

        self.cB_cameraName = QComboBox(self.frame)
        self.cB_cameraName.setObjectName(u"cB_cameraName")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.cB_cameraName)

        self.l_camera = QLabel(self.frame)
        self.l_camera.setObjectName(u"l_camera")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.l_camera)


        self.verticalLayout_3.addWidget(self.frame)

        self.frame_8 = QFrame(self.scrollAreaWidgetContents)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.formLayout_5 = QFormLayout(self.frame_8)
        self.formLayout_5.setObjectName(u"formLayout_5")
        self.label_11 = QLabel(self.frame_8)
        self.label_11.setObjectName(u"label_11")

        self.formLayout_5.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_11)

        self.dSB_scaleCamera = QDoubleSpinBox(self.frame_8)
        self.dSB_scaleCamera.setObjectName(u"dSB_scaleCamera")
        self.dSB_scaleCamera.setMinimum(10.000000000000000)
        self.dSB_scaleCamera.setMaximum(500.000000000000000)
        self.dSB_scaleCamera.setSingleStep(10.000000000000000)
        self.dSB_scaleCamera.setValue(40.000000000000000)

        self.formLayout_5.setWidget(0, QFormLayout.ItemRole.FieldRole, self.dSB_scaleCamera)

        self.chB_vMrirrorCamera = QCheckBox(self.frame_8)
        self.chB_vMrirrorCamera.setObjectName(u"chB_vMrirrorCamera")

        self.formLayout_5.setWidget(1, QFormLayout.ItemRole.LabelRole, self.chB_vMrirrorCamera)

        self.chB_hMrirrorCamera = QCheckBox(self.frame_8)
        self.chB_hMrirrorCamera.setObjectName(u"chB_hMrirrorCamera")

        self.formLayout_5.setWidget(1, QFormLayout.ItemRole.FieldRole, self.chB_hMrirrorCamera)

        self.pB_saveCamera = QPushButton(self.frame_8)
        self.pB_saveCamera.setObjectName(u"pB_saveCamera")

        self.formLayout_5.setWidget(2, QFormLayout.ItemRole.SpanningRole, self.pB_saveCamera)


        self.verticalLayout_3.addWidget(self.frame_8)

        self.litho_frame = QFrame(self.scrollAreaWidgetContents)
        self.litho_frame.setObjectName(u"litho_frame")
        self.litho_frame.setEnabled(False)
        self.litho_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.litho_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.formLayout_2 = QFormLayout(self.litho_frame)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.litho_showTime_l = QLabel(self.litho_frame)
        self.litho_showTime_l.setObjectName(u"litho_showTime_l")

        self.formLayout_2.setWidget(5, QFormLayout.ItemRole.LabelRole, self.litho_showTime_l)

        self.litho_pauseTime_l = QLabel(self.litho_frame)
        self.litho_pauseTime_l.setObjectName(u"litho_pauseTime_l")

        self.formLayout_2.setWidget(6, QFormLayout.ItemRole.LabelRole, self.litho_pauseTime_l)

        self.litho_cycles_l = QLabel(self.litho_frame)
        self.litho_cycles_l.setObjectName(u"litho_cycles_l")

        self.formLayout_2.setWidget(7, QFormLayout.ItemRole.LabelRole, self.litho_cycles_l)

        self.litho_showTime_sB = QSpinBox(self.litho_frame)
        self.litho_showTime_sB.setObjectName(u"litho_showTime_sB")
        self.litho_showTime_sB.setMinimum(1)
        self.litho_showTime_sB.setMaximum(100000)
        self.litho_showTime_sB.setValue(1000)

        self.formLayout_2.setWidget(5, QFormLayout.ItemRole.FieldRole, self.litho_showTime_sB)

        self.litho_pauseTime_sB = QSpinBox(self.litho_frame)
        self.litho_pauseTime_sB.setObjectName(u"litho_pauseTime_sB")
        self.litho_pauseTime_sB.setMinimum(0)
        self.litho_pauseTime_sB.setMaximum(100000)
        self.litho_pauseTime_sB.setValue(0)

        self.formLayout_2.setWidget(6, QFormLayout.ItemRole.FieldRole, self.litho_pauseTime_sB)

        self.litho_cycles_sB = QSpinBox(self.litho_frame)
        self.litho_cycles_sB.setObjectName(u"litho_cycles_sB")
        self.litho_cycles_sB.setMinimum(1)
        self.litho_cycles_sB.setMaximum(100)
        self.litho_cycles_sB.setValue(1)

        self.formLayout_2.setWidget(7, QFormLayout.ItemRole.FieldRole, self.litho_cycles_sB)

        self.litho_start_pB = QPushButton(self.litho_frame)
        self.litho_start_pB.setObjectName(u"litho_start_pB")
        self.litho_start_pB.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.litho_start_pB.sizePolicy().hasHeightForWidth())
        self.litho_start_pB.setSizePolicy(sizePolicy)
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        brush1 = QBrush(QColor(0, 170, 0, 255))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush1)
        brush2 = QBrush(QColor(0, 255, 0, 255))
        brush2.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Light, brush2)
        brush3 = QBrush(QColor(0, 212, 0, 255))
        brush3.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Midlight, brush3)
        brush4 = QBrush(QColor(0, 85, 0, 255))
        brush4.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Dark, brush4)
        brush5 = QBrush(QColor(0, 113, 0, 255))
        brush5.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Mid, brush5)
        brush6 = QBrush(QColor(255, 255, 255, 255))
        brush6.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.BrightText, brush6)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush6)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush1)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Shadow, brush)
        brush7 = QBrush(QColor(127, 212, 127, 255))
        brush7.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.AlternateBase, brush7)
        brush8 = QBrush(QColor(255, 255, 220, 255))
        brush8.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipBase, brush8)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipText, brush)
        brush9 = QBrush(QColor(0, 0, 0, 127))
        brush9.setStyle(Qt.BrushStyle.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, brush9)
#endif
#if QT_VERSION >= QT_VERSION_CHECK(6, 6, 0)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Accent, brush6)
#endif
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Light, brush2)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Midlight, brush3)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Dark, brush4)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Mid, brush5)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.BrightText, brush6)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush6)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Shadow, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.AlternateBase, brush7)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ToolTipBase, brush8)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ToolTipText, brush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, brush9)
#endif
#if QT_VERSION >= QT_VERSION_CHECK(6, 6, 0)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Accent, brush6)
#endif
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush4)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Light, brush2)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Midlight, brush3)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Dark, brush4)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Mid, brush5)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.BrightText, brush6)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Shadow, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.AlternateBase, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ToolTipBase, brush8)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ToolTipText, brush)
        brush10 = QBrush(QColor(0, 85, 0, 127))
        brush10.setStyle(Qt.BrushStyle.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, brush10)
#endif
        brush11 = QBrush(QColor(0, 221, 0, 255))
        brush11.setStyle(Qt.BrushStyle.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(6, 6, 0)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Accent, brush11)
#endif
        self.litho_start_pB.setPalette(palette)
        self.litho_start_pB.setAutoDefault(False)
        self.litho_start_pB.setFlat(False)

        self.formLayout_2.setWidget(4, QFormLayout.ItemRole.LabelRole, self.litho_start_pB)

        self.litho_stop_pB = QPushButton(self.litho_frame)
        self.litho_stop_pB.setObjectName(u"litho_stop_pB")
        palette1 = QPalette()
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        brush12 = QBrush(QColor(170, 0, 0, 255))
        brush12.setStyle(Qt.BrushStyle.SolidPattern)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush12)
        brush13 = QBrush(QColor(255, 0, 0, 255))
        brush13.setStyle(Qt.BrushStyle.SolidPattern)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Light, brush13)
        brush14 = QBrush(QColor(212, 0, 0, 255))
        brush14.setStyle(Qt.BrushStyle.SolidPattern)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Midlight, brush14)
        brush15 = QBrush(QColor(85, 0, 0, 255))
        brush15.setStyle(Qt.BrushStyle.SolidPattern)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Dark, brush15)
        brush16 = QBrush(QColor(113, 0, 0, 255))
        brush16.setStyle(Qt.BrushStyle.SolidPattern)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Mid, brush16)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.BrightText, brush6)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush6)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush12)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Shadow, brush)
        brush17 = QBrush(QColor(212, 127, 127, 255))
        brush17.setStyle(Qt.BrushStyle.SolidPattern)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.AlternateBase, brush17)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipBase, brush8)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipText, brush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, brush9)
#endif
#if QT_VERSION >= QT_VERSION_CHECK(6, 6, 0)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Accent, brush6)
#endif
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush12)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Light, brush13)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Midlight, brush14)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Dark, brush15)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Mid, brush16)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.BrightText, brush6)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush6)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush12)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Shadow, brush)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.AlternateBase, brush17)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ToolTipBase, brush8)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ToolTipText, brush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, brush9)
#endif
#if QT_VERSION >= QT_VERSION_CHECK(6, 6, 0)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Accent, brush6)
#endif
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush15)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush12)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Light, brush13)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Midlight, brush14)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Dark, brush15)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Mid, brush16)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.BrightText, brush6)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush12)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush12)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Shadow, brush)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.AlternateBase, brush12)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ToolTipBase, brush8)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ToolTipText, brush)
        brush18 = QBrush(QColor(85, 0, 0, 127))
        brush18.setStyle(Qt.BrushStyle.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, brush18)
#endif
        brush19 = QBrush(QColor(221, 0, 0, 255))
        brush19.setStyle(Qt.BrushStyle.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(6, 6, 0)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Accent, brush19)
#endif
        self.litho_stop_pB.setPalette(palette1)

        self.formLayout_2.setWidget(4, QFormLayout.ItemRole.FieldRole, self.litho_stop_pB)

        self.litho_progress_prBar = QProgressBar(self.litho_frame)
        self.litho_progress_prBar.setObjectName(u"litho_progress_prBar")
        self.litho_progress_prBar.setMinimumSize(QSize(0, 0))
        self.litho_progress_prBar.setValue(0)
        self.litho_progress_prBar.setTextVisible(True)
        self.litho_progress_prBar.setTextDirection(QProgressBar.Direction.TopToBottom)

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.SpanningRole, self.litho_progress_prBar)

        self.litho_bright_l = QLabel(self.litho_frame)
        self.litho_bright_l.setObjectName(u"litho_bright_l")

        self.formLayout_2.setWidget(8, QFormLayout.ItemRole.LabelRole, self.litho_bright_l)

        self.litho_bright_sB = QSpinBox(self.litho_frame)
        self.litho_bright_sB.setObjectName(u"litho_bright_sB")
        self.litho_bright_sB.setMaximum(255)
        self.litho_bright_sB.setValue(255)

        self.formLayout_2.setWidget(8, QFormLayout.ItemRole.FieldRole, self.litho_bright_sB)


        self.verticalLayout_3.addWidget(self.litho_frame)

        self.pB_maskSelect = QPushButton(self.scrollAreaWidgetContents)
        self.pB_maskSelect.setObjectName(u"pB_maskSelect")

        self.verticalLayout_3.addWidget(self.pB_maskSelect)

        self.frame_3 = QFrame(self.scrollAreaWidgetContents)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setEnabled(False)
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.formLayout_7 = QFormLayout(self.frame_3)
        self.formLayout_7.setObjectName(u"formLayout_7")
        self.l_align_maskName = QLabel(self.frame_3)
        self.l_align_maskName.setObjectName(u"l_align_maskName")
        self.l_align_maskName.setMaximumSize(QSize(16777215, 20))
        self.l_align_maskName.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout_7.setWidget(0, QFormLayout.ItemRole.SpanningRole, self.l_align_maskName)

        self.l_align_maskMini = QLabel(self.frame_3)
        self.l_align_maskMini.setObjectName(u"l_align_maskMini")
        self.l_align_maskMini.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout_7.setWidget(1, QFormLayout.ItemRole.SpanningRole, self.l_align_maskMini)

        self.l_align_scale = QLabel(self.frame_3)
        self.l_align_scale.setObjectName(u"l_align_scale")
        self.l_align_scale.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout_7.setWidget(2, QFormLayout.ItemRole.LabelRole, self.l_align_scale)

        self.dSB_align_scale = QDoubleSpinBox(self.frame_3)
        self.dSB_align_scale.setObjectName(u"dSB_align_scale")
        self.dSB_align_scale.setMaximum(600.000000000000000)
        self.dSB_align_scale.setValue(200.000000000000000)

        self.formLayout_7.setWidget(2, QFormLayout.ItemRole.FieldRole, self.dSB_align_scale)

        self.l_align_opacity = QLabel(self.frame_3)
        self.l_align_opacity.setObjectName(u"l_align_opacity")
        self.l_align_opacity.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout_7.setWidget(3, QFormLayout.ItemRole.LabelRole, self.l_align_opacity)

        self.dSB_align_opacity = QDoubleSpinBox(self.frame_3)
        self.dSB_align_opacity.setObjectName(u"dSB_align_opacity")
        self.dSB_align_opacity.setMaximum(100.000000000000000)
        self.dSB_align_opacity.setSingleStep(5.000000000000000)
        self.dSB_align_opacity.setValue(50.000000000000000)

        self.formLayout_7.setWidget(3, QFormLayout.ItemRole.FieldRole, self.dSB_align_opacity)

        self.l_align_coord_W = QLabel(self.frame_3)
        self.l_align_coord_W.setObjectName(u"l_align_coord_W")

        self.formLayout_7.setWidget(4, QFormLayout.ItemRole.LabelRole, self.l_align_coord_W)

        self.sB_align_coord_W = QSpinBox(self.frame_3)
        self.sB_align_coord_W.setObjectName(u"sB_align_coord_W")
        self.sB_align_coord_W.setMinimum(-4000)
        self.sB_align_coord_W.setMaximum(4000)
        self.sB_align_coord_W.setValue(1920)

        self.formLayout_7.setWidget(4, QFormLayout.ItemRole.FieldRole, self.sB_align_coord_W)

        self.l_align_coord_H = QLabel(self.frame_3)
        self.l_align_coord_H.setObjectName(u"l_align_coord_H")

        self.formLayout_7.setWidget(5, QFormLayout.ItemRole.LabelRole, self.l_align_coord_H)

        self.sB_align_coord_H = QSpinBox(self.frame_3)
        self.sB_align_coord_H.setObjectName(u"sB_align_coord_H")
        self.sB_align_coord_H.setMinimum(-4000)
        self.sB_align_coord_H.setMaximum(4000)
        self.sB_align_coord_H.setValue(1080)

        self.formLayout_7.setWidget(5, QFormLayout.ItemRole.FieldRole, self.sB_align_coord_H)

        self.chB_align_show = QCheckBox(self.frame_3)
        self.chB_align_show.setObjectName(u"chB_align_show")
        self.chB_align_show.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.chB_align_show.setCheckable(True)
        self.chB_align_show.setChecked(True)
        self.chB_align_show.setTristate(False)

        self.formLayout_7.setWidget(6, QFormLayout.ItemRole.LabelRole, self.chB_align_show)

        self.chB_align_noFrame = QCheckBox(self.frame_3)
        self.chB_align_noFrame.setObjectName(u"chB_align_noFrame")

        self.formLayout_7.setWidget(6, QFormLayout.ItemRole.FieldRole, self.chB_align_noFrame)

        self.chB_align_mirrorV = QCheckBox(self.frame_3)
        self.chB_align_mirrorV.setObjectName(u"chB_align_mirrorV")

        self.formLayout_7.setWidget(7, QFormLayout.ItemRole.LabelRole, self.chB_align_mirrorV)

        self.chB_align_mirrorH = QCheckBox(self.frame_3)
        self.chB_align_mirrorH.setObjectName(u"chB_align_mirrorH")

        self.formLayout_7.setWidget(7, QFormLayout.ItemRole.FieldRole, self.chB_align_mirrorH)


        self.verticalLayout_3.addWidget(self.frame_3)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_2.addWidget(self.scrollArea)

        self.graphicsView = QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setFrameShape(QFrame.Shape.NoFrame)

        self.horizontalLayout_2.addWidget(self.graphicsView)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.litho_start_pB.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pB_stopCamera.setText(QCoreApplication.translate("MainWindow", u"\u23f8 \u0421\u0442\u043e\u043f", None))
        self.pB_startCamera.setText(QCoreApplication.translate("MainWindow", u"\u25b6 \u0421\u0442\u0430\u0440\u0442", None))
        self.l_camera.setText(QCoreApplication.translate("MainWindow", u"\u041a\u0430\u043c\u0435\u0440\u0430:", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\u041c\u0430\u0441\u0448\u0442\u0430\u0431:", None))
        self.chB_vMrirrorCamera.setText(QCoreApplication.translate("MainWindow", u"\u043e\u0442\u0440\u0430\u0437\u0438\u0442\u044c\n"
"\u0432\u0435\u0440\u0442\u0438\u043a\u0430\u043b\u044c\u043d\u043e", None))
        self.chB_hMrirrorCamera.setText(QCoreApplication.translate("MainWindow", u"\u043e\u0442\u0440\u0430\u0437\u0438\u0442\u044c\n"
"\u0433\u043e\u0440\u0438\u0437\u043e\u043d\u0442\u0430\u043b\u044c\u043d\u043e", None))
        self.pB_saveCamera.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u0438\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435", None))
        self.litho_showTime_l.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0440\u0435\u043c\u044f \u0442\u0440\u0430\u043d\u0441\u043b\u044f\u0446\u0438\u0438 (\u043c\u0441):", None))
        self.litho_pauseTime_l.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0440\u0435\u043c\u044f \u043f\u0430\u0443\u0437\u044b (\u043c\u0441):", None))
        self.litho_cycles_l.setText(QCoreApplication.translate("MainWindow", u"\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0446\u0438\u043a\u043b\u043e\u0432:", None))
        self.litho_start_pB.setText(QCoreApplication.translate("MainWindow", u"\u25b6 \u0421\u0442\u0430\u0440\u0442", None))
        self.litho_stop_pB.setText(QCoreApplication.translate("MainWindow", u"\u23f8 \u0421\u0442\u043e\u043f", None))
        self.litho_bright_l.setText(QCoreApplication.translate("MainWindow", u"\u042f\u0440\u043a\u043e\u0441\u0442\u044c:", None))
        self.pB_maskSelect.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u0448\u0430\u0431\u043b\u043e\u043d", None))
        self.l_align_maskName.setText(QCoreApplication.translate("MainWindow", u"\u0438\u043c\u044f \u0448\u0430\u0431\u043b\u043e\u043d\u0430.png", None))
        self.l_align_maskMini.setText(QCoreApplication.translate("MainWindow", u"\u0448\u0430\u0431\u043b\u043e\u043d \u043d\u0435 \u0432\u044b\u0431\u0440\u0430\u043d", None))
        self.l_align_scale.setText(QCoreApplication.translate("MainWindow", u"\u043c\u0430\u0441\u0448\u0442\u0430\u0431", None))
        self.l_align_opacity.setText(QCoreApplication.translate("MainWindow", u"\u043f\u0440\u043e\u0437\u0440\u0430\u0447\u043d\u043e\u0441\u0442\u044c", None))
        self.l_align_coord_W.setText(QCoreApplication.translate("MainWindow", u"\u043f\u043e\u043b\u043e\u0436\u0435\u043d\u0438\u0435 (X)", None))
        self.l_align_coord_H.setText(QCoreApplication.translate("MainWindow", u"\u043f\u043e\u043b\u043e\u0436\u0435\u043d\u0438\u0435 (Y)", None))
        self.chB_align_show.setText(QCoreApplication.translate("MainWindow", u"\u043f\u043e\u043a\u0430\u0437\u0430\u0442\u044c\n"
"\u0448\u0430\u0431\u043b\u043e\u043d", None))
        self.chB_align_noFrame.setText(QCoreApplication.translate("MainWindow", u"\u0431\u0435\u0437 \u0440\u0430\u043c\u043a\u0438", None))
        self.chB_align_mirrorV.setText(QCoreApplication.translate("MainWindow", u"\u043e\u0442\u0440\u0430\u0437\u0438\u0442\u044c\n"
"\u0432\u0435\u0440\u0442\u0438\u043a\u0430\u043b\u044c\u043d\u043e", None))
        self.chB_align_mirrorH.setText(QCoreApplication.translate("MainWindow", u"\u043e\u0442\u0440\u0430\u0437\u0438\u0442\u044c\n"
"\u0433\u043e\u0440\u0438\u0437\u043e\u043d\u0442\u0430\u043b\u044c\u043d\u043e", None))
    # retranslateUi

