#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys, subprocess
from PyQt5 import QtGui, QtWidgets
from PyQt5 import QtCore, QtWidgets

####################################################################
class PPTGUI(QtWidgets.QWidget):


    def __init__(self):
        super(PPTGUI, self).__init__()
        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 900, 580))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tabWidget.addTab(self.tab_4, "")
        self.initUI()
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtCore.QCoreApplication.translate("MainWindow", "1. Run Bundler", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtCore.QCoreApplication.translate("MainWindow", "2. Run CMVS/PMVS", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtCore.QCoreApplication.translate("MainWindow", "or run PMVS without CMVS", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QtCore.QCoreApplication.translate("MainWindow", "Check Camera Database", None))
    def initUI(self):
####################################################################

#BUNDLER
# button 1 for pictures directory
        self.button1 = QtWidgets.QPushButton('Select Photos Path', self.tab)
        self.button1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button1.move(20, 30)
        self.button1.clicked.connect(self.showDialog1)
        self.setFocus()

# directory path label
        self.label9 = QtWidgets.QLabel('path:', self.tab)
        self.label9.move(190, 34)

        self.text4 = QtWidgets.QLineEdit(self.tab)
        self.text4.move(235, 30)
        self.text4.resize(550, 27)

# help button select directory
        self.help_button1 = QtWidgets.QPushButton("", self.tab)
        self.help_button1.setIcon(QtGui.QIcon('icons/info_icon.png'))
        self.help_button1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.help_button1.move(800, 26)
        self.help_button1.clicked.connect(self.on_help1_clicked)
        self.setFocus()

# features extractor combo
        self.label16 = QtWidgets.QLabel('Select Feature Extractor:', self.tab)
        self.label16.move(20, 84)

        self.text15 = QtWidgets.QLineEdit("siftvlfeat", self.tab)
        self.text15.setReadOnly(True)
        self.combo = QtWidgets.QComboBox(self.tab)
        self.combo.addItem("siftvlfeat")
        self.combo.addItem("siftlowe")
        self.combo.move(200, 80)
        self.text15.move(360, 100)
        self.text15.resize(0, 0)

        self.combo.activated['QString'].connect(self.onActivated)

# help button features extractor
        self.help_button2 = QtWidgets.QPushButton("", self.tab)
        self.help_button2.setIcon(QtGui.QIcon('icons/info_icon.png'))
        self.help_button2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.help_button2.move(300, 76)
        self.help_button2.clicked.connect(self.on_help2_clicked)
        self.setFocus()

# image width

        self.cb1 = QtWidgets.QCheckBox('Set desired Photos Width:', self.tab)
        self.cb1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.cb1.move(380, 80)
        self.cb1.toggle()
        self.cb1.stateChanged[int].connect(self.changesize1)

        self.text13 = QtWidgets.QLineEdit('1200', self.tab)
        self.text13.move(600, 78)
        self.text13.resize(70, 27)

# help button width
        self.help_button3 = QtWidgets.QPushButton("", self.tab)
        self.help_button3.setIcon(QtGui.QIcon('icons/info_icon.png'))
        self.help_button3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.help_button3.move(720, 76)
        self.help_button3.clicked.connect(self.on_help3_clicked)
        self.setFocus()

# image resize
        self.cb2 = QtWidgets.QCheckBox('Scale Photos with a Scaling Factor', self.tab)
        self.cb2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.cb2.move(380, 130)
        self.cb2.toggle()
        self.cb2.setChecked(False)
        self.cb2.stateChanged[int].connect(self.changesize2)

        self.text11 = QtWidgets.QLineEdit("1", self.tab)
        self.text11.setReadOnly(True)
        self.combo2 = QtWidgets.QComboBox(self.tab)
        self.combo2.hide()
        self.combo2.addItem("1")
        self.combo2.addItem("0.75")
        self.combo2.addItem("0.5")
        self.combo2.addItem("0.25")
        self.combo2.move(650, 130)
        self.text11.move(390, 100)
        self.text11.resize(0, 0)

        self.combo2.activated['QString'].connect(self.onActivated2)

# help button resize
        self.help_button4 = QtWidgets.QPushButton("", self.tab)
        self.help_button4.setIcon(QtGui.QIcon('icons/info_icon.png'))
        self.help_button4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.help_button4.move(720, 126)
        self.help_button4.clicked.connect(self.on_help4_clicked)
        self.setFocus()

# button 4 for start bundler
        self.button4 = QtWidgets.QPushButton('Run', self.tab)
        self.button4.setIcon(QtGui.QIcon('icons/python_icon.png'))
        self.button4.move(20, 180)
        self.button4.clicked.connect(self.startbundler)

        self.text2 = QtWidgets.QLineEdit(self.tab)
        self.text2.move(120, 184)
        self.text2.setReadOnly(True)
        self.text2.resize(760, 27)

        self.text4.textChanged['QString'].connect(self.onChangedpathbundler)
        self.text15.textChanged['QString'].connect(self.onChangedextractor)
        self.text13.textChanged['QString'].connect(self.onChangedwidth)
        self.text11.textChanged['QString'].connect(self.onChangedsize)

#output

        self.line1 = QtWidgets.QFrame(self.tab)
        self.line1.setGeometry(QtCore.QRect(10, 220, 880, 20))
        self.line1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line1.setObjectName("line1")

        self.label20 = QtWidgets.QLabel('Output Bundler:', self.tab)
        self.label20.move(20, 240)

        self.output1 = QtWidgets.QTextBrowser(self.tab)
        self.output1.move(20, 264)
        self.output1.resize(850, 270)
        self.output1.setAcceptRichText(True)
        self.output1.setAutoFormatting(QtWidgets.QTextEdit.AutoBulletList)


# CMVS/PMVS
# button 2 for Bundler output directory

        self.button2 = QtWidgets.QPushButton('Select Bundler Output Path', self.tab_3)
        self.button2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button2.move(20, 30)
        self.button2.clicked.connect(self.showDialog2)
        self.setFocus()

# directory output path label
        self.label10 = QtWidgets.QLabel('path:', self.tab_3)
        self.label10.move(240, 34)

        self.text3 = QtWidgets.QLineEdit(self.tab_3)
        self.text3.move(285, 30)
        self.text3.resize(500, 27)

# help button 5 select bundler output directory
        self.help_button5 = QtWidgets.QPushButton("", self.tab_3)
        self.help_button5.setIcon(QtGui.QIcon('icons/info_icon.png'))
        self.help_button5.setFocusPolicy(QtCore.Qt.NoFocus)
        self.help_button5.move(800, 26)
        self.help_button5.clicked.connect(self.on_help5_clicked)
        self.setFocus()

# number images for cluster
        self.label11 = QtWidgets.QLabel('Number of Photos in each Cluster:', self.tab_3)
        self.label11.move(240, 84)

        self.text5 = QtWidgets.QLineEdit('10', self.tab_3)
        self.text5.move(490, 82)
        self.text5.resize(70, 27)

# help button 6 select bundler output directory
        self.help_button6 = QtWidgets.QPushButton("", self.tab_3)
        self.help_button6.setIcon(QtGui.QIcon('icons/info_icon.png'))
        self.help_button6.setFocusPolicy(QtCore.Qt.NoFocus)
        self.help_button6.move(580, 79)
        self.help_button6.clicked.connect(self.on_help6_clicked)
        self.setFocus()

# button run CMVS
        self.button5 = QtWidgets.QPushButton('Run', self.tab_3)
        self.button5.setIcon(QtGui.QIcon('icons/python_icon.png'))
        self.button5.move(20, 130)
        self.button5.clicked.connect(self.startcmvs)

        self.text6 = QtWidgets.QLineEdit(self.tab_3)
        self.text6.move(120, 134)
        self.text6.setReadOnly(True)
        self.text6.resize(760, 27)

        self.text3.textChanged['QString'].connect(self.onChangedpathcmvs)
        self.text5.textChanged['QString'].connect(self.onChangedcluster)

#output

        self.line3 = QtWidgets.QFrame(self.tab_3)
        self.line3.setGeometry(QtCore.QRect(10, 220, 880, 20))
        self.line3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line3.setObjectName("line3")

        self.label21 = QtWidgets.QLabel('Output CMVS/PMVS:', self.tab_3)
        self.label21.move(20, 240)

        self.output2 = QtWidgets.QTextBrowser(self.tab_3)
        self.output2.move(20, 264)
        self.output2.resize(850, 270)
        self.output2.setAcceptRichText(True)
        self.output2.setAutoFormatting(QtWidgets.QTextEdit.AutoBulletList)

# run only PMVS
        self.cb3 = QtWidgets.QCheckBox('Use directly PMVS2 (without CMVS):', self.tab_2)
        self.cb3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.cb3.move(20, 30)
        self.cb3.toggle()
        self.cb3.setChecked(False)
        self.cb3.stateChanged[int].connect(self.openpmvs)

# button 3 for output directory
        self.button3 = QtWidgets.QPushButton('Select Bundler Output Path', self.tab_2)
        self.button3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button3.move(20, 80)
        self.button3.hide()
        self.button3.clicked.connect(self.showDialog3)
        self.setFocus()

# directory output path label
        self.label14 = QtWidgets.QLabel('path:', self.tab_2)
        self.label14.move(240, 84)
        self.label14.hide()

        self.text7 = QtWidgets.QLineEdit(self.tab_2)
        self.text7.move(280, 80)
        self.text7.hide()
        self.text7.resize(500, 27)

# help button 7 select bundler output directory
        self.help_button7 = QtWidgets.QPushButton("", self.tab_2)
        self.help_button7.setIcon(QtGui.QIcon('icons/info_icon.png'))
        self.help_button7.setFocusPolicy(QtCore.Qt.NoFocus)
        self.help_button7.move(800, 76)
        self.help_button7.hide()
        self.help_button7.clicked.connect(self.on_help5_clicked)
        self.setFocus()

# run PMVS
        self.button6 = QtWidgets.QPushButton('Run', self.tab_2)
        self.button6.setIcon(QtGui.QIcon('icons/python_icon.png'))
        self.button6.move(20, 130)
        self.button6.hide()
        self.button6.clicked.connect(self.startpmvs)

        self.text8 = QtWidgets.QLineEdit(self.tab_2)
        self.text8.move(120, 134)
        self.text8.setReadOnly(True)
        self.text8.hide()
        self.text8.resize(760, 27)

        self.text7.textChanged['QString'].connect(self.onChangedpathpmvs)

#output

        self.line2 = QtWidgets.QFrame(self.tab_2)
        self.line2.setGeometry(QtCore.QRect(10, 220, 880, 20))
        self.line2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line2.setObjectName("line2")

        self.label22 = QtWidgets.QLabel('Output PMVS:', self.tab_2)
        self.label22.move(20, 240)

        self.output3 = QtWidgets.QTextBrowser(self.tab_2)
        self.output3.move(20, 264)
        self.output3.resize(850, 270)
        self.output3.setAcceptRichText(True)
        self.output3.setAutoFormatting(QtWidgets.QTextEdit.AutoBulletList)


# Set Camera Database

# button 1 for pictures directory
        self.button8 = QtWidgets.QPushButton('Select Photos Path', self.tab_4)
        self.button8.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button8.move(20, 30)
        self.button8.clicked.connect(self.showDialog4)
        self.setFocus()

# directory path label
        self.label12 = QtWidgets.QLabel('path:', self.tab_4)
        self.label12.move(190, 34)

        self.text9 = QtWidgets.QLineEdit(self.tab_4)
        self.text9.move(235, 30)
        self.text9.resize(550, 27)

# help button select directory
        self.help_button9 = QtWidgets.QPushButton("", self.tab_4)
        self.help_button9.setIcon(QtGui.QIcon('icons/info_icon.png'))
        self.help_button9.setFocusPolicy(QtCore.Qt.NoFocus)
        self.help_button9.move(800, 26)
        self.help_button9.clicked.connect(self.on_help9_clicked)
        self.setFocus()

# button run Camera Database
        self.button10 = QtWidgets.QPushButton('Run', self.tab_4)
        self.button10.setIcon(QtGui.QIcon('icons/python_icon.png'))
        self.button10.move(20, 80)
        self.button10.clicked.connect(self.startcamdat)

        self.text10 = QtWidgets.QLineEdit(self.tab_4)
        self.text10.move(120, 84)
        self.text10.setReadOnly(True)
        self.text10.resize(760, 27)

        self.text9.textChanged['QString'].connect(self.onChangedpathcamdat)

#output

        self.line4 = QtWidgets.QFrame(self.tab_4)
        self.line4.setGeometry(QtCore.QRect(10, 220, 880, 20))
        self.line4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line4.setObjectName("line1")

        self.label23 = QtWidgets.QLabel('Output Camera Database:', self.tab_4)
        self.label23.move(20, 240)

        self.output4 = QtWidgets.QTextBrowser(self.tab_4)
        self.output4.move(20, 264)
        self.output4.resize(850, 270)
        self.output4.setAcceptRichText(True)
        self.output4.setAutoFormatting(QtWidgets.QTextEdit.AutoBulletList)


####################################################################
        self.setWindowTitle('Python Photogrammetry Toolbox GUI v 0.1')
        self.setGeometry(300, 300, 900, 580)
        self.setWindowIcon(QtGui.QIcon('icons/python_icon.png'))
####################################################################

# select directory with photos
    def showDialog1(self):
        directoryname = QtWidgets.QFileDialog.getExistingDirectory(self, 'Open directory with photos', '/home')
        self.text4.setText(directoryname)

# combo vlfeat-sift
    def onActivated(self, text):
        self.text15.setText(text)

# combo size-image
    def onActivated2(self, text):
        self.text11.setText(text)

# width-size select
    def changesize1(self, value):
        if self.cb1.isChecked():
            self.combo2.hide()
            self.text13.show()
            self.cb2.setChecked(False)
            self.text2.setText("python ./RunBundler.py --photos=" + self.text4.displayText() + " --featureExtractor=" + self.text15.displayText()+ " --maxPhotoDimension=" + self.text13.displayText())

    def changesize2(self, text):
        if self.cb2.isChecked():
            self.combo2.show()
            self.text13.hide()
            self.cb1.setChecked(False)
            self.text2.setText("python ./RunBundler.py --photos=" + self.text4.displayText() + " --featureExtractor=" + self.text15.displayText()+ " --photoScalingFactor=" + self.text11.displayText())

# start bundler
    def startbundler(self):
        command = self.text2.displayText()
        proc = subprocess.Popen((str(command)), shell=True, stdout=subprocess.PIPE)
        output = proc.stdout.read()
        self.output1.append(str(output))

# help button 1 - select directory
    def on_help1_clicked(self):
        QtWidgets.QMessageBox.information(self, "Help!", "Select the directory with original photos. Pictures have to be in JPG file format.", QtWidgets.QMessageBox.Ok)

# help button 2 - feature extractor
    def on_help2_clicked(self):
        QtWidgets.QMessageBox.information(self, "Help!", "Select the feature extractore between VLFEAT and SIFT. \n\nVLFEAT (http://www.vlfeat.org/) is released under GPL v.2 license. \n\nSIFT (http://www.cs.ubc.ca/~lowe/keypoints/) is being made available for individual research use only.  Any commercial use or any redistribution of this software requires a license from the University of British Columbia. Before use SIFT download and copy the binary into the <software/sift-lowe> folder.", QtWidgets.QMessageBox.Ok)

# help button 3 - feature extractor
    def on_help3_clicked(self):
        QtWidgets.QMessageBox.information(self, "Help!", "Copy of a photo will be scaled down if either width or height exceeds the value insert in <maxPhotoDimension>. After scaling the maximum of width and height will be equal to the value insert in <maxPhotoDimension>. \n\nDefault value is 1200: an image of 3008x2000 px will be scale into a copy of 1200x798 px.", QtWidgets.QMessageBox.Ok)

# help button 4 - feature extractor
    def on_help4_clicked(self):
        QtWidgets.QMessageBox.information(self, "Help!", "Scale all photos to the specified scaling factor: \n\n1 = original size \n\n0.75 = 75% of the original size \n\n0.5 = half size \n\n0.25 = 25% of the original size.", QtWidgets.QMessageBox.Ok)

# connection path-command
    def onChangedpathbundler(self, text):
        if self.cb2.isChecked(): self.text2.setText("python ./RunBundler.py --photos=" + self.text4.displayText() + " --featureExtractor=" + self.text15.displayText()+ " --photoScalingFactor=" + self.text11.displayText())
        if self.cb1.isChecked(): self.text2.setText("python ./RunBundler.py --photos=" + self.text4.displayText() + " --featureExtractor=" + self.text15.displayText()+ " --maxPhotoDimension=" + self.text13.displayText())

# connection extractor-command
    def onChangedextractor(self, text):
        if self.cb2.isChecked(): self.text2.setText("python ./RunBundler.py --photos=" + self.text4.displayText() + " --featureExtractor=" + self.text15.displayText()+ " --photoScalingFactor=" + self.text11.displayText())
        if self.cb1.isChecked(): self.text2.setText("python ./RunBundler.py --photos=" + self.text4.displayText() + " --featureExtractor=" + self.text15.displayText()+ " --maxPhotoDimension=" + self.text13.displayText())

# connection width-command
    def onChangedwidth(self, text):
        self.cb2.setChecked(False)
        self.cb1.setChecked(True)
        self.text2.setText("python ./RunBundler.py --photos=" + self.text4.displayText() + " --featureExtractor=" + self.text15.displayText()+ " --maxPhotoDimension=" + self.text13.displayText())

# connection size-command
    def onChangedsize(self, text):
        self.cb1.setChecked(False)
        self.cb2.setChecked(True)
        self.text2.setText("python ./RunBundler.py --photos=" + self.text4.displayText() + " --featureExtractor=" + self.text15.displayText()+ " --photoScalingFactor=" + self.text11.displayText())

# select directory with photos
    def showDialog2(self):
        directoryname = QtWidgets.QFileDialog.getExistingDirectory(self, 'Open directory with Bundler output files', '/home')
        self.text3.setText(directoryname)

# help button 5 - select directory
    def on_help5_clicked(self):
        QtWidgets.QMessageBox.information(self, "Help!", "Select the Bundler output directory.", QtWidgets.QMessageBox.Ok)

# connection path-command
    def onChangedpathcmvs(self, text):
        self.text6.setText("python ./RunCMVS.py --bundlerOutputPath=" + self.text3.displayText() + " --ClusterToCompute=" + self.text5.displayText())

# connection number cluster
    def onChangedcluster(self, text):
        self.text6.setText("python ./RunCMVS.py --bundlerOutputPath=" + self.text3.displayText() + " --ClusterToCompute=" + self.text5.displayText())

# help button 6 - cluster
    def on_help6_clicked(self):
        QtWidgets.QMessageBox.information(self, "Help!", "Select the max number of photos for each cluster that CMVS should compute. Separated PLY output files will be created. \n\nDepends on the CPUs of your computer: if infinite loop occur, stop the process and try a different value. \n\nDefault value is 10: an image set with 28 photos will be compute in 3 separated clusters.", QtWidgets.QMessageBox.Ok)

# start cmvs
    def startcmvs(self):
        command = self.text6.displayText()
        proc = subprocess.Popen((str(command)), shell=True, stdout=subprocess.PIPE)
        output = proc.stdout.read()
        self.output2.append(str(output))

# open pmvs
    def openpmvs(self, text):
        if self.cb3.isChecked():
            self.button3.show()
            self.button6.show()
            self.text7.show()
            self.text8.show()
            self.label14.show()
            self.help_button7.show()
        else: self.label14.hide(), self.button3.hide(), self.button6.hide(), self.text7.hide(), self.text8.hide(), self.help_button7.hide()

# select directory with bundler output
    def showDialog3(self):
        directoryname = QtWidgets.QFileDialog.getExistingDirectory(self, 'Open directory with Bundler output files', '/home')
        self.text7.setText(directoryname)

# connection path-command
    def onChangedpathpmvs(self, text):
        self.text8.setText("python ./RunPMVS.py --bundlerOutputPath=" + self.text7.displayText())

# start pmvs
    def startpmvs(self):
        command = self.text8.displayText()
        proc = subprocess.Popen((str(command)), shell=True, stdout=subprocess.PIPE)
        output = proc.stdout.read()
        self.output3.append(str(output))

# select directory with photos (Camera Database)
    def showDialog4(self):
        directoryname = QtWidgets.QFileDialog.getExistingDirectory(self, 'Open directory with photos', '/home')
        self.text9.setText(directoryname)

# help button 9 - select directory
    def on_help9_clicked(self):
        QtWidgets.QMessageBox.information(self, "Help!", "Select the directory with original photos. Pictures have to be in JPG file format. \n\nPress the RUN button to check if the camera is inset inside the database. \n\nIf the camera is not correctly saved, please insert in the terminal windows the CCD width in mm", QtWidgets.QMessageBox.Ok)

# connection path-command
    def onChangedpathcamdat(self, text):
        self.text10.setText("python ./RunBundler.py --photos=" + self.text9.displayText() + " --checkCameraDatabase")

# start Camera Database
    def startcamdat(self):
        command = self.text10.displayText()
        proc = subprocess.Popen((str(command)), shell=True)

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    ppt = PPTGUI()
    ppt.show()
    app.exec_()
