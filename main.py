from CLIENT import *
from SERVER import *
from threading import Thread
import time
import gui
import sys
import os
from PyQt5 import *
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
output_file = ""
buf_size = 10240
frame_size = 0

class MainApp(QtWidgets.QMainWindow, gui.Ui_model):
    inputFile_ = ""
    outputFile_ = ""
    frameSize_ = 0
    errorProbability_ = 0

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.inputFile.clicked.connect(self.openInputFileDialog)
        self.outputFile.clicked.connect(self.openOutputFileDialog)
        self.startButton.clicked.connect(self.startTransmission)
        self.resetButton.clicked.connect(self.resetProgram)

    def resetProgram(self):
        self.inputFile_ = ""
        self.outputFile_ = ""
        self.frameSize_ = 0
        self.errorProbability_ = 0
        self.inputFile.setStyleSheet("background-color: rgb(255, 245, 219);\n"
"font: 87 10pt \"Segoe UI Black\"")
        self.outputFile.setStyleSheet("background-color: rgb(255, 245, 219);\n"
"font: 87 10pt \"Segoe UI Black\"")
        self.errorProbability.setValue(0)
        self.frameSize.setValue(0)
        self.repeatCount.setText("")
        self.finalSpeed.setText("")
        self.gotBlocks.setText("")
        self.errorBlocks.setText("")
        self.errorCoeff.setText("")
        self.trasmissionTime.setText("")


    def startTransmission(self):
        if int(self.errorProbability.value()) > 100:
            QMessageBox.about(self, "Ошибка", "Вероятность ошибки не может быть больше 100%")
            return
        if int(self.errorProbability.value()) > 100:
            QMessageBox.about(self, "Ошибка", "Вероятность ошибки не может быть больше 100%")
            return
        if int(self.frameSize.value()) == 0:
            QMessageBox.about(self, "Ошибка", "Размер блока не может быть равен нулю")
            return
        if self.inputFile_ == "":
            QMessageBox.about(self, "Ошибка", "Не выбран файл-источник (ИС)")
            return
        if self.outputFile_ == "":
            QMessageBox.about(self, "Ошибка", "Не выбран файл-приёмник (ПС)")
            return


        self.frameSize_ = int(self.frameSize.value())
        self.errorProbability_ = int(self.errorProbability.value())

        th = Thread(target = self.server)
        th.start()
        newclient = Client(ipadd="127.0.0.1", portn=3241, error_probability=self.errorProbability_, frame_size=self.frameSize_, buffer_size=10240)
        start_time = time.time()
        newclient.send_file(filename=self.inputFile_)
        send_time = time.time() - start_time
        self.trasmissionTime.setText(str(round(send_time, 4)))
        errorCount = 0
        frameCount = 0
        with open("results", 'r') as f:
            errorCount = int(f.readline())
            frameCount = int(f.readline())
        os.system("del results")
        self.repeatCount.setText(str(errorCount))
        self.finalSpeed.setText(str(round(frameCount * self.frameSize_ / send_time, 4)))
        self.gotBlocks.setText(str(frameCount))
        self.errorBlocks.setText(str(errorCount))
        self.errorCoeff.setText(str(round(errorCount / frameCount, 3)))
    
    def server(self):
        newServer = Server(ipaddr="127.0.0.1", portn=3241, frame_size=self.frameSize_, buffer_size=10240)
        newServer.receive_file(filepath=self.outputFile_, logpath="logfile.txt")

    def openInputFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","Text Files (*.txt)", options=options)
        self.inputFile_ = str(files[0])
        self.inputFile.setStyleSheet("background-color: rgb(0, 255, 255);\n"
"font: 87 10pt \"Segoe UI Black\"")
    
    def openOutputFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","Text Files (*.txt)", options=options)
        self.outputFile_ = str(fileName)
        self.outputFile.setStyleSheet("background-color: rgb(0, 255, 255);\n"
"font: 87 10pt \"Segoe UI Black\"")

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()
'''
error_probability = int(input("Вероятность ошибки в %: "))
input_file = input("Название входного файла: ")
output_file = input("Название выходного файла: ")
frame_size = int(input("Размер блока данных в байтах: "))


'''