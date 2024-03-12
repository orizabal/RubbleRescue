# Form implementation generated from reading ui file 'ui/views/main.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1148, 927)
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, 600, 271, 261))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.Legend = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.Legend.setContentsMargins(10, 10, 0, 0)
        self.Legend.setObjectName("Legend")
        self.LegendTitle = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.LegendTitle.setObjectName("LegendTitle")
        self.Legend.addWidget(self.LegendTitle)
        self.VictimLegendItem = QtWidgets.QHBoxLayout()
        self.VictimLegendItem.setContentsMargins(0, -1, -1, -1)
        self.VictimLegendItem.setObjectName("VictimLegendItem")
        self.PotentialVictimLegendIcon = QtWidgets.QGraphicsView(parent=self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PotentialVictimLegendIcon.sizePolicy().hasHeightForWidth())
        self.PotentialVictimLegendIcon.setSizePolicy(sizePolicy)
        self.PotentialVictimLegendIcon.setMaximumSize(QtCore.QSize(25, 25))
        self.PotentialVictimLegendIcon.setObjectName("PotentialVictimLegendIcon")
        self.VictimLegendItem.addWidget(self.PotentialVictimLegendIcon)
        self.VictimLegendItemLabel = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.VictimLegendItemLabel.setObjectName("VictimLegendItemLabel")
        self.VictimLegendItem.addWidget(self.VictimLegendItemLabel)
        self.Legend.addLayout(self.VictimLegendItem)
        self.RescuedVictimLegendItem = QtWidgets.QHBoxLayout()
        self.RescuedVictimLegendItem.setContentsMargins(0, 0, -1, -1)
        self.RescuedVictimLegendItem.setObjectName("RescuedVictimLegendItem")
        self.RescuedVictimLegendIcon = QtWidgets.QGraphicsView(parent=self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.RescuedVictimLegendIcon.sizePolicy().hasHeightForWidth())
        self.RescuedVictimLegendIcon.setSizePolicy(sizePolicy)
        self.RescuedVictimLegendIcon.setMaximumSize(QtCore.QSize(25, 25))
        self.RescuedVictimLegendIcon.setObjectName("RescuedVictimLegendIcon")
        self.RescuedVictimLegendItem.addWidget(self.RescuedVictimLegendIcon)
        self.RescuedVictimLegendItemLabel = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.RescuedVictimLegendItemLabel.setObjectName("RescuedVictimLegendItemLabel")
        self.RescuedVictimLegendItem.addWidget(self.RescuedVictimLegendItemLabel)
        self.Legend.addLayout(self.RescuedVictimLegendItem)
        self.ModuleLegendItem = QtWidgets.QHBoxLayout()
        self.ModuleLegendItem.setContentsMargins(0, 0, -1, -1)
        self.ModuleLegendItem.setObjectName("ModuleLegendItem")
        self.ModuleLegendIcon = QtWidgets.QGraphicsView(parent=self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ModuleLegendIcon.sizePolicy().hasHeightForWidth())
        self.ModuleLegendIcon.setSizePolicy(sizePolicy)
        self.ModuleLegendIcon.setMaximumSize(QtCore.QSize(25, 25))
        self.ModuleLegendIcon.setObjectName("ModuleLegendIcon")
        self.ModuleLegendItem.addWidget(self.ModuleLegendIcon)
        self.ModuleLegendItemLabel = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.ModuleLegendItemLabel.setObjectName("ModuleLegendItemLabel")
        self.ModuleLegendItem.addWidget(self.ModuleLegendItemLabel)
        self.Legend.addLayout(self.ModuleLegendItem)
        self.TMLegendItem = QtWidgets.QHBoxLayout()
        self.TMLegendItem.setContentsMargins(0, 0, -1, -1)
        self.TMLegendItem.setObjectName("TMLegendItem")
        self.TMLegendIcon = QtWidgets.QGraphicsView(parent=self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TMLegendIcon.sizePolicy().hasHeightForWidth())
        self.TMLegendIcon.setSizePolicy(sizePolicy)
        self.TMLegendIcon.setMaximumSize(QtCore.QSize(25, 25))
        self.TMLegendIcon.setObjectName("TMLegendIcon")
        self.TMLegendItem.addWidget(self.TMLegendIcon)
        self.TMLegendItemLabel = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.TMLegendItemLabel.setObjectName("TMLegendItemLabel")
        self.TMLegendItem.addWidget(self.TMLegendItemLabel)
        self.Legend.addLayout(self.TMLegendItem)
        self.UserLegendItem = QtWidgets.QHBoxLayout()
        self.UserLegendItem.setContentsMargins(-1, 0, -1, -1)
        self.UserLegendItem.setObjectName("UserLegendItem")
        self.UserLegendIcon = QtWidgets.QGraphicsView(parent=self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.UserLegendIcon.sizePolicy().hasHeightForWidth())
        self.UserLegendIcon.setSizePolicy(sizePolicy)
        self.UserLegendIcon.setMaximumSize(QtCore.QSize(25, 25))
        self.UserLegendIcon.setObjectName("UserLegendIcon")
        self.UserLegendItem.addWidget(self.UserLegendIcon)
        self.UserLegendItemLabel = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.UserLegendItemLabel.setObjectName("UserLegendItemLabel")
        self.UserLegendItem.addWidget(self.UserLegendItemLabel)
        self.Legend.addLayout(self.UserLegendItem)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(parent=self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(30, 20, 271, 581))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.VictimList = QtWidgets.QListView(parent=self.verticalLayoutWidget_2)
        self.VictimList.setObjectName("VictimList")
        self.verticalLayout_2.addWidget(self.VictimList)
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(299, 19, 831, 841))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=self.frame)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(544, 729, 271, 91))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.MapToggles = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.MapToggles.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.MapToggles.setContentsMargins(10, 10, 10, 15)
        self.MapToggles.setObjectName("MapToggles")
        self.PastVictimsToggle = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PastVictimsToggle.sizePolicy().hasHeightForWidth())
        self.PastVictimsToggle.setSizePolicy(sizePolicy)
        self.PastVictimsToggle.setMaximumSize(QtCore.QSize(75, 75))
        self.PastVictimsToggle.setCheckable(True)
        self.PastVictimsToggle.setObjectName("PastVictimsToggle")
        self.MapToggles.addWidget(self.PastVictimsToggle)
        self.ModulesToggle = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ModulesToggle.sizePolicy().hasHeightForWidth())
        self.ModulesToggle.setSizePolicy(sizePolicy)
        self.ModulesToggle.setMaximumSize(QtCore.QSize(75, 75))
        self.ModulesToggle.setCheckable(True)
        self.ModulesToggle.setObjectName("ModulesToggle")
        self.MapToggles.addWidget(self.ModulesToggle)
        self.TeamToggle = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TeamToggle.sizePolicy().hasHeightForWidth())
        self.TeamToggle.setSizePolicy(sizePolicy)
        self.TeamToggle.setMaximumSize(QtCore.QSize(75, 75))
        self.TeamToggle.setCheckable(True)
        self.TeamToggle.setObjectName("TeamToggle")
        self.MapToggles.addWidget(self.TeamToggle)
        self.Compass = QtWidgets.QGraphicsView(parent=self.frame)
        self.Compass.setGeometry(QtCore.QRect(790, 10, 25, 25))
        self.Compass.setMaximumSize(QtCore.QSize(25, 25))
        self.Compass.setObjectName("Compass")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1148, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.LegendTitle.setText(_translate("MainWindow", "Legend"))
        self.VictimLegendItemLabel.setText(_translate("MainWindow", "Potential Victim"))
        self.RescuedVictimLegendItemLabel.setText(_translate("MainWindow", "Rescued Victim"))
        self.ModuleLegendItemLabel.setText(_translate("MainWindow", "Module"))
        self.TMLegendItemLabel.setText(_translate("MainWindow", "Team Member"))
        self.UserLegendItemLabel.setText(_translate("MainWindow", "You"))
        self.PastVictimsToggle.setText(_translate("MainWindow", "Past Victims"))
        self.ModulesToggle.setText(_translate("MainWindow", "Modules"))
        self.TeamToggle.setText(_translate("MainWindow", "Team"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
