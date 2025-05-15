from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
import math as math
import sys
import time
import libximc.highlevel as ximc

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('irisInterface.ui', self)
        self.axis = ximc.Axis('xi-com:\\\\.\\COM3')
        self.axis.open_device()
        self.status = self.axis.get_status()
        limits = self.axis.get_edges_settings()
        print("Status.Ipwr: {}".format(self.status.Ipwr))
        print("Status.Upwr: {}".format(self.status.Upwr))
        print("Status.Iusb: {}".format(self.status.Iusb))
        print("Status.Flags: {}".format(self.status.Flags))
        print("Status.Flags: {}".format(limits))
        self.findLimit()


    def findLimit(self):
        start_time = time.time()
        self.axis.command_left()
        while True:
            if time.time() - start_time > 10:
                self.axis.command_stop()
                print("limit switch not found... Investigate manually and try again\n Quitting...")
                time.sleep(3)
                sys.exit()
            self.status = self.axis.get_status()
            print("Finding limit switch")
            if int(self.status.GPIOFlags) == 18:
                self.axis.command_stop()
                print("GPIOFlags.STATE_LEFT_EDGE reached.")
                break
            time.sleep(0.1)
        self.left_edge = self.axis.get_position()
        self.left_edge = self.left_edge.Position + self.left_edge.uPosition/256
        print("Left Edge Limit: {} steps".format(self.left_edge))


    def closeEvent(self, event):
        self.axis.close_device()

    def set_100_button(self):
        print("\nGoing to 100%")
        req = math.modf(self.left_edge)
        [pos, upos] = [int(req[1]), int(req[0]*256)]
        print("Position: {0} steps, {1} microsteps".format(pos, upos))
        self.axis.command_move(pos, upos)


    def set_75_button(self):
        print("\nGoing to 75%")
        req = math.modf(self.left_edge*75)
        [pos, upos] = [int(req[1]), int(req[0]*256)]
        print("Position: {0} steps, {1} microsteps".format(pos, upos))
        self.axis.command_move(pos, upos)

    def set_50_button(self):
        print("\nGoing to 50%")
        req = math.modf(self.left_edge*50)
        [pos, upos] = [int(req[1]), int(req[0]*256)]
        print("Position: {0} steps, {1} microsteps".format(pos, upos))
        self.axis.command_move(pos, upos)

    def set_25_button(self):
        print("\nGoing to 25%")
        req = math.modf(self.left_edge*25)
        [pos, upos] = [int(req[1]), int(req[0]*256)]
        print("Position: {0} steps, {1} microsteps".format(pos, upos))
        self.axis.command_move(pos, upos)

    def set_10_button(self):
        print("\nGoing to 10%")
        req = math.modf(self.left_edge*10)
        [pos, upos] = [int(req[1]), int(req[0]*256)]
        print("Position: {0} steps, {1} microsteps".format(pos, upos))
        self.axis.command_move(pos, upos)

    def set_5_button(self):
        print("\nGoing to 5%")
        req = math.modf(self.left_edge*5)
        [pos, upos] = [int(req[1]), int(req[0]*256)]
        print("Position: {0} steps, {1} microsteps".format(pos, upos))
        self.axis.command_move(pos, upos)


    def set_position_button(self):
        sbx = self.spinBox.value()
        req = math.modf(self.left_edge*sbx)
        [pos, upos] = [int(req[1]), int(req[0]*256)] 
        self.axis.command_move(pos, upos)
        res="Position: {0} steps, {1} microsteps".format(pos, upos)
        res2="Percent Open: {}%".format(sbx)
        print(res + '\n' + res2)

    def print_position_button(self):
        pos = self.axis.get_position()
        res="Position: {0} steps, {1} microsteps".format(pos.Position, pos.uPosition)
        res2="Percent Open: {}%".format(round(1-(pos.Position - self.left_edge)/self.left_edge)*100)
        print(res2 + '\n' + res)
        self.plainTextEdit.setPlainText(res2 + '\n' + res)


if  __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
