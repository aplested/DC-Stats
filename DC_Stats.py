#! /usr/bin/env python
"""
Launch rantest GUI: PyQt5 or Tk.
"""

import sys

if __name__ == "__main__":
    
    print ("Using Python version ", sys.version)
    try:
        from PyQt5 import QtGui #import *
        print ("Imported Pyqt5 QtGui")
        from PyQt5.QtWidgets import QApplication
        print ("Imported Pyqt5 QtWidgets QApplication")
        from GUI import QTrantest
        print ("Imported DC-Stats GUI")
        app = QApplication(sys.argv)
        form = QTrantest.RantestQT()
        form.show()
        app.exec_()
        
    except:
        if sys.version_info[0] < 3:
            from Tkinter import *
        else:
            from tkinter import *    
        from GUI.DC_Stats_Tk import *
        # initiate main frame
        master = Tk()
        app = DCP(master)
        master.mainloop()
    


    
