import sys
from PyQt4 import QtCore, QtGui,Qt
from qplayer_ui import * 
from res_rc import *
from connection import *

class Player(QtGui.QMainWindow):
	def __init__(self,parent=None):
		QtGui.QWidget.__init__(self,parent)
		self.ui=Ui_MainWindow()
		self.ui.setupUi(self)
		self.mute=False

		#stworzenie watku
		self.connection=Connection(self)
		#podlaczenie sygnalu z watku do funkcji
		QtCore.QObject.connect(self.connection,QtCore.SIGNAL("get_status()"), self.loadData)
		#tu bedzie wiecej podlaczen... zapewne
		#odpalenie watku
		self.connection.run()
		
		
	def loadData(self):
		'''funkcja do ladowania informacji na starcie programu'''
		#pobranie statusu i ustawienie ikonki
		status=str(self.connection.status['state'])

		icon=QtGui.QIcon()
		if  status== 'pause' or status== 'stop':
			icon.addPixmap(QtGui.QPixmap(":/icons/media-playback-start.png"))
			self.play=False

		else:
			icon.addPixmap(QtGui.QPixmap(":/icons/media-playback-pause.png"))
			self.play=True
		self.ui.playBtn.setIcon(icon)

		#pobranie volume... TODO: ustawienie vol w mpd podzielnego przez 5
		vol=int(self.connection.status['volume'])//5
		#pobranie nazwy artysty
		song=str(self.connection.client.currentsong()['artist'])+"-"+str(self.connection.client.currentsong()['title'])
		#ustawienie statusbara
		self.status=StatusInfo(self.ui.statusbar,song,"",str(self.ui.volSlider.value()*5),status.capitalize())
		#ustawienie slidera z volume (wczesniej sie nie da przez klase StatusInfo
		self.ui.volSlider.setValue(vol)

	@QtCore.pyqtSlot()
	def on_playBtn_clicked(self):
		icon=QtGui.QIcon()
		if self.play:
			icon.addPixmap(QtGui.QPixmap(":/icons/media-playback-start.png"))
			self.play=False
			self.status.setPlaying("Paused")
			self.connection.client.pause()
		else:
			icon.addPixmap(QtGui.QPixmap(":/icons/media-playback-pause.png"))
			self.play=True
			self.status.setPlaying("Playing")
			self.connection.client.play()
		self.ui.playBtn.setIcon(icon)
	@QtCore.pyqtSlot()
	def on_nextBtn_clicked(self):
		self.connection.client.next()
	@QtCore.pyqtSlot()
	def on_prevBtn_clicked(self):
		self.connection.client.previous()
	def on_stopBtn_clicked(self):
		self.connection.client.stop()
		icon=QtGui.QIcon()
		if self.play:
			icon.addPixmap(QtGui.QPixmap(":/icons/media-playback-start.png"))
			self.play=False
			self.ui.playBtn.setIcon(icon)
		self.status.setPlaying("Stopped")

	@QtCore.pyqtSlot()
	def on_volImg_clicked(self):
		icon=QtGui.QIcon()
		if self.mute:
			self.getVolIcon()
			self.mute=False
		else:
			icon.addPixmap(QtGui.QPixmap(":/icons/audio-volume-muted.png"))
			self.mute=True
			self.ui.volImg.setIcon(icon)
	def on_volSlider_valueChanged(self,a):
		if not self.mute: self.getVolIcon()
		volume=str(self.ui.volSlider.value()*5)
		self.ui.volSlider.setToolTip("Volume:"+volume)
		self.status.setVolume(volume)
		
	def getVolIcon(self):
		icon=QtGui.QIcon()
		val=self.ui.volSlider.value()
		if val>15: vol="high"
		elif val<=15 and val>5: vol="medium"
		elif val<=5 and val>1: vol="low"
		else: vol="muted"
		icon.addPixmap(QtGui.QPixmap(":/icons/audio-volume-"+vol+".png"))
		self.ui.volImg.setIcon(icon)

class StatusInfo(object):
	
	def __init__(self,statusbar,track,time,volume,playing):
		self.statusbar=statusbar
		self.track=track
		self.time=time
		self.volume=volume
		self.playing=playing
		self.setStatus()
	def setStatus(self):
		status=self.playing+" || "+self.track+" || "+self.time+" || "+self.volume+"%"
		self.statusbar.showMessage(status)
		

	def setTime(self,x):
		self.time=x
		self.setStatus()
	def setVolume(self,x):
		self.volume=x
		self.setStatus()		
	def setTrack(self,x):
		self.track=x
		self.setStatus()
	def setPlaying(self,x):
		self.playing=x
		self.setStatus()
if __name__=="__main__":
	app= QtGui.QApplication(sys.argv)
	myapp = Player()
	myapp.show()
	sys.exit(app.exec_())
