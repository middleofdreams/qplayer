import mpd
from PyQt4 import QtCore,QtGui

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
		self.sleep(1)
		self.running=True
		self.currentsong=self.client.currentsong()
		self.currentplaylist=self.client.playlist()
		self.state=self.client.status()['state']
		

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
			self.give5tries(self.client.play)
		else: self.client.play(id)
		if self.give5tries(self.client.status)['state']!="play": self.error(1)
	def pause(self):
		self.give5tries(self.client.pause)
		if self.give5tries(self.client.status)['state']!="pause": self.error(1)		

	def stop(self):
		self.give5tries(self.client.stop)
		if self.give5tries(self.client.status)!="stop": self.error(1)	
	def previous(self):
		self.give5tries(self.client.previous)
		if self.give5tries(self.client.status)!="play": self.error(1)							

	def next(self):
		self.give5tries(self.client.next)
		if self.give5tries(self.client.status)['state']!="play": self.error(1)		
	def give5tries(self,func):
		i=0
		value=None
		while i<5:
			try:
				value=func()
				i=5
			except:
				i+=1
		return value
class LoadDatabase(QtCore.QThread):
	def __init__(self,parent,listall):
		super(LoadDatabase,self).__init__(parent)
		self.listall=listall		
	def run(self):	
		self.items=[]
		artists=[]
		#albums=[]
		albums={}
		#albums={'Unknown artist':{'Unknown album':[]}
		for i in self.listall:
			try:
				artist=i['artist']
			except:
				artist=".Unknown artist"
			try:
				track=[i['title'],i['file']]
			except:
				try:
					track=[i['file'],i['file']]
				except:
					track="$$5dir5$$"	
			try:	
				album=i['album']
			except: 
				album=".Unknown album"
			if track!="$$5dir5$$":
				#if not artist in album: albums[artist]=[]
				try:albums[artist]
				except KeyError:albums[artist]={}
				if 	albums[artist].has_key(album):
					albums[artist][album].append(track)
				else :
					albums[artist][album]=[track]


		#print albums
		for i in albums:
			item=QtGui.QTreeWidgetItem([str(i)])
			for j in albums[i]:
				child=QtGui.QTreeWidgetItem([str(j)])
				item.addChild(child)
				for k in albums[i][j]:
					grandchild=QtGui.QTreeWidgetItem(k)
					child.addChild(grandchild)
		
			self.items.append(item)
		#print i,j,k
	
		self.emit(QtCore.SIGNAL("add_item()"),)
