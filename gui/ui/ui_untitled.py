# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitledXsCHvU.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QProgressBar, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

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
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout_3.addWidget(self.label)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_3.addWidget(self.pushButton)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.progressBar_vector = QProgressBar(self.centralwidget)
        self.progressBar_vector.setObjectName(u"progressBar_vector")
        self.progressBar_vector.setValue(0)

        self.horizontalLayout_2.addWidget(self.progressBar_vector)

        self.pbt_vector = QPushButton(self.centralwidget)
        self.pbt_vector.setObjectName(u"pbt_vector")

        self.horizontalLayout_2.addWidget(self.pbt_vector)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.progressBar_scan = QProgressBar(self.centralwidget)
        self.progressBar_scan.setObjectName(u"progressBar_scan")
        self.progressBar_scan.setValue(0)

        self.horizontalLayout.addWidget(self.progressBar_scan)

        self.pbt_scan = QPushButton(self.centralwidget)
        self.pbt_scan.setObjectName(u"pbt_scan")

        self.horizontalLayout.addWidget(self.pbt_scan)


        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Init", None))
        self.pbt_vector.setText(QCoreApplication.translate("MainWindow", u"Vector", None))
        self.pbt_scan.setText(QCoreApplication.translate("MainWindow", u"Scan", None))
    # retranslateUi

