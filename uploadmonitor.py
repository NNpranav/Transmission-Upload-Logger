from __future__ import print_function
import bencode
import glob
import os
import os.path
import datetime
now = datetime.datetime.now()
from tabulate import tabulate

rspath = '/var/lib/transmission-daemon/.config/resume/*'
dbPath = 'torrentData.txt'
outPath = '/var/www/html/dailyRecord.txt'
tempOutPath = '/var/www/html/prevRecord.txt'
tfPath = '/var/lib/transmission-daemon/.config/torrents/*'

#open each resume file
files = glob.glob(rspath)
tempname = ""
totalDifference = 0
trackerName = ""
if not os.path.exists(dbPath):
	execfile('createdb.py')
	quit()

tableList = list()
today = now.strftime("%d-%m-%Y at %H:%M")
torEntry = ["","",today,""]
tableList.append(torEntry)
torEntry = ["","Upload","Tracker","Torrent"]
tableList.append(torEntry)
counter = 1

for file in files:
	splitName = file.split('.')
	torHash = splitName[len(splitName)-2]
	torrentFilePath = tfPath+torHash+'.torrent'
	torrentFile = glob.glob(torrentFilePath)
	for torrent in torrentFile:
		with open(torrent) as t:
			torD = t.read()
			tData = bencode.decode(torD)
			announce = tData['announce']
			tracker = announce.split('/')
			address = tracker[2].split(':')
			trackerName = address[0]
	with open(file) as f:
		torrentData = f.read()
		dTorrentData = bencode.decode(torrentData)
		tempname = dTorrentData['name']
		name = tempname + str(dTorrentData['added-date'])
		uploaded = dTorrentData['uploaded']/1048576
		with open(dbPath) as oldDB:
			oldData = oldDB.read()
			dOldData = bencode.decode(oldData)
			try:
				oldUpload = dOldData[name]
				if uploaded > oldUpload:
					uploadDifference = uploaded - oldUpload
					totalDifference += uploadDifference
					firstCol = str(uploadDifference)+" MB"
					torEntry = [counter,firstCol,trackerName,tempname]
					tableList.append(torEntry)
					counter+=1
			except:
				if uploaded > 0:
					firstCol = str(uploadDifference) + " MB"
					torEntry = [counter,firstCol,trackerName,tempname]
					tableList.append(torEntry)
					counter+=1
totalEntry = ["","","",""]
tableList.append(totalEntry)
uploadTotal = str(totalDifference)+" MB"
totalEntry = ["Total",uploadTotal,"--","--"]
tableList.append(totalEntry)

try:
	with open(outPath, 'r') as oldFile:
		with open(tempOutPath,'w') as dailyLog:
			dailyLog.write('\r\n')
			dailyLog.write('\r\n')
			dailyLog.write(tabulate(tableList, tablefmt="grid"))
			dailyLog.write('\r\n')
			dailyLog.write('\r\n')
			dailyLog.write(oldFile.read())
		dailyLog.close()
	oldFile.close()
	os.remove(outPath)
	os.rename(tempOutPath, outPath)
except:
	with open(tempOutPath,'w') as dailyLog:
		dailyLog.write('\r\n')
		dailyLog.write('\r\n')
		dailyLog.write(tabulate(tableList, tablefmt="grid"))
		dailyLog.write('\r\n')
		dailyLog.write('\r\n')
        dailyLog.close()
	os.rename(tempOutPath, outPath)

#reset database
execfile('createdb.py')
