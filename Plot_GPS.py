import sys
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
QVBoxLayout, QSizePolicy)
import numpy as np

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.figure import Figure
import sys,time
import random
from PyQt5.QtCore import Qt
import rospy
from std_msgs.msg import String

class Window(QDialog):
	wav=[]
	xrow = []
	yrow = []
	lat = []
	lon = []
	ang = []
	cnt = 0
	first = True
	def __init__(self , parent=None):
		super(Window, self).__init__(parent)
		self.figure = plt.figure()

		self.canvas = FigureCanvas(self.figure)
		FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding,QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)
		self.button = QPushButton('Plot Way Points')
		self.TField1 = QTextEdit();
		#self.TField2 = QTextEdit();
		#self.TField3 = QLineEdit();
		self.navi_toolbar = NavigationToolbar(self.canvas, self)

		self.Wave1 = QLabel("Add WayPoints")
		self.Wave1.setAlignment=(Qt.AlignVCenter)
		self.Wave1.setIndent(20)
		self.Wave1.setFixedHeight(35)

		layout = QVBoxLayout()
		layout.setContentsMargins(0, 0, 0, 0)
		layout.addWidget(self.navi_toolbar)
		layout.addWidget(self.canvas)
		layout.addWidget(self.button)
		layout.addWidget(self.Wave1)

		layout.addWidget(self.TField1)

		self.setLayout(layout)
		self.ax = self.figure.add_subplot(111)
		self.button.clicked.connect(self.plotWave);

		rospy.init_node('receive_gps', anonymous=True)
		rospy.Subscriber("topic_gps", String, self.callback, queue_size=1)


	def callback(self, data):
		data = str(data)
		mydata = data.split(' ')
		x = float(mydata[1][1:])
		y = float(mydata[2])
		com = int(mydata[3][:-1])
		#print x,y,com
		if(self.cnt > 20):
			self.lat = []
			self.lon = []
			self.ang = []
			self.cnt=0
			for i in range(len(self.lat)):
				myMarker = mpl.markers.MarkerStyle(marker='$->$')
				myMarker._transform = myMarker.get_transform().rotate_deg(self.ang[i])
				self.ax.scatter(self.lat[i], self.lon[i], marker=myMarker, color = 'white', s=200)
				self.canvas.draw()
			
		else:
			if(self.first == True):
				myMarker = mpl.markers.MarkerStyle(marker='$->$')
				myMarker._transform = myMarker.get_transform().rotate_deg(com)
				self.curr_plot = self.ax.scatter(x, y, marker=myMarker, s=200, color='black')
				self.first = False
			else:
				myMarker = mpl.markers.MarkerStyle(marker='$->$')
				myMarker._transform = myMarker.get_transform().rotate_deg(com)
				self.curr_plot.set_color('red')
				self.curr_plot = self.ax.scatter(x, y, marker=myMarker, s=200, color='black')

			self.cnt+=1
			self.lat.append(x)
			self.lon.append(y)
			self.ang.append(com)
			self.canvas.draw()
		


	def plotWave(self):  
		try:
			self.Data = self.TField1.toPlainText()
			self.Data = self.Data.split('\n')
			
			lat = []
			lon = []

			for i in range(len(self.Data)):
				x,y = self.Data[i].split(',')
				x = float(x)
				y = float(y)
				lat.append(  float(x)  )
				lon.append(  float(y)  )
			
			self.ax.plot(lat, lon, zorder=1, lw=3, c='green')
			self.ax.scatter(lat, lon, s=120, zorder=2, c='yellow')
			for i in range(len(self.Data)):
				point = (lat[i], lon[i])
				self.ax.annotate('Waypoint ' + str(i),point)
			self.canvas.draw()
		except Exception as e:
			print e	
if __name__ == '__main__':
	app = QApplication(sys.argv)
	main = Window()
	main.show()
	sys.exit(app.exec_())
