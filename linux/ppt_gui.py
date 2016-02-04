#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys, subprocess
from PyQt4 import QtGui
from PyQt4 import QtCore

#################################################################### 
class PPTGUI(QtGui.QWidget):
  
    
    def __init__(self):
        super(PPTGUI, self).__init__()
	self.tabWidget = QtGui.QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 900, 580))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tabWidget.addTab(self.tab_4, "")
        self.initUI()
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("MainWindow", "1. Run Bundler", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("MainWindow", "2. Run CMVS/PMVS", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("MainWindow", "or run PMVS without CMVS", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QtGui.QApplication.translate("MainWindow", "Check Camera Database", None, QtGui.QApplication.UnicodeUTF8))
    def initUI(self):
#################################################################### 

#BUNDLER
# button 1 for pictures directory 
        self.button1 = QtGui.QPushButton('Select Photos Path', self.tab)
        self.button1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button1.move(20, 30)
        self.connect(self.button1, QtCore.SIGNAL('clicked()'), self.showDialog1)
        self.setFocus()

# directory path label
        self.label9 = QtGui.QLabel('path:', self.tab)
        self.label9.move(190, 34)

        self.text4 = QtGui.QLineEdit(self.tab)
        self.text4.move(235, 30)
        self.text4.resize(550, 27)

# help button select directory
	self.help_button1 = QtGui.QPushButton("", self.tab)
	self.help_button1.setIcon(QtGui.QIcon('icons/info_icon.png'))
        self.help_button1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.help_button1.move(800, 26)
        self.connect(self.help_button1, QtCore.SIGNAL('clicked()'), self.on_help1_clicked)
        self.setFocus()

# features extractor combo
        self.label16 = QtGui.QLabel('Select Feature Extractor:', self.tab)
        self.label16.move(20, 84)

        self.text15 = QtGui.QLineEdit("siftvlfeat", self.tab)
	self.text15.setReadOnly(True)
        self.combo = QtGui.QComboBox(self.tab)
        self.combo.addItem("siftvlfeat")
        self.combo.addItem("siftlowe")
        self.combo.move(200, 80)
        self.text15.move(360, 100)
        self.text15.resize(0, 0)

        self.connect(self.combo, QtCore.SIGNAL('activated(QString)'), self.onActivated)

# help button features extractor
	self.help_button2 = QtGui.QPushButton("", self.tab)
	self.help_button2.setIcon(QtGui.QIcon('icons/info_icon.png'))
        self.help_button2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.help_button2.move(300, 76)
        self.connect(self.help_button2, QtCore.SIGNAL('clicked()'), self.on_help2_clicked)
        self.setFocus()

# image width

        self.cb1 = QtGui.QCheckBox('Set desired Photos Width:', self.tab)
        self.cb1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.cb1.move(380, 80)
        self.cb1.toggle()
        self.connect(self.cb1, QtCore.SIGNAL('stateChanged(int)'), self.changesize1)

        self.text13 = QtGui.QLineEdit('1200', self.tab)
        self.text13.move(600, 78)
        self.text13.resize(70, 27)

# help button width
	self.help_button3 = QtGui.QPushButton("", self.tab)
	self.help_button3.setIcon(QtGui.QIcon('icons/info_icon.png'))
        self.help_button3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.help_button3.move(720, 76)
        self.connect(self.help_button3, QtCore.SIGNAL('clicked()'), self.on_help3_clicked)
        self.setFocus()

# image resize
        self.cb2 = QtGui.QCheckBox('Scale Photos with a Scaling Factor', self.tab)
        self.cb2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.cb2.move(380, 130)
        self.cb2.toggle()
	self.cb2.setChecked(False)
        self.connect(self.cb2, QtCore.SIGNAL('stateChanged(int)'), self.changesize2)

        self.text11 = QtGui.QLineEdit("1", self.tab)
	self.text11.setReadOnly(True)
        self.combo2 = QtGui.QComboBox(self.tab)
	self.combo2.hide()
        self.combo2.addItem("1")
        self.combo2.addItem("0.75")
        self.combo2.addItem("0.5")
        self.combo2.addItem("0.25")
        self.combo2.move(650, 130)
        self.text11.move(390, 100)
        self.text11.resize(0, 0)

        self.connect(self.combo2, QtCore.SIGNAL('activated(QString)'), self.onActivated2)

# help button resize
	self.help_button4 = QtGui.QPushButton("", self.tab)
	self.help_button4.setIcon(QtGui.QIcon('icons/info_icon.png'))
        self.help_button4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.help_button4.move(720, 126)
        self.connect(self.help_button4, QtCore.SIGNAL('clicked()'), self.on_help4_clicked)
        self.setFocus()

# button 4 for start bundler 
        self.button4 = QtGui.QPushButton('Run', self.tab)
	self.button4.setIcon(QtGui.QIcon('icons/python_icon.png'))
        self.button4.move(20, 180)
        self.connect(self.button4, QtCore.SIGNAL('clicked()'), self.startbundler)

        self.text2 = QtGui.QLineEdit(self.tab)
	self.text2.move(120, 184)
	self.text2.setReadOnly(True)
        self.text2.resize(760, 27)

	self.connect(self.text4, QtCore.SIGNAL('textChanged(QString)'), self.onChangedpathbundler)
	self.connect(self.text15, QtCore.SIGNAL('textChanged(QString)'), self.onChangedextractor)
 	self.connect(self.text13, QtCore.SIGNAL('textChanged(QString)'), self.onChangedwidth)    
	self.connect(self.text11, QtCore.SIGNAL('textChanged(QString)'), self.onChangedsize)

#output

        self.line1 = QtGui.QFrame(self.tab)
        self.line1.setGeometry(QtCore.QRect(10, 220, 880, 20))
        self.line1.setFrameShape(QtGui.QFrame.HLine)
        self.line1.setFrameShadow(QtGui.QFrame.Sunken)
        self.line1.setObjectName("line1")

        self.label20 = QtGui.QLabel('Output Bundler:', self.tab)
        self.label20.move(20, 240)

	self.output1 = QtGui.QTextBrowser(self.tab)
        self.output1.move(20, 264)
        self.output1.resize(850, 270)
        self.output1.setAcceptRichText(True)
        self.output1.setAutoFormatting(QtGui.QTextEdit.AutoBulletList)


# CMVS/PMVS     
# button 2 for Bundler output directory
        
        self.button2 = QtGui.QPushButton('Select Bundler Output Path', self.tab_3)
        self.button2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button2.move(20, 30)
        self.connect(self.button2, QtCore.SIGNAL('clicked()'), self.showDialog2)
        self.setFocus()

# directory output path label
        self.label10 = QtGui.QLabel('path:', self.tab_3)
        self.label10.move(240, 34)

        self.text3 = QtGui.QLineEdit(self.tab_3)
        self.text3.move(285, 30)
        self.text3.resize(500, 27)

# help button 5 select bundler output directory
	self.help_button5 = QtGui.QPushButton("", self.tab_3)
	self.help_button5.setIcon(QtGui.QIcon('icons/info_icon.png'))
        self.help_button5.setFocusPolicy(QtCore.Qt.NoFocus)
        self.help_button5.move(800, 26)
        self.connect(self.help_button5, QtCore.SIGNAL('clicked()'), self.on_help5_clicked)
        self.setFocus()

# number images for cluster
        self.label11 = QtGui.QLabel('Number of Photos in each Cluster:', self.tab_3)
        self.label11.move(240, 84)

        self.text5 = QtGui.QLineEdit('10', self.tab_3)
        self.text5.move(490, 82)
        self.text5.resize(70, 27)

# help button 6 select bundler output directory
	self.help_button6 = QtGui.QPushButton("", self.tab_3)
	self.help_button6.setIcon(QtGui.QIcon('icons/info_icon.png'))
        self.help_button6.setFocusPolicy(QtCore.Qt.NoFocus)
        self.help_button6.move(580, 79)
        self.connect(self.help_button6, QtCore.SIGNAL('clicked()'), self.on_help6_clicked)
        self.setFocus()

# button run CMVS
        self.button5 = QtGui.QPushButton('Run', self.tab_3)
	self.button5.setIcon(QtGui.QIcon('icons/python_icon.png'))
        self.button5.move(20, 130)
        self.connect(self.button5, QtCore.SIGNAL('clicked()'), self.startcmvs)

        self.text6 = QtGui.QLineEdit(self.tab_3)
	self.text6.move(120, 134)
	self.text6.setReadOnly(True)
        self.text6.resize(760, 27)

	self.connect(self.text3, QtCore.SIGNAL('textChanged(QString)'), self.onChangedpathcmvs)
	self.connect(self.text5, QtCore.SIGNAL('textChanged(QString)'), self.onChangedcluster)

#output

        self.line3 = QtGui.QFrame(self.tab_3)
        self.line3.setGeometry(QtCore.QRect(10, 220, 880, 20))
        self.line3.setFrameShape(QtGui.QFrame.HLine)
        self.line3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line3.setObjectName("line3")

        self.label21 = QtGui.QLabel('Output CMVS/PMVS:', self.tab_3)
        self.label21.move(20, 240)

	self.output2 = QtGui.QTextBrowser(self.tab_3)
        self.output2.move(20, 264)
        self.output2.resize(850, 270)
        self.output2.setAcceptRichText(True)
        self.output2.setAutoFormatting(QtGui.QTextEdit.AutoBulletList)

# run only PMVS
        self.cb3 = QtGui.QCheckBox('Use directly PMVS2 (without CMVS):', self.tab_2)
        self.cb3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.cb3.move(20, 30)
        self.cb3.toggle()
	self.cb3.setChecked(False)
        self.connect(self.cb3, QtCore.SIGNAL('stateChanged(int)'), self.openpmvs)

# button 3 for output directory
        self.button3 = QtGui.QPushButton('Select Bundler Output Path', self.tab_2)
        self.button3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button3.move(20, 80)
	self.button3.hide()
        self.connect(self.button3, QtCore.SIGNAL('clicked()'), self.showDialog3)
        self.setFocus()

# directory output path label
        self.label14 = QtGui.QLabel('path:', self.tab_2)
        self.label14.move(240, 84)
	self.label14.hide()

        self.text7 = QtGui.QLineEdit(self.tab_2)
        self.text7.move(280, 80)
	self.text7.hide()
        self.text7.resize(500, 27)

# help button 7 select bundler output directory
	self.help_button7 = QtGui.QPushButton("", self.tab_2)
	self.help_button7.setIcon(QtGui.QIcon('icons/info_icon.png'))
        self.help_button7.setFocusPolicy(QtCore.Qt.NoFocus)
        self.help_button7.move(800, 76)
	self.help_button7.hide()
        self.connect(self.help_button7, QtCore.SIGNAL('clicked()'), self.on_help5_clicked)
        self.setFocus()

# run PMVS
        self.button6 = QtGui.QPushButton('Run', self.tab_2)
	self.button6.setIcon(QtGui.QIcon('icons/python_icon.png'))
        self.button6.move(20, 130)
	self.button6.hide()
        self.connect(self.button6, QtCore.SIGNAL('clicked()'), self.startpmvs)

        self.text8 = QtGui.QLineEdit(self.tab_2)
	self.text8.move(120, 134)
	self.text8.setReadOnly(True)
	self.text8.hide()
        self.text8.resize(760, 27)

	self.connect(self.text7, QtCore.SIGNAL('textChanged(QString)'), self.onChangedpathpmvs)

#output

        self.line2 = QtGui.QFrame(self.tab_2)
        self.line2.setGeometry(QtCore.QRect(10, 220, 880, 20))
        self.line2.setFrameShape(QtGui.QFrame.HLine)
        self.line2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line2.setObjectName("line2")

        self.label22 = QtGui.QLabel('Output PMVS:', self.tab_2)
        self.label22.move(20, 240)

	self.output3 = QtGui.QTextBrowser(self.tab_2)
        self.output3.move(20, 264)
        self.output3.resize(850, 270)
        self.output3.setAcceptRichText(True)
        self.output3.setAutoFormatting(QtGui.QTextEdit.AutoBulletList)
        

# Set Camera Database      
        
# button 1 for pictures directory 
        self.button8 = QtGui.QPushButton('Select Photos Path', self.tab_4)
        self.button8.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button8.move(20, 30)
        self.connect(self.button8, QtCore.SIGNAL('clicked()'), self.showDialog4)
        self.setFocus()

# directory path label
        self.label12 = QtGui.QLabel('path:', self.tab_4)
        self.label12.move(190, 34)

        self.text9 = QtGui.QLineEdit(self.tab_4)
        self.text9.move(235, 30)
        self.text9.resize(550, 27)

# help button select directory
	self.help_button9 = QtGui.QPushButton("", self.tab_4)
	self.help_button9.setIcon(QtGui.QIcon('icons/info_icon.png'))
        self.help_button9.setFocusPolicy(QtCore.Qt.NoFocus)
        self.help_button9.move(800, 26)
        self.connect(self.help_button9, QtCore.SIGNAL('clicked()'), self.on_help9_clicked)
        self.setFocus()
        
# button run Camera Database
        self.button10 = QtGui.QPushButton('Run', self.tab_4)
	self.button10.setIcon(QtGui.QIcon('icons/python_icon.png'))
        self.button10.move(20, 80)
        self.connect(self.button10, QtCore.SIGNAL('clicked()'), self.startcamdat)

        self.text10 = QtGui.QLineEdit(self.tab_4)
	self.text10.move(120, 84)
	self.text10.setReadOnly(True)
        self.text10.resize(760, 27)

	self.connect(self.text9, QtCore.SIGNAL('textChanged(QString)'), self.onChangedpathcamdat)
	
#output

        self.line4 = QtGui.QFrame(self.tab_4)
        self.line4.setGeometry(QtCore.QRect(10, 220, 880, 20))
        self.line4.setFrameShape(QtGui.QFrame.HLine)
        self.line4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line4.setObjectName("line1")

        self.label23 = QtGui.QLabel('Output Camera Database:', self.tab_4)
        self.label23.move(20, 240)

	self.output4 = QtGui.QTextBrowser(self.tab_4)
        self.output4.move(20, 264)
        self.output4.resize(850, 270)
        self.output4.setAcceptRichText(True)
        self.output4.setAutoFormatting(QtGui.QTextEdit.AutoBulletList)
	

####################################################################    
        self.setWindowTitle('Python Photogrammetry Toolbox GUI v 0.1')
        self.setGeometry(300, 300, 900, 580)
	self.setWindowIcon(QtGui.QIcon('icons/python_icon.png'))
####################################################################       

# select directory with photos
    def showDialog1(self):
	directoryname = QtGui.QFileDialog.getExistingDirectory(self, 'Open directory with photos', '/home')
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
		QtGui.QMessageBox.information(self, "Help!", "Select the directory with original photos. Pictures have to be in JPG file format.", QtGui.QMessageBox.Ok)

# help button 2 - feature extractor
    def on_help2_clicked(self):
		QtGui.QMessageBox.information(self, "Help!", "Select the feature extractore between VLFEAT and SIFT. \n\nVLFEAT (http://www.vlfeat.org/) is released under GPL v.2 license. \n\nSIFT (http://www.cs.ubc.ca/~lowe/keypoints/) is being made available for individual research use only.  Any commercial use or any redistribution of this software requires a license from the University of British Columbia. Before use SIFT download and copy the binary into the <software/sift-lowe> folder.", QtGui.QMessageBox.Ok)

# help button 3 - feature extractor
    def on_help3_clicked(self):
		QtGui.QMessageBox.information(self, "Help!", "Copy of a photo will be scaled down if either width or height exceeds the value insert in <maxPhotoDimension>. After scaling the maximum of width and height will be equal to the value insert in <maxPhotoDimension>. \n\nDefault value is 1200: an image of 3008x2000 px will be scale into a copy of 1200x798 px.", QtGui.QMessageBox.Ok)

# help button 4 - feature extractor
    def on_help4_clicked(self):
		QtGui.QMessageBox.information(self, "Help!", "Scale all photos to the specified scaling factor: \n\n1 = original size \n\n0.75 = 75% of the original size \n\n0.5 = half size \n\n0.25 = 25% of the original size.", QtGui.QMessageBox.Ok)

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
	directoryname = QtGui.QFileDialog.getExistingDirectory(self, 'Open directory with Bundler output files', '/home')
        self.text3.setText(directoryname)

# help button 5 - select directory
    def on_help5_clicked(self):
		QtGui.QMessageBox.information(self, "Help!", "Select the Bundler output directory.", QtGui.QMessageBox.Ok)

# connection path-command
    def onChangedpathcmvs(self, text):
	self.text6.setText("python ./RunCMVS.py --bundlerOutputPath=" + self.text3.displayText() + " --ClusterToCompute=" + self.text5.displayText())

# connection number cluster
    def onChangedcluster(self, text):
	self.text6.setText("python ./RunCMVS.py --bundlerOutputPath=" + self.text3.displayText() + " --ClusterToCompute=" + self.text5.displayText())

# help button 6 - cluster
    def on_help6_clicked(self):
		QtGui.QMessageBox.information(self, "Help!", "Select the max number of photos for each cluster that CMVS should compute. Separated PLY output files will be created. \n\nDepends on the CPUs of your computer: if infinite loop occur, stop the process and try a different value. \n\nDefault value is 10: an image set with 28 photos will be compute in 3 separated clusters.", QtGui.QMessageBox.Ok)
            
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
	directoryname = QtGui.QFileDialog.getExistingDirectory(self, 'Open directory with Bundler output files', '/home')
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
	directoryname = QtGui.QFileDialog.getExistingDirectory(self, 'Open directory with photos', '/home')
        self.text9.setText(directoryname)
        
# help button 9 - select directory
    def on_help9_clicked(self):
		QtGui.QMessageBox.information(self, "Help!", "Select the directory with original photos. Pictures have to be in JPG file format. \n\nPress the RUN button to check if the camera is inset inside the database. \n\nIf the camera is not correctly saved, please insert in the terminal windows the CCD width in mm", QtGui.QMessageBox.Ok)

# connection path-command
    def onChangedpathcamdat(self, text):
	self.text10.setText("python ./RunBundler.py --photos=" + self.text9.displayText() + " --checkCameraDatabase")

# start Camera Database
    def startcamdat(self):
	command = self.text10.displayText()
	proc = subprocess.Popen((str(command)), shell=True)

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    ppt = PPTGUI()
    ppt.show()
    app.exec_()
