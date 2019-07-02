'''
Created on May 23, 2019

@author: amin
'''

import sys
from PyQt5.QtWidgets import QApplication
from MainWidget import MainWidget


class Gui:
    def __init__(self):
        self.app = QApplication(sys.argv)

        widget = MainWidget()
        widget.resize(400, 600)
        widget.show()
        
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    gui = Gui()
