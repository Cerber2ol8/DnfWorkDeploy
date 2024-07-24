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
    QSizePolicy, QSpacerItem, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(907, 534)
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

        self.button_start = QPushButton(self.centralwidget)
        self.button_start.setObjectName(u"button_start")

        self.verticalLayout_15.addWidget(self.button_start)

        self.button_stop = QPushButton(self.centralwidget)
        self.button_stop.setObjectName(u"button_stop")

        self.verticalLayout_15.addWidget(self.button_stop)


        self.horizontalLayout_10.addLayout(self.verticalLayout_15)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_6)


        self.verticalLayout_3.addLayout(self.horizontalLayout_10)


        self.horizontalLayout_7.addLayout(self.verticalLayout_3)


        self.horizontalLayout_2.addLayout(self.horizontalLayout_7)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_fps = QLabel(self.centralwidget)
        self.label_fps.setObjectName(u"label_fps")

        self.verticalLayout_2.addWidget(self.label_fps)

        self.button_reload = QPushButton(self.centralwidget)
        self.button_reload.setObjectName(u"button_reload")

        self.verticalLayout_2.addWidget(self.button_reload)

        self.button_back = QPushButton(self.centralwidget)
        self.button_back.setObjectName(u"button_back")

        self.verticalLayout_2.addWidget(self.button_back)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setReadOnly(True)

        self.horizontalLayout.addWidget(self.textEdit)


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
        self.flip.setText(QCoreApplication.translate("MainWindow", u"Flip", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:20pt;\">Loading</span></p></body></html>", None))
        self.label_info2.setText(QCoreApplication.translate("MainWindow", u"\u529f\u80fd\u6d4b\u8bd5\u533a\u57df", None))
        self.button_move_up.setText(QCoreApplication.translate("MainWindow", u"move up", None))
        self.button_move_down.setText(QCoreApplication.translate("MainWindow", u"move down", None))
        self.button_move_left.setText(QCoreApplication.translate("MainWindow", u"move left", None))
        self.button_move_right.setText(QCoreApplication.translate("MainWindow", u"move right", None))
        self.button_move_stop.setText(QCoreApplication.translate("MainWindow", u"move stop", None))
        self.button_test_skill.setText(QCoreApplication.translate("MainWindow", u"test skill", None))
        self.button_cursor.setText(QCoreApplication.translate("MainWindow", u"show_cursor", None))
        self.label_info1.setText(QCoreApplication.translate("MainWindow", u"\u8fd0\u884c\u533a\u57df", None))
        self.button_start.setText(QCoreApplication.translate("MainWindow", u"START DETECTION", None))
        self.button_stop.setText(QCoreApplication.translate("MainWindow", u"STOP DETECTION", None))
        self.label_fps.setText(QCoreApplication.translate("MainWindow", u"frame rate", None))
        self.button_reload.setText(QCoreApplication.translate("MainWindow", u"RELOAD CONF", None))
        self.button_back.setText(QCoreApplication.translate("MainWindow", u"PHONE BACK", None))
    # retranslateUi

