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
		QtCore.QObject.connect(self.connection,QtCore.SIGNAL("change_playlist()"), self.loadPlaylist)
		QtCore.QObject.connect(self.connection,QtCore.SIGNAL("playback_error()"), self.playbackError)
		QtCore.QObject.connect(self.connection,QtCore.SIGNAL("database_fill()"), self.databaseFill)

		#tu bedzie wiecej podlaczen... zapewne
		#odpalenie watku
		self.connection.start()
		self.pupd.start()
	
	def databaseFill(self):
		artists=[]
		albums={}
		for i in self.connection.client.listallinfo():
			try:
				artist=i['artist']
				album=i['album']
				title=i['title']
				if not album in albums:
					albums[artist]=[]
				albums[artist].append(album)	
			except: pass	
		for i in albums:
			item=QtGui.QTreeWidgetItem([str(i)])
			self.ui.treeWidget_2.addTopLevelItem(item)
			for j in albums[i]:
				child=QtGui.QTreeWidgetItem([str(j)])
				item.addChild(child)		
	def updateBar(self,force=False):
		if force:
			try:
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
			except:
				pass
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
	


		if  status== 'pause' or status== 'stop':
			self.play=False
			print "a"
			try: 
				self.pupd.timer.stop()
				print "aa"
			except: pass

		else:
			self.play=True
			self.pupd.timer.start()


		#pobranie nazwy artysty
		title,artist,album=self.getTags(self.connection.client.currentsong())
		song=artist+" - "+title
		self.status=StatusInfo(self.ui.statusbar,self,song,"",str(self.ui.volSlider.value()*5),status.capitalize())
		self.setWindowTitle(song)
		self.setPlayPauseBtn()

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
		self.loadPlaylist()
		
	def loadPlaylist(self):
		self.ui.treeWidget.clear()
		#ladowanie playlisty:
		for track in self.connection.client.playlistinfo():
			title,artist,album=self.getTags(track)
			item=QtGui.QTreeWidgetItem([" ",str(int(track['pos'])+1),artist,title,album,track['file'].split("/")[-1],track['file']])
			self.ui.treeWidget.addTopLevelItem(item)
		self.highlightTrack()
		
	def changeSong(self):
		title,artist,album=self.getTags(self.connection.currentsong)
		song=artist+" - "+title
		self.status.setTrack(song)
		self.updateBar(True)
		self.highlightTrack()
		self.setWindowTitle(song)


	@QtCore.pyqtSlot()
	def on_playBtn_clicked(self):
		if self.play:
			self.status.setPlaying("Paused")
			self.connection.pause()
			self.play=False
			self.pupd.timer.stop()
			self.connection.pause()
			self.updateBar(True)		


		else:
			self.play=True
			self.pupd.timer.start()
			self.connection.play()
			self.updateBar(True)

		self.setPlayPauseBtn()



	@QtCore.pyqtSlot()
	def on_nextBtn_clicked(self):
		if not self.play:
			self.connection.play()
			self.play=True
			self.pupd.timer.start()
			self.setPlayPauseBtn()
	
		self.connection.next()
		self.updateBar(True)

	@QtCore.pyqtSlot()
	def on_prevBtn_clicked(self):

		if not self.play:
			self.connection.play()
			self.play=True
			self.pupd.timer.start()
			self.setPlayPauseBtn()

		self.connection.previous()
		self.updateBar(True)


	def on_stopBtn_clicked(self):
		self.connection.stop()

		self.play=False
		self.setPlayPauseBtn()

		self.pupd.timer.stop()

		self.status.setPlaying("Stop")
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
			item=self.ui.treeWidget.topLevelItem(int(self.connection.client.currentsong()['pos']))
			item.setText(0,"#")

		except: item=None
	
		try:
			self.plItem.setText(0,"")

		except: pass
		self.plItem=item

	def on_treeWidget_itemActivated(self,e):
		nr=e.text(1)
		self.connection.client.play(int(nr)-1)
		self.play=True
		self.pupd.timer.start()
		self.setPlayPauseBtn()
	
	def setPlayPauseBtn(self):
		icon=QtGui.QIcon()
		if self.play:
			self.status.setPlaying("Play")

			icon.addPixmap(QtGui.QPixmap(":/icons/media-playback-pause.png"))
		else:
			icon.addPixmap(QtGui.QPixmap(":/icons/media-playback-start.png"))
		self.ui.playBtn.setIcon(icon)

	def getTags(self,track):
			try: artist=track['artist']
			except: artist=""
			try: title=track['title']
			except: title=""
			try: album=track['album']
			except: album=""
			if artist=="" and title=="": 
				try: title=track['file'].split("/")[-1]
				except: title="--"
			return title,artist,album
			
	def playbackError(self):
		self.play=False
		self.pupd.timer.stop()
		self.setPlayPauseBtn()
		self.status.setPlaying("Stop")
class StatusInfo(object):
	
	def __init__(self,statusbar,mw,track,time,volume,playing):
		self.statusbar=statusbar
		self.mw=mw
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
