#! /usr/bin/python
import os
import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from dcstats import dataIO
from dcstats.fieller import Fieller
import dcstats.rantest as rantest
from dcstats.basic_stats import TTestBinomial
from dcstats.Hedges import Hedges_d
from dcstats.basic_stats import TTestContinuous

__author__="remis"
__date__ ="$03-Jan-2010 15:26:00$"

class rantestQT(QDialog):
    def __init__(self, parent=None):
        super(rantestQT, self).__init__(parent)
        self.resize(400, 600)
        tab_widget = QTabWidget()
        tab1 = QWidget()
        tab1.setStyleSheet("QWidget { background-color: %s }"% "white")
        tab2 = QWidget()
        tab3 = QWidget()
        tab4 = QWidget()
        tab_widget.addTab(tab1, "Wellcome!")
        tab_widget.addTab(tab2, "Rantest: continuous")
        tab_widget.addTab(tab3, "Rantest: binary")
        tab_widget.addTab(tab4, "Fieller")

        self.nran = 5000
        self.paired = 0
        self.path = ""

        ####### Tabs ##########
        tab1_layout = QVBoxLayout(tab1)
        tab1_layout.addWidget(QLabel("<p align=center><b>Welcome to DC_PyPs: "
        "Statistics!</b></p>"))
        tab1_layout.addWidget(self.movie_screen())
        tab1_layout.addWidget(QLabel("<p align=center><b>To continue select a "
        "statistical test from visible tabs.</b></p>"))
        self.rancont_layout(QVBoxLayout(tab2))
        self.ranbin_layout(QVBoxLayout(tab3))
        self.fieller_layout(QVBoxLayout(tab4))

        ##### Finalise main window ######
        vbox = QVBoxLayout()
        vbox.addWidget(tab_widget)
        quitButton = QPushButton("&QUIT")
        quitButton.clicked.connect(self.close)
        vbox.addLayout(self.single_button(quitButton))
        self.setLayout(vbox)
        self.setWindowTitle("DC_PyPs: Statistics")

#######   TAB 4: FIELLER. START  #############
    def fieller_layout(self, tab_layout):
        'Prepare layout for Tab 4. Fieller theorema.'
        intro_fieller = ("FIELLER: calculates confidence limits for a ratio " +
            "according Fieller''s theorem." +
            "\nCalculates approximate SD of the ratio r=a/b, given " +
            "the SD of a (numerator) \nand of b (denominator), " +
            "and the correlation coefficient between a, b (zero if they are " +
            "independent). \n")
        tab_layout.addWidget(QLabel(intro_fieller))

        grid = QGridLayout()
        grid.addWidget(QLabel("Nominator:"), 0, 0)
        grid.addWidget(QLabel("SD of Nominator:"), 1, 0)
        grid.addWidget(QLabel("Denominator:"), 2, 0)
        grid.addWidget(QLabel("SD of Denominator:"), 3, 0)
        grid.addWidget(QLabel("Correlation coefficient (nom,denom):"), 4, 0)
        grid.addWidget(QLabel("Alpha:"), 5, 0)
        grid.addWidget(QLabel("Total number of observations (Na + Nb):"), 6, 0)
        self.tb4e1 = QLineEdit("14")
        grid.addWidget(self.tb4e1, 0, 1)
        self.tb4e2 = QLineEdit("3")
        grid.addWidget(self.tb4e2, 1, 1)
        self.tb4e3 = QLineEdit("7")
        grid.addWidget(self.tb4e3, 2, 1)
        self.tb4e4 = QLineEdit("2")
        grid.addWidget(self.tb4e4, 3, 1)
        self.tb4e5 = QLineEdit("0")
        grid.addWidget(self.tb4e5, 4, 1)
        self.tb4e6 = QLineEdit("0.05")
        grid.addWidget(self.tb4e6, 5, 1)
        self.tb4e7 = QLineEdit("12")
        grid.addWidget(self.tb4e7, 6, 1)
        tab_layout.addLayout(grid)

        self.tb4b1 = QPushButton("Calculate")
        tab_layout.addLayout(self.single_button(self.tb4b1))
        self.tb4txt = QTextBrowser()
        self.tb4txt.append("RESULT WILL BE DISPLAYED HERE")
        tab_layout.addWidget(self.tb4txt)
        self.tb4b1.clicked.connect(self.callback2)       
        return tab_layout

    def callback2(self):
        'Called by CALCULATE button in Tab4.'
        a = float(self.tb4e1.text())
        b = float(self.tb4e3.text())
        sa = float(self.tb4e2.text())
        sb = float(self.tb4e4.text())
        r = float(self.tb4e5.text())
        alpha = float(self.tb4e6.text())
        Ntot = float(self.tb4e7.text())
        self.tb4txt.clear()
