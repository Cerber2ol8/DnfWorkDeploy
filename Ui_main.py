# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QHBoxLayout,
    QLabel, QLayout, QMainWindow, QPushButton,
    QRadioButton, QSizePolicy, QSlider, QSpacerItem,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(963, 720)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_3 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_4.addWidget(self.label_2)

        self.combo_device = QComboBox(self.centralwidget)
        self.combo_device.setObjectName(u"combo_device")
        self.combo_device.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_4.addWidget(self.combo_device)

        self.keyboard_mode = QCheckBox(self.centralwidget)
        self.keyboard_mode.setObjectName(u"keyboard_mode")

        self.horizontalLayout_4.addWidget(self.keyboard_mode)

        self.flip = QCheckBox(self.centralwidget)
        self.flip.setObjectName(u"flip")

        self.horizontalLayout_4.addWidget(self.flip)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetFixedSize)
        self.horizontalLayout_2.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_7.addWidget(self.label)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")

        self.verticalLayout_3.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.label_info2 = QLabel(self.centralwidget)
        self.label_info2.setObjectName(u"label_info2")

        self.verticalLayout_13.addWidget(self.label_info2)

        self.radioButton = QRadioButton(self.centralwidget)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setEnabled(False)
        self.radioButton.setChecked(True)

        self.verticalLayout_13.addWidget(self.radioButton)

        self.button_get_map = QPushButton(self.centralwidget)
        self.button_get_map.setObjectName(u"button_get_map")

        self.verticalLayout_13.addWidget(self.button_get_map)

        self.button_reset_map = QPushButton(self.centralwidget)
        self.button_reset_map.setObjectName(u"button_reset_map")

        self.verticalLayout_13.addWidget(self.button_reset_map)

        self.button_save_map = QPushButton(self.centralwidget)
        self.button_save_map.setObjectName(u"button_save_map")

        self.verticalLayout_13.addWidget(self.button_save_map)

        self.button_move_up = QPushButton(self.centralwidget)
        self.button_move_up.setObjectName(u"button_move_up")

        self.verticalLayout_13.addWidget(self.button_move_up)

        self.button_move_down = QPushButton(self.centralwidget)
        self.button_move_down.setObjectName(u"button_move_down")

        self.verticalLayout_13.addWidget(self.button_move_down)

        self.button_move_left = QPushButton(self.centralwidget)
        self.button_move_left.setObjectName(u"button_move_left")

        self.verticalLayout_13.addWidget(self.button_move_left)

        self.button_move_right = QPushButton(self.centralwidget)
        self.button_move_right.setObjectName(u"button_move_right")

        self.verticalLayout_13.addWidget(self.button_move_right)

        self.button_move_stop = QPushButton(self.centralwidget)
        self.button_move_stop.setObjectName(u"button_move_stop")

        self.verticalLayout_13.addWidget(self.button_move_stop)

        self.button_attack = QPushButton(self.centralwidget)
        self.button_attack.setObjectName(u"button_attack")

        self.verticalLayout_13.addWidget(self.button_attack)

        self.button_test_skill = QPushButton(self.centralwidget)
        self.button_test_skill.setObjectName(u"button_test_skill")

        self.verticalLayout_13.addWidget(self.button_test_skill)

        self.button_cursor = QPushButton(self.centralwidget)
        self.button_cursor.setObjectName(u"button_cursor")

        self.verticalLayout_13.addWidget(self.button_cursor)


        self.horizontalLayout_10.addLayout(self.verticalLayout_13)

        self.verticalLayout_15 = QVBoxLayout()
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.label_info1 = QLabel(self.centralwidget)
        self.label_info1.setObjectName(u"label_info1")

        self.verticalLayout_15.addWidget(self.label_info1)

        self.button_reload = QPushButton(self.centralwidget)
        self.button_reload.setObjectName(u"button_reload")

        self.verticalLayout_15.addWidget(self.button_reload)

        self.button_back = QPushButton(self.centralwidget)
        self.button_back.setObjectName(u"button_back")

        self.verticalLayout_15.addWidget(self.button_back)

        self.button_start = QPushButton(self.centralwidget)
        self.button_start.setObjectName(u"button_start")

        self.verticalLayout_15.addWidget(self.button_start)

        self.button_stop = QPushButton(self.centralwidget)
        self.button_stop.setObjectName(u"button_stop")

        self.verticalLayout_15.addWidget(self.button_stop)


        self.horizontalLayout_10.addLayout(self.verticalLayout_15)


        self.verticalLayout_3.addLayout(self.horizontalLayout_10)


        self.horizontalLayout_7.addLayout(self.verticalLayout_3)


        self.horizontalLayout_2.addLayout(self.horizontalLayout_7)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setEnabled(True)
        self.textEdit.setFocusPolicy(Qt.NoFocus)
        self.textEdit.setAutoFillBackground(False)
        self.textEdit.setReadOnly(True)

        self.horizontalLayout.addWidget(self.textEdit)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_fps = QLabel(self.centralwidget)
        self.label_fps.setObjectName(u"label_fps")

        self.verticalLayout_5.addWidget(self.label_fps)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_info_freq = QLabel(self.centralwidget)
        self.label_info_freq.setObjectName(u"label_info_freq")

        self.verticalLayout_4.addWidget(self.label_info_freq)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.slider_frame_req = QSlider(self.centralwidget)
        self.slider_frame_req.setObjectName(u"slider_frame_req")
        self.slider_frame_req.setMinimum(1)
        self.slider_frame_req.setMaximum(30)
        self.slider_frame_req.setOrientation(Qt.Horizontal)

        self.horizontalLayout_6.addWidget(self.slider_frame_req)

        self.label_info_frame_freq = QLabel(self.centralwidget)
        self.label_info_frame_freq.setObjectName(u"label_info_frame_freq")

        self.horizontalLayout_6.addWidget(self.label_info_frame_freq)


        self.verticalLayout_4.addLayout(self.horizontalLayout_6)


        self.horizontalLayout_5.addLayout(self.verticalLayout_4)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_info_enemy_x = QLabel(self.centralwidget)
        self.label_info_enemy_x.setObjectName(u"label_info_enemy_x")

        self.verticalLayout_8.addWidget(self.label_info_enemy_x)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.slider_attx = QSlider(self.centralwidget)
        self.slider_attx.setObjectName(u"slider_attx")
        self.slider_attx.setMinimum(100)
        self.slider_attx.setMaximum(800)
        self.slider_attx.setSingleStep(40)
        self.slider_attx.setOrientation(Qt.Horizontal)

        self.horizontalLayout_13.addWidget(self.slider_attx)

        self.label_attx = QLabel(self.centralwidget)
        self.label_attx.setObjectName(u"label_attx")

        self.horizontalLayout_13.addWidget(self.label_attx)


        self.verticalLayout_8.addLayout(self.horizontalLayout_13)


        self.horizontalLayout_5.addLayout(self.verticalLayout_8)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_7.addWidget(self.label_3)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.slider_atty = QSlider(self.centralwidget)
        self.slider_atty.setObjectName(u"slider_atty")
        self.slider_atty.setMinimum(150)
        self.slider_atty.setMaximum(800)
        self.slider_atty.setSingleStep(40)
        self.slider_atty.setOrientation(Qt.Horizontal)

        self.horizontalLayout_12.addWidget(self.slider_atty)

        self.label_atty = QLabel(self.centralwidget)
        self.label_atty.setObjectName(u"label_atty")

        self.horizontalLayout_12.addWidget(self.label_atty)


        self.verticalLayout_7.addLayout(self.horizontalLayout_12)


        self.horizontalLayout_5.addLayout(self.verticalLayout_7)


        self.verticalLayout_5.addLayout(self.horizontalLayout_5)


        self.verticalLayout_2.addLayout(self.verticalLayout_5)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")

        self.horizontalLayout.addLayout(self.horizontalLayout_8)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout.setStretch(1, 100)

        self.horizontalLayout_3.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Device", None))
        self.keyboard_mode.setText(QCoreApplication.translate("MainWindow", u"KeyBoard Input Mode", None))
        self.flip.setText(QCoreApplication.translate("MainWindow", u"Flip", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:20pt;\">Loading</span></p></body></html>", None))
        self.label_info2.setText(QCoreApplication.translate("MainWindow", u"\u5730\u56fe/\u529f\u80fd\u6d4b\u8bd5", None))
        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"\u76ee\u524d\u4ec5\u652f\u6301\u5c71\u810a", None))
        self.button_get_map.setText(QCoreApplication.translate("MainWindow", u"get map", None))
        self.button_reset_map.setText(QCoreApplication.translate("MainWindow", u"reset map", None))
        self.button_save_map.setText(QCoreApplication.translate("MainWindow", u"save map", None))
        self.button_move_up.setText(QCoreApplication.translate("MainWindow", u"move up", None))
        self.button_move_down.setText(QCoreApplication.translate("MainWindow", u"move down", None))
        self.button_move_left.setText(QCoreApplication.translate("MainWindow", u"move left", None))
        self.button_move_right.setText(QCoreApplication.translate("MainWindow", u"move right", None))
        self.button_move_stop.setText(QCoreApplication.translate("MainWindow", u"move stop", None))
        self.button_attack.setText(QCoreApplication.translate("MainWindow", u"test_attack", None))
        self.button_test_skill.setText(QCoreApplication.translate("MainWindow", u"test skill", None))
        self.button_cursor.setText(QCoreApplication.translate("MainWindow", u"show_cursor", None))
        self.label_info1.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">\u4f7f\u7528\u6761\u6b3e\uff1a</span></p><p><span style=\" font-weight:600;\">\u672c\u7a0b\u5e8f\u4ec5\u4f9b\u6d4b\u8bd5\u5b66\u4e60\u4f7f\u7528\uff0c\u4e0d\u9488\u5bf9\u4efb\u4f55\u7a0b\u5e8f\u548c\u4e3b\u4f53\u3002</span></p><p><span style=\" font-weight:600;\">\u7981\u6b62\u4efb\u4f55\u5f62\u5f0f\u7684\u975e\u6cd5\u7528\u9014\u548c\u76c8\u5229\u6d3b\u52a8\uff0c</span></p><p><span style=\" font-weight:600;\">\u4efb\u4f55\u672a\u7ecf\u5141\u8bb8\u7684\u4f20\u64ad\u548c\u76c8\u5229\u4e0e\u4f5c\u8005\u672c\u4eba\u65e0\u5173\u3002</span></p><p><span style=\" font-weight:600;\">\u5f00\u59cb\u4f7f\u7528\u4e0b\u65b9\u7684\u4efb\u4e00\u529f\u80fd\uff0c\u5373\u89c6\u4e3a\u8ba4\u540c\u4e0a\u8ff0\u6761\u6b3e\uff01</span></p></body></html>", None))
        self.button_reload.setText(QCoreApplication.translate("MainWindow", u"RELOAD CONFIG", None))
        self.button_back.setText(QCoreApplication.translate("MainWindow", u"RESET GAME", None))
        self.button_start.setText(QCoreApplication.translate("MainWindow", u"START DETECTION", None))
        self.button_stop.setText(QCoreApplication.translate("MainWindow", u"STOP DETECTION", None))
        self.label_fps.setText(QCoreApplication.translate("MainWindow", u"frame rate", None))
        self.label_info_freq.setText(QCoreApplication.translate("MainWindow", u"\u68c0\u6d4b\u9891\u7387\uff08\u8d8a\u5c0f\u8d8a\u597d\uff0c\u4f46\u5403\u6027\u80fd\uff09", None))
        self.label_info_frame_freq.setText(QCoreApplication.translate("MainWindow", u"\u68c0\u6d4b\u9891\u7387", None))
        self.label_info_enemy_x.setText(QCoreApplication.translate("MainWindow", u"\u653b\u51fbx\u65b9\u5411\u9608\u503c", None))
        self.label_attx.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u653b\u51fby\u65b9\u5411\u9608\u503c", None))
        self.label_atty.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
    # retranslateUi

