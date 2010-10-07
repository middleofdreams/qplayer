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
		while self.running:
			self.sleep(1)
			self.status=self.client.status()
			self.emit(QtCore.SIGNAL("update_bar()"))
