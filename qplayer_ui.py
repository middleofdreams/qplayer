# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qplayer.ui'
#
# Created: Thu Oct  7 08:27:26 2010
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(739, 393)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(14, 2, 14, 2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.prevBtn = QtGui.QPushButton(self.frame)
        self.prevBtn.setMinimumSize(QtCore.QSize(33, 33))
        self.prevBtn.setMaximumSize(QtCore.QSize(33, 33))
        self.prevBtn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.prevBtn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/media-seek-backward.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.prevBtn.setIcon(icon)
        self.prevBtn.setIconSize(QtCore.QSize(28, 28))
        self.prevBtn.setFlat(True)
        self.prevBtn.setObjectName("prevBtn")
        self.horizontalLayout.addWidget(self.prevBtn)
        self.playBtn = QtGui.QPushButton(self.frame)
        self.playBtn.setMinimumSize(QtCore.QSize(36, 36))
        self.playBtn.setMaximumSize(QtCore.QSize(40, 40))
        self.playBtn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.playBtn.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.playBtn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/media-playback-pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(":/icons/media-playback-start.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.playBtn.setIcon(icon1)
        self.playBtn.setIconSize(QtCore.QSize(32, 32))
        self.playBtn.setAutoExclusive(False)
        self.playBtn.setAutoDefault(False)
        self.playBtn.setDefault(False)
        self.playBtn.setFlat(True)
        self.playBtn.setObjectName("playBtn")
        self.horizontalLayout.addWidget(self.playBtn)
        self.stopBtn = QtGui.QPushButton(self.frame)
        self.stopBtn.setMinimumSize(QtCore.QSize(33, 33))
        self.stopBtn.setMaximumSize(QtCore.QSize(33, 33))
        self.stopBtn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.stopBtn.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/media-playback-stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stopBtn.setIcon(icon2)
        self.stopBtn.setIconSize(QtCore.QSize(28, 28))
        self.stopBtn.setFlat(True)
        self.stopBtn.setObjectName("stopBtn")
        self.horizontalLayout.addWidget(self.stopBtn)
        self.nextBtn = QtGui.QPushButton(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nextBtn.sizePolicy().hasHeightForWidth())
        self.nextBtn.setSizePolicy(sizePolicy)
        self.nextBtn.setMinimumSize(QtCore.QSize(33, 33))
        self.nextBtn.setMaximumSize(QtCore.QSize(33, 33))
        self.nextBtn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.nextBtn.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/media-seek-forward.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.nextBtn.setIcon(icon3)
        self.nextBtn.setIconSize(QtCore.QSize(28, 28))
        self.nextBtn.setFlat(True)
        self.nextBtn.setObjectName("nextBtn")
        self.horizontalLayout.addWidget(self.nextBtn)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.volSlider = QtGui.QSlider(self.frame)
        self.volSlider.setMaximumSize(QtCore.QSize(70, 16777215))
        self.volSlider.setMaximum(20)
        self.volSlider.setSingleStep(1)
        self.volSlider.setPageStep(2)
        self.volSlider.setProperty("value", 0)
        self.volSlider.setOrientation(QtCore.Qt.Horizontal)
        self.volSlider.setTickPosition(QtGui.QSlider.NoTicks)
        self.volSlider.setObjectName("volSlider")
        self.horizontalLayout.addWidget(self.volSlider)
        self.volImg = QtGui.QPushButton(self.frame)
        self.volImg.setEnabled(True)
        self.volImg.setMinimumSize(QtCore.QSize(30, 30))
        self.volImg.setMaximumSize(QtCore.QSize(30, 30))
        self.volImg.setFocusPolicy(QtCore.Qt.NoFocus)
        self.volImg.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/audio-volume-high.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.volImg.setIcon(icon4)
        self.volImg.setIconSize(QtCore.QSize(21, 21))
        self.volImg.setCheckable(True)
        self.volImg.setFlat(True)
        self.volImg.setObjectName("volImg")
        self.horizontalLayout.addWidget(self.volImg)
        self.verticalLayout_2.addWidget(self.frame)
        self.frame_2 = QtGui.QFrame(self.centralwidget)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.progressBar = QtGui.QProgressBar(self.frame_2)
        self.progressBar.setMaximumSize(QtCore.QSize(16777215, 12))
        self.progressBar.setSizeIncrement(QtCore.QSize(0, 0))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_2.addWidget(self.progressBar)
        self.verticalLayout_2.addWidget(self.frame_2)
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.currentplaylist = QtGui.QWidget()
        self.currentplaylist.setObjectName("currentplaylist")
        self.verticalLayout = QtGui.QVBoxLayout(self.currentplaylist)
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeWidget = QtGui.QTreeWidget(self.currentplaylist)
        self.treeWidget.setObjectName("treeWidget")
        self.verticalLayout.addWidget(self.treeWidget)
        self.tabWidget.addTab(self.currentplaylist, "")
        self.musiccollection = QtGui.QWidget()
        self.musiccollection.setObjectName("musiccollection")
        self.tabWidget.addTab(self.musiccollection, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 739, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setAutoFillBackground(False)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "no", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(1, QtGui.QApplication.translate("MainWindow", "Track", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(2, QtGui.QApplication.translate("MainWindow", "Artist", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(3, QtGui.QApplication.translate("MainWindow", "Album", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(4, QtGui.QApplication.translate("MainWindow", "File name", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(5, QtGui.QApplication.translate("MainWindow", "File path", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.currentplaylist), QtGui.QApplication.translate("MainWindow", "Current Playlist", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.musiccollection), QtGui.QApplication.translate("MainWindow", "Music Collection", None, QtGui.QApplication.UnicodeUTF8))

import res_rc
