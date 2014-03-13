import threading
import time

class QueryThread(threading.Thread):
    def __init__(self, db, query, email, userlimit, downloadtype):
        super(QueryThread, self).__init__()
        self.daemon = True
        self.db = db
        self.query = query
        self.email = email
        self.userlimit = userlimit
        self.downloadtype = downloadtype

    def run(self):
        time.sleep(10)
        print "hi!!"
