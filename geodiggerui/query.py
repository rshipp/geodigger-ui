import threading
import time
from Crypto.Hash import SHA
import random
from bson.son import SON
import pymongo
import smtplib

import geodiggerui.config as config

class QueryThread(threading.Thread):
    def __init__(self, db, query, email, userlimit, downloadtype, host):
        super(QueryThread, self).__init__()
        self.daemon = True
        self.db = db
        self.query = query
        self.email = email
        self.userlimit = userlimit
        self.downloadtype = downloadtype.lower()
        self.host = host
        uniq = SHA.new("%s.%s" % (int(time.time()*1000),
            random.random())).hexdigest()
        self.filename = uniq + '.' + self.downloadtype
        # Email settings
        self.username = config.email['username']
        self.password = config.email['password']
        self.address = config.email['address']
        self.emailserver = config.email['server']

    def run(self):
        # Run the query.
        try:
            self.db.ensure_index([(u'loc', pymongo.GEOSPHERE)])
#            self.db.aggregate(SON([
#                ('$match', self.query),
#                ('$group', SON([
#                    ('_id', '$userID'),
#                    (),
#                    ])),
#            ]))
            pass
        except Exception as e:
            msg = "A problem occurred while processing your query.\n" +\
                  "The details of the error are as follows:\n" +\
                  str(e.message) + "\n"
        else:
            msg = "Your query has completed. The resulting data" +\
                  "file is available for download at\n" +\
                  "http://"+self.host+"/download/"+self.filename+"\n"

        # Email the results.
        try:
            smtp = smtplib.SMTP_SSL(self.emailserver)
            smtp.login(self.username, self.password)
            smtp.sendmail(self.address, self.email,
                "From: GeoDigger <"+e+">\n" +\
                "To: " + self.email + "\n" +\
                "Subject: Query Results\n\n" + msg)
            smtp.quit()
        except Exception as e:
            print e
