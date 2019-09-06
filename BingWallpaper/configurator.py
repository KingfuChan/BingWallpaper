# pylint: disable=E0611

import os
import sys
from os import path

import winshell
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from dialog import Ui_Dialog
from directories import icon_dir
from win32api import ShellExecute


class MyWindow(QMainWindow, Ui_Dialog):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        # set and lock window size
        mySize = (self.gridLayoutWidget.width(),
                  self.gridLayoutWidget.height())
        self.resize(*mySize)
        self.setMaximumSize(*mySize)
        self.setMinimumSize(*mySize)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(icon_dir()),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        # initialize tooltip of checkbox_1
        self.tooltip_temp = self.checkBox_1.toolTip()
        self.Update_toolTip()

    def OK_buttonClick(self):
        settings = [
            self.spinBox_1.value() if self.checkBox_1.isChecked() else 0,
            self.spinBox_2.value() if self.checkBox_2.isChecked() else 0,
            self.spinBox_3.value() if self.checkBox_3.isChecked() else 0,
            self.spinBox_4.value(),
        ]
        settings = [str(s) for s in settings]

        # generate link in startup
        directory = path.dirname(sys.argv[0])
        target = path.join(directory, "BingWallpaper.exe")
        arguments = ' '.join(settings)
        winshell.CreateShortcut(
            Path=path.join(winshell.startup(), "BingWallpaper.lnk"),
            Target=target,
            Arguments=arguments,
            StartIn=directory,)

        # messagebox question, ask to download
        ans = QMessageBox.question(
            self, "创建配置", "成功配置开机启动！\n是否立即执行程序？", QMessageBox.Ok | QMessageBox.Cancel)
        if ans == QMessageBox.Ok:
            ShellExecute(0, 'open', target, arguments, directory, 1)
            self.close()

    def Reset_buttonClick(self):
        # reset checkbox status
        self.checkBox_1.setChecked(False)
        self.checkBox_2.setChecked(False)
        self.checkBox_3.setChecked(False)

        # reset spin box default numbers
        self.spinBox_1.setValue(14)
        self.spinBox_2.setValue(5)
        self.spinBox_3.setValue(3)
        self.spinBox_4.setValue(15)

    def Delete_buttonClick(self):
        try:
            os.remove(path.join(winshell.startup(), "BingWallpaper.lnk"))
            info = "开机启动配置已删除！"
        except FileNotFoundError:
            info = "未配置开机启动！"
        # messagebox information
        QMessageBox.information(self, "删除配置", info)

    def Exit_buttonClick(self):
        self.close()

    def Sync_Retry_3(self):
        # synchronize checkbox 3 and 4
        self.checkBox_4.setChecked(self.checkBox_3.isChecked())

    def Sync_Retry_4(self):
        # synchronize checkbox 3 and 4
        self.checkBox_3.setChecked(self.checkBox_4.isChecked())

    def Update_toolTip(self):
        # upadate the tooltip of checkBox 1
        n = self.spinBox_1.value()
        if n > 15:
            n = 15
        tooltip = self.tooltip_temp.replace('?n?', str(n))
        self.checkBox_1.setToolTip(tooltip)


def execute(argv):
    app = QApplication(argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    execute(sys.argv)
