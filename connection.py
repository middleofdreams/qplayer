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
		print self.status
		#po pobraniu info wysyla sygnal
		self.emit(QtCore.SIGNAL("get_status()"),)
		self.sleep(1)
		self.running=True
		self.currentsong=self.client.currentsong()
		self.currentplaylist=self.client.playlist()
		self.state=self.client.status()['state']
		self.emit(QtCore.SIGNAL("database_fill()"),)
		while self.running:
			self.sleep(1)
			self.status=self.client.status()
			if self.currentsong!=self.client.currentsong():
				#self.sleep(0.1)
				self.currentsong=self.client.currentsong()
				self.emit(QtCore.SIGNAL("change_song()"),)
				self.sleep(1)
			if self.currentplaylist!=self.client.playlist():
				self.currentplaylist=self.client.playlist()
				self.emit(QtCore.SIGNAL("change_playlist()"),)
				self.sleep(1)
			try:
				if self.state!=self.client.status()['state']:
					self.sleep(1)
					self.state=self.client.status()['state']
					self.emit(QtCore.SIGNAL("get_status()"),)
			except:pass
	
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

	
