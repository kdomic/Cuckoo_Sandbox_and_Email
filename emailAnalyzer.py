#!/usr/bin/env python
import email, imaplib, os
import time 
import signal
import sys
import json
import datetime

running = True

def signal_handler(signal, frame):
	global running
	running = False
	print('You pressed Ctrl+C!')
signal.signal(signal.SIGINT, signal_handler)


class Email:
	temp_dir = '/home/kdomic/UPLOAD/'
	imap = None

	def __init__(self):
		print "...:::Email analysis started:::..."

	def connect(self, username, password, host, port):
		self.imap = imaplib.IMAP4(host, port)
		self.imap.login(username,password)

	def close(self):
		try:
			self.imap.logout()
			self.imap.close();
		except Exception:
			print ""
		print "...:::END:::..."

	def read(self):
		self.imap.select("INBOX")
		resp, items = self.imap.search(None, 'RECENT')
		items = items[0].split()
		
		for emailid in items:			
			newEmailId = self.moveMessage(emailid, 'INBOX', 'PROCESSING')
			self.analyzeMessage(newEmailId,'PROCESSING')
			break

	def analyzeMessage(self, emailid, folder):
		import email
		self.imap.select(folder)
		resp, data = self.imap.fetch(emailid, "(RFC822)")
		email_body = data[0][1]
		mail = email.message_from_string(email_body)

		if mail.get_content_maintype() != 'multipart':
			return "notMine"

		print "["+mail["From"]+"]:" + mail["Subject"]

		for part in mail.walk():
			if part.get_content_maintype() == 'multipart':
				continue

			if part.get('Content-Disposition') is None:
				continue

			filename = part.get_filename()
			counter = 1

			if not filename:
				filename = 'part-%03d%s' % (counter, 'bin')
				counter += 1

			date = datetime.date.today().strftime("%Y%m%d")
			time = datetime.datetime.now().time().strftime("%H%M%S")
			path = os.path.join(self.temp_dir, filename+"_"+date+time)

			if not os.path.isfile(path):
				fp = open(path, 'wb')
				fp.write(part.get_payload(decode=True))
				fp.close()	            	
				if(self.sendFileToCuckoo(path)==False):
					print "----------------------------------OK"
					newId = self.moveMessage(emailid,'PROCESSING','INBOX')
					self.imap.store(newId, 'FLAGS', '(\UNSEEN)')
				else:
					print "----------------------------------VIRUS"
					self.moveMessage(emailid,'PROCESSING','SPAM')

	def sendFileToCuckoo(self, path):
		from lib.cuckoo.common.objects import Dictionary
		from lib.cuckoo.core.database import Database
		db = Database()
		a = db.add_path(path,package="")
		#a = db.add_path(path, 60, None, None, 3, None, 'cuckoo1', 'windows', False, False, None)
		print "Analyzing task: " + str(a)
		return self.isVirus(a)

	def isVirus(self,analysisId):
		if(analysisId==None):
			return True
		global running			
		while running:
			try:
				json_data=open('/home/kdomic/Downloads/cuckoo/storage/analyses/'+str(analysisId)+'/reports/report.json')
				data = json.load(json_data)
				json_data.close()
				try:
					virusNum = data["virustotal"]["positives"]
					if(virusNum==0):
						print "FILE: OK"
						return False
					else:	
						print "FILE: VIRUS DETECTED"
						return True
				except Exception:
					print "Unknown file type"
					return False
			except Exception:
				print "Analyzing: Task [" + str(analysisId) +"]"
			time.sleep(10)

	def createFolder(self, name):
		typ, create_response = self.imap.create(name)
		#print 'CREATED '+name+':', create_response

	def moveMessage(self, emailid, fromFolder, toFolder):
		#print 'COPYING:', emailid
		mId = self.getMessageId(fromFolder,emailid)
		self.createFolder(toFolder)
		self.imap.copy(emailid, toFolder)
		typ, response = self.imap.store(emailid, '+FLAGS', '\Deleted')
		typ, response = self.imap.expunge()
		newEmailid = self.getMessageNum(toFolder,mId)
		return newEmailid

	def getMessageNum(self, folder, mId):
		import email
		self.imap.select(folder)
		resp, items = self.imap.search(None, 'ALL')
		items = items[0].split()
		for num in items:
			typ, data = self.imap.fetch(num, '(RFC822)')
			mail = email.message_from_string(data[0][1])
			if(mail["Message-ID"]==mId):
				return num

	def getMessageId(self, folder, num):
		import email
		self.imap.select(folder)
		resp, items = self.imap.search(None, 'ALL')
		typ, data = self.imap.fetch(num, '(RFC822)')
		mail = email.message_from_string(data[0][1])
		return mail["Message-ID"]

	def test(self):
		self.imap.select("PROCESSING")
		#print self.imap.uid("FETCH", "<539EEC59.7080905@localhost.com>", "(RFC822)")
		resp, items = self.imap.search(None, 'ALL')
		items = items[0].split()
		for num in items:
			print "-------------------------------------------"
			typ, data = self.imap.fetch(num, '(RFC822)')
			#print 'Message %s\n%s\n' % (num, data[0][1])
			#typ, response = self.imap.fetch(num, '(FLAGS)')
			#print 'Flags after:', response	

###main

while running:
	email = Email()
	email.connect("korisnik1@localhost.com", "123456", "localhost.com",143)
	email.read()
	email.close()
	time.sleep(10)