#        log = PrintLog(self.tb4txt) #, sys.stdout)
        #Call Fieller to calculate statistics.
        flr = Fieller(a, b, sa, sb, r, alpha, Ntot)
        self.tb4txt.append(str(flr))
#######   TAB 4: FIELLER. END  #############

#######   TAB 3: RANTEST FOR BINARY DATA. START  #############
    def ranbin_layout(self, tab_layout):
        """ """
        tab_layout.addWidget(QLabel(rantest.RTINTROD))
        tab_layout.addWidget(QLabel("Sample 1"))
        layout1 = QHBoxLayout()
        layout1.addWidget(QLabel("Successes:"))
        self.tb3e1 = QLineEdit("3")
        layout1.addWidget(self.tb3e1)
        layout1.addWidget(QLabel("Failures:"))
        self.tb3e2 = QLineEdit("4")
        layout1.addWidget(self.tb3e2)
        layout1.addStretch()
        tab_layout.addLayout(layout1)

        tab_layout.addWidget(QLabel("Sample 2"))
        layout2 = QHBoxLayout()
        layout2.addWidget(QLabel("Successes:"))
        self.tb3e3 = QLineEdit("4")
        layout2.addWidget(self.tb3e3)
        layout2.addWidget(QLabel("Failures:"))
        self.tb3e4 = QLineEdit("5")
        layout2.addWidget(self.tb3e4)
        layout2.addStretch()
        tab_layout.addLayout(layout2)

        layout3 = QHBoxLayout()
        layout3.addWidget(QLabel("Number of randomisations:"))
        self.tb3e5 = QLineEdit("5000")
        layout3.addWidget(self.tb3e5)
        layout3.addStretch()
        tab_layout.addLayout(layout3)
        
        self.tb3b1 = QPushButton("Calculate")
        tab_layout.addLayout(self.single_button(self.tb3b1))
        self.tb3txt = QTextBrowser()
        self.tb3txt.append("RESULT WILL BE DISPLAYED HERE")
        tab_layout.addWidget(self.tb3txt)
        self.tb3b1.clicked.connect(self.callback3)

        return tab_layout

    def callback3(self):
        """Called by button CALCULATE."""
        ir1 = int(self.tb3e1.text())
        if1 = int(self.tb3e2.text())
        ir2 = int(self.tb3e3.text())
        if2 = int(self.tb3e4.text())
        self.nran = int(self.tb3e5.text())
        self.tb3txt.clear()
        
        ttb = TTestBinomial(ir1, if1, ir2, if2)
        rnt = rantest.RantestBinomial(ir1, if1, ir2, if2)
        rnt.run_rantest(self.nran)
        self.tb3txt.append(str(ttb))
        self.tb3txt.append(str(rnt))
        
#######   TAB 3: RANTEST FOR BINARY DATA. END  #############

