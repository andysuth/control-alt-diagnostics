from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
import math as math
import sys
import serial

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('example_v3.ui', self)
        self.serial = serial.Serial(port='COM3', baudrate=57600, timeout=3)

    def closeEvent(self, event):
        self.serial.close()

    def set_new_transmission_button(self):
        input = self.doubleSpinBox2.value()
        angle = round(0.5*(math.acos(-1.0*abs(math.sqrt((input-5.0)/95.0)))-0.3196)*180/math.pi,6)
        cmd = '1PA' + str(angle) + '\r\n'
        self.serial.write(cmd.encode())


    def set_new_angle_button(self):
        value = self.doubleSpinBox.value()     
        cmd = '1PA' + str(value) + '\r\n'
        self.serial.write(cmd.encode())

    def print_new_position_button(self):
        cmd = '1TP\r\n'
        self.serial.write(cmd.encode())
        data = self.serial.readline().decode().rstrip()[:11]
        value = float(data.split("P")[1])
        tm = 5+95*math.cos(0.3196 + 2*value*math.pi/180)**2
        print(data)
        res = data
        res2 = ('transmission '+ str(round(tm,2))+' %')
        print(res2)

        self.plainTextEdit.setPlainText(res + '\n' +  res2)

if  __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
