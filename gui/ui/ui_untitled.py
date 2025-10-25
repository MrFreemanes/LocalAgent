# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitledIkfgap.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(600, 430)
        MainWindow.setMinimumSize(QSize(600, 430))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label_dir = QLabel(self.centralwidget)
        self.label_dir.setObjectName(u"label_dir")

        self.horizontalLayout.addWidget(self.label_dir)

        self.btn_init = QPushButton(self.centralwidget)
        self.btn_init.setObjectName(u"btn_init")

        self.horizontalLayout.addWidget(self.btn_init)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_progress = QHBoxLayout()
        self.horizontalLayout_progress.setObjectName(u"horizontalLayout_progress")

        self.verticalLayout.addLayout(self.horizontalLayout_progress)

        self.textEdit_chat = QTextEdit(self.centralwidget)
        self.textEdit_chat.setObjectName(u"textEdit_chat")
        self.textEdit_chat.setReadOnly(True)

        self.verticalLayout.addWidget(self.textEdit_chat)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.lineEdit_massage = QLineEdit(self.centralwidget)
        self.lineEdit_massage.setObjectName(u"lineEdit_massage")
        self.lineEdit_massage.setMaxLength(200)
        self.lineEdit_massage.setClearButtonEnabled(True)

        self.horizontalLayout_2.addWidget(self.lineEdit_massage)

        self.btn_massage = QPushButton(self.centralwidget)
        self.btn_massage.setObjectName(u"btn_massage")

        self.horizontalLayout_2.addWidget(self.btn_massage)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_dir.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0434\u0438\u0440\u0435\u043a\u0442\u043e\u0440\u0438\u044e", None))
        self.btn_init.setText(QCoreApplication.translate("MainWindow", u"Init", None))
        self.lineEdit_massage.setInputMask("")
        self.lineEdit_massage.setText("")
        self.lineEdit_massage.setPlaceholderText("")
        self.btn_massage.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u044c", None))
    # retranslateUi

