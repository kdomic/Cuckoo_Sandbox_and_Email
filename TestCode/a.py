#!/usr/bin/env python
import Queue
import threading
import urllib2, datetime

print "test " + datetime.date.today().strftime("%Y%m%d")+datetime.datetime.now().time().strftime("%H%M%S")

'''

from pprint import pprint

radi = True

def signal_handler(signal, frame):
	global radi
	radi = False
	print('You pressed Ctrl+C!')	

signal.signal(signal.SIGINT, signal_handler)

while radi:
	try:
		json_data=open('/home/kdomic/Downloads/cuckoo/storage/analyses/381/reports/report.json')
		data = json.load(json_data)
		pprint(data["virustotal"]["positives"])
		json_data.close()
	except Exception: 
		print "NEMA"
	time.sleep(3)










# called by each thread
def get_url(q, url):
	print url
	#
	q.task_done()


theurls = [1,2,3,4]

q = Queue.Queue()

for u in theurls:
	print "Po: "+ str(u)
	q.put(u)
	t = threading.Thread(target=get_url, args = (q,u))
	t.daemon = True
	t.start()

q.join()
'''