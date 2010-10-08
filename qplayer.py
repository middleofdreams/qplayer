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
		self.ui.treeWidget.setColumnWidth(0,17)
		self.ui.treeWidget.setHeaderLabel("#")

		self.mute=False

		self.play=False
		self.plItem=None
		#stworzenie watku
		self.connection=Connection(self)
		self.pupd=ProgressUpdate(self)
		#podlaczenie sygnalu z watku do funkcji
		QtCore.QObject.connect(self.connection,QtCore.SIGNAL("get_status()"), self.loadData)
		QtCore.QObject.connect(self.pupd.timer,QtCore.SIGNAL("timeout()"), self.updateBar)
		QtCore.QObject.connect(self.connection,QtCore.SIGNAL("change_song()"), self.changeSong)

		#tu bedzie wiecej podlaczen... zapewne
		#odpalenie watku
		self.connection.start()
		self.pupd.start()
		
	def updateBar(self,force=False):
		if force:
			try:
				pr=str(self.connection.client.status()['time']).split(":")
				pr[1]
			except:
				#worst line ever?
				ti=self.connection.client.playlistinfo()[int(self.connection.client.status()['songid'])]
				pr=[0,ti['time']]
			self.ui.progressBar.setMaximum(int(pr[1]))
			self.ui.progressBar.setValue(int(pr[0]))
			self.ui.progressBar.setFormat(str(int(pr[0])//60).zfill(2)+":"+str(int(pr[0])%60).zfill(2))
			
		elif not force and self.play:
			#try:
				self.ui.progressBar.setValue(int(self.ui.progressBar.value())+1)
				t=self.ui.progressBar.text()
				m,s=str(t).split(":")
				m=int(m)
				s=int(s)
				if s==59:
					s=0
					m=m+1
				else:
					s=s+1
					
					
				self.ui.progressBar.setFormat(str(m).zfill(2)+":"+str(s).zfill(2))
			#except:
			#	pass

		
	
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
			self.pupd.timer.start()
		self.ui.playBtn.setIcon(icon)


		#pobranie nazwy artysty
		try:
			song=str(self.connection.client.currentsong()['artist'])+"-"+str(self.connection.client.currentsong()['title'])
		except: song=""
		self.status=StatusInfo(self.ui.statusbar,song,"",str(self.ui.volSlider.value()*5),status.capitalize())
		#pobranie volume... TODO: ustawienie vol w mpd podzielnego przez 5
		vol=int(self.connection.status['volume'])//5
		self.ui.volSlider.setValue(vol)
		self.getVolIcon()
		if self.play:
			self.updateBar(True)
		else:
			self.ui.progressBar.setMaximum(200)
			self.ui.progressBar.setValue(0)
			self.ui.progressBar.setFormat("00:00")
		#ladowanie playlisty:
		for track in self.connection.client.playlistinfo():
			item=QtGui.QTreeWidgetItem([" ",str(int(track['id'])+1),track['artist'],track['title'],track['album'],track['file'].split("/")[-1],track['file']])
			self.ui.treeWidget.addTopLevelItem(item)
		self.highlightTrack()
		
	def changeSong(self):
		song=str(self.connection.client.currentsong()['artist'])+"-"+str(self.connection.client.currentsong()['title'])
		self.status.setTrack(song)
		self.updateBar(True)
		self.highlightTrack()


	@QtCore.pyqtSlot()
	def on_playBtn_clicked(self):
		icon=QtGui.QIcon()
		if self.play:
			icon.addPixmap(QtGui.QPixmap(":/icons/media-playback-start.png"))
			self.status.setPlaying("Paused")
			self.connection.client.pause()
			self.updateBar(True)		
			self.play=False
			self.pupd.timer.stop()

		else:
			icon.addPixmap(QtGui.QPixmap(":/icons/media-playback-pause.png"))
			self.status.setPlaying("Playing")
			self.connection.client.play()
			self.updateBar(True)

			self.play=True
			self.pupd.timer.start()

		self.ui.playBtn.setIcon(icon)




	@QtCore.pyqtSlot()
	def on_nextBtn_clicked(self):
		icon=QtGui.QIcon()
		if not self.play:
			self.connection.client.play()
			self.play=True
			self.pupd.timer.start()
			
		icon.addPixmap(QtGui.QPixmap(":/icons/media-playback-pause.png"))
		self.status.setPlaying("Playing")
		self.connection.client.next()
		self.ui.playBtn.setIcon(icon)
		self.updateBar(True)

	@QtCore.pyqtSlot()
	def on_prevBtn_clicked(self):

		icon=QtGui.QIcon()
		if not self.play:
			self.connection.client.play()
			self.play=True
			self.pupd.timer.start()
			
		icon.addPixmap(QtGui.QPixmap(":/icons/media-playback-pause.png"))
		self.status.setPlaying("Playing")
		self.connection.client.previous()
		self.ui.playBtn.setIcon(icon)
		self.updateBar(True)


	def on_stopBtn_clicked(self):
		self.connection.client.stop()

		icon=QtGui.QIcon()
		if self.play:
			icon.addPixmap(QtGui.QPixmap(":/icons/media-playback-start.png"))
			self.ui.playBtn.setIcon(icon)
		self.play=False
		self.pupd.timer.stop()

		self.status.setPlaying("Stopped")
		self.ui.progressBar.setMaximum(200)
		self.ui.progressBar.setValue(0)
		self.ui.progressBar.setFormat("00:00")



	@QtCore.pyqtSlot()
	def on_volImg_clicked(self):
		icon=QtGui.QIcon()
		if self.mute:
			self.getVolIcon()
			self.mute=False
			vol=self.vol*5
			self.connection.client.setvol(vol)
		else:
			icon.addPixmap(QtGui.QPixmap(":/icons/audio-volume-muted.png"))
			self.mute=True
			self.vol=int(self.connection.status['volume'])//5
			self.connection.client.setvol(0)
			
			self.ui.volImg.setIcon(icon)
	def on_volSlider_valueChanged(self,a):
		if not self.mute: self.getVolIcon()
		volume=str(self.ui.volSlider.value()*5)
		self.ui.volSlider.setToolTip("Volume:"+volume)
		self.connection.client.setvol(volume)
		self.status.setVolume(volume)
		self.vol=volume
		
	def getVolIcon(self):
		icon=QtGui.QIcon()
		val=self.ui.volSlider.value()
		if val>15: vol="high"
		elif val<=15 and val>5: vol="medium"
		elif val<=5 and val>1: vol="low"
		else: vol="muted"
		icon.addPixmap(QtGui.QPixmap(":/icons/audio-volume-"+vol+".png"))
		self.ui.volImg.setIcon(icon)
	def highlightTrack(self):
		try:
			item=self.ui.treeWidget.topLevelItem(int(self.connection.client.currentsong()['id']))
			item.setText(0,"#")

		except: item=None
	
		try:
			self.plItem.setText(0,"")

		except: pass
		self.plItem=item

	def on_treeWidget_itemActivated(self,e):
		nr=e.text(1)
		self.connection.client.play(int(nr)-1)
	

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

class ProgressUpdate(QtCore.QThread):
	def __init__(self,parent):
		super(ProgressUpdate,self).__init__(parent)		
		self.parent=parent
		self.timer=QtCore.QTimer()
		
	def run(self):
		self.timer.setInterval(1000)
			

		

if __name__=="__main__":
	app= QtGui.QApplication(sys.argv)
	myapp = Player()
	myapp.show()
	sys.exit(app.exec_())
