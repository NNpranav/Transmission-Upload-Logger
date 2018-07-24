from __future__ import print_function
import bencode
import glob

#Transmission .resume files path:
rspath = '/var/lib/transmission-daemon/.config/resume/*'
dbPath = 'torrentData.txt'

files=glob.glob(rspath)
with open(dbPath,'w') as db:
	db.write('d')
db.close()
for file in files:
	with open(file) as f:
		torrentData = f.read()
		torrent = bencode.decode(torrentData)
		tempname = torrent['name']
		addeddate = torrent['added-date']
		uploaded = torrent['uploaded']/1048576
		name = tempname + str(addeddate)
		euploaded = bencode.encode(uploaded)
		ename = bencode.encode(name)
		with open(dbPath,'a') as db:
			db.write(ename)
			db.write(euploaded)
		db.close()

with open(dbPath,'a') as db:
	db.write('e')
db.close()