#######   TAB 2: RANTEST FOR CONTINUOSLY VARIABLY DATA. START  #############
    def rancont_layout(self, tab_layout):
        """Create Tab2 layout."""
        tab_layout.addWidget(QLabel(rantest.RTINTROD))

        self.tb2b1 = QPushButton("Get data from Excel file")
        tab_layout.addLayout(self.single_button(self.tb2b1))
        layout1 = QHBoxLayout()
        layout1.addWidget(QLabel("Number of randomisations:"))
        self.tb2e5 = QLineEdit(str(self.nran))
        layout1.addWidget(self.tb2e5)
        self.tb2c1 = QCheckBox("&Paired test?")
        layout1.addWidget(self.tb2c1)
        tab_layout.addLayout(layout1)
        self.tb2b2 = QPushButton("Run test")
        tab_layout.addLayout(self.single_button(self.tb2b2))

        self.tb2txt = QTextBrowser()
        self.tb2txt.append("RESULT WILL BE DISPLAYED HERE")
        tab_layout.addWidget(self.tb2txt)
        self.tb2e5.editingFinished.connect(self.ran_changed)
        self.tb2c1.stateChanged.connect(self.ran_changed)
        self.tb2b1.clicked.connect(self.callback1)
        self.tb2b2.clicked.connect(self.callback4)
        return tab_layout

    def callback1(self):
        """Called by TAKE DATA FROM FILE button in Tab2"""
        try:
            self.filename, filt = QFileDialog.getOpenFileName(self,
                "Open Data File...", self.path, "MS Excel Files (*.xlsx)")
            self.path = os.path.split(str(self.filename))[0]
            #TODO: allow loading from other format files
            self.load_data_from_Excel()
        except:
            pass

    def load_data_from_Excel(self):
        #TODO: currently loads only firs two columns. Allow multiple column load.
        xl = pd.ExcelFile(self.filename)
        dialog = ExcelSheetDlg(xl.sheet_names, self)
        if dialog.exec_():
            xlssheet = dialog.returnSheet()
        dt = xl.parse(xlssheet)
        self.X = dt.iloc[:,0].dropna().values.tolist()
        self.Y = dt.iloc[:,1].dropna().values.tolist()
        self.get_basic_statistics()
       
    def get_basic_statistics(self):
        # Calculate and display basic statistics
        self.tb2txt.clear()
        self.tb2txt.append('Data loaded from a text file: ' + self.filename + '\n')
        ttc = TTestContinuous(self.X, self.Y, self.paired)
        self.tb2txt.append(str(ttc))
        #calculation of hedges d and approximate 95% confidence intervals
        #not tested against known values yet AP 170518
        hedges_calculation = Hedges_d(self.X, self.Y)
        hedges_calculation.hedges_d_unbiased()
        #lowerCI, upperCI = hedges_calculation.approx_CI(self.paired)
        #paired needed for degrees of freedom
        lowerCI, upperCI = hedges_calculation.bootstrap_CI(5000)
        #option to have bootstrap calculated CIs should go here
        self.tb2txt.append(str(hedges_calculation))
                
    def callback4(self):
        """Called by RUN TEST button in Tab2."""
        rnt = rantest.RantestContinuous(self.X, self.Y, self.paired)
        rnt.run_rantest(self.nran)
        self.tb2txt.append(str(rnt))

    def ran_changed(self):
        if self.tb2c1.isChecked():
            self.paired = 1
        else:
            self.paired = 0
        self.nran = int(self.tb2e5.text()) 
#######   TAB 2: RANTEST FOR CONTINUOSLY VARIABLY DATA. START  #############

    def single_button(self, bt):
        b_layout = QHBoxLayout()
        b_layout.addStretch()
        b_layout.addWidget(bt)
        b_layout.addStretch()
        return b_layout

#######   TAB 1: WELCOME!  START   ############
    def movie_screen(self):
        """Set up the gif movie screen."""
        movie_screen = QLabel()
        # expand and center the label
        movie_screen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        movie_screen.setAlignment(Qt.AlignCenter)
        movie = QMovie("GUI/dca2.gif", QByteArray(), self)
        movie.setCacheMode(QMovie.CacheAll)
        movie.setSpeed(100)
        movie_screen.setMovie(movie)
        movie.start()
        return movie_screen
#######   TAB 1: WELCOME!  END   ############


class ExcelSheetDlg(QDialog):
    """
    Dialog to choose Excel sheet to load.
    """
    def __init__(self, sheetlist, parent=None):
        super(ExcelSheetDlg, self).__init__(parent)
        self.sheet = ''
        self.List = QListWidget()
        self.List.addItems(sheetlist)
        self.List.itemSelectionChanged.connect(self.sheetSelected)
        layout1 = QHBoxLayout()
        layout1.addWidget(self.List)
        layout2 = QVBoxLayout()
        layout2.addLayout(layout1)
        layout2.addWidget(ok_cancel_button(self))
        self.setLayout(layout2)
        self.resize(200, 300)
        self.setWindowTitle("Choose Excel sheet to load...")

    def sheetSelected(self):
        """
        Get selected sheet name.
        """
        self.sheet = self.List.currentRow()

    def returnSheet(self):
        """
        Return selected sheet name.
        """
        return self.sheet

def ok_cancel_button(parent):
    buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
    buttonBox.button(QDialogButtonBox.Ok).setDefault(True)
    buttonBox.accepted.connect(parent.accept)
    buttonBox.rejected.connect(parent.reject)
    # Following is for pyqt4
    #self.connect(buttonBox, SIGNAL("accepted()"),
    #     self, SLOT("accept()"))
    #self.connect(buttonBox, SIGNAL("rejected()"),
    #     self, SLOT("reject()"))
    return buttonBox