import mpd
from PyQt4 import QtCore

class Connection(QtCore.QThread):
	def __init__(self,parent):
		super(Connection,self).__init__(parent)		
	def run(self):
		PASSWORD = False
		self.client = mpd.MPDClient()
		self.client.connect("localhost", 6600)
		if PASSWORD:
			try:
				client.password(PASSWORD)
			except CommandError:
				exit(1)
		self.status=self.client.status()
		#po pobraniu info wysyla sygnal
		self.emit(QtCore.SIGNAL("get_status()"),)
		self.running=True
		self.currentsong=self.client.currentsong()
		self.currentplaylist=self.client.playlist()
		while self.running:
			self.sleep(1)
			self.status=self.client.status()
			if self.currentsong!=self.client.currentsong():
				self.currentsong=self.client.currentsong()
				self.emit(QtCore.SIGNAL("change_song()"),)
			if self.currentplaylist!=self.client.playlist():
				self.currentplaylist=self.client.playlist()
				self.emit(QtCore.SIGNAL("change_playlist()"),)
	def error(self,err_nr):
		if err_nr==1:
			self.emit(QtCore.SIGNAL("playback_error()"),)

	def play(self,id=None):
		if id==None:
			self.client.play()
		else: self.client.play(id)
		if self.client.status()['state']!="play": self.error(1)
	def pause(self):
		self.client.pause()
		if self.client.status()['state']!="pause": self.error(1)		

	def stop(self):
		self.client.stop()
		if self.client.status()['state']!="stop": self.error(1)	
	def previous(self):
		self.client.previous()
		if self.client.status()['state']!="play": self.error(1)							

	def next(self):
		self.client.next()
		if self.client.status()['state']!="play": self.error(1)		
