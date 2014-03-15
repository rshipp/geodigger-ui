import os
import smtplib
import subprocess
import random
import threading
import time

from Crypto.Hash import SHA
from shapely.geometry import Point, Polygon
import pymongo

import geodiggerui.config as config

class QueryThread(threading.Thread):
    def __init__(self, db, query, polygon, email, userlimit, host):
        super(QueryThread, self).__init__()
        self.daemon = True
        self.db = db
        self.query = query
        self.polygon = polygon
        if self.polygon == None:
            self.polygon = [
                    [-180, 90],
                    [-180, -90],
                    [180, -90],
                    [180, 90]
            ]
        self.email = email
        self.userlimit = userlimit
        self.host = host
        uniq = SHA.new("%s.%s" % (int(time.time()*1000),
            random.random())).hexdigest()
        self.filename = uniq + '.csv'
        self.filepath = config.ui['tmp'] + '/' + self.filename
        self.tfilepath = config.ui['tmp'] + '/tmp' + self.filename
        # Email settings
        self.username = config.email['username']
        self.password = config.email['password']
        self.address = config.email['address']
        self.emailserver = config.email['server']

    def run(self):
        # Run the query.
        try:
            # Open the data file.
            with open(self.filepath, 'w+') as f:
                self.db.ensure_index([(u'loc', pymongo.GEOSPHERE)])
                # Write the data.
                for record in self.db.find(self.query):
                    f.write("%s,%s,%s,%s\n" % (record['userID'], record['time'],
                                        record['loc']['coordinates'][0],
                                        record['loc']['coordinates'][1])
                                        )
            # Sort the data file by user ID.
            sort = subprocess.check_call(["sort", self.filepath, "-o",
                self.filepath])
            # Do postprocessing.
            # Initial values.
            polygon = Polygon(self.polygon)
            current = None
            skip = False
            tweets = []
            seq = 1
            # Loop over the data.
            with open(self.filepath, 'r+') as f, open(self.tfilepath, 'w+') as output:
                for line in f:
                    data = line.replace('\n', '').split(',')
                    user = data[0]
                    date = data[1]
                    if current == user and skip:
                        continue
                    location = (float(data[2]), float(data[3]))
                    point = Point(location)
                    # location is in target area
                    if point.within(polygon):
                        # 1st user? 
                        if current == None:
                            tweets.append([date, location])
                            current = user
                            skip = False
                        # same user? 
                        elif current == user:
                            tweets.append([date, location])
                        # user changed!
                        else:
                            # save data for the current user, if > 1
                            if len(tweets) > 1:
                                # but first let's check if it is not a robot
                                robot = True
                                location = None
                                for tweet in tweets:
                                    if location == None:
                                        location = tweet[1]
                                    elif location != tweet[1]:
                                        robot = False
                                        break
                                # OK, your are not a robot
                                if not robot:
                                    for tweet in tweets:
                                        output.write(str(seq) + ',' + str(tweet[0]) + ',' + str.format('{0:.5f}', tweet[1][0]) + ',' + str.format('{0:.5f}', tweet[1][1]) + '\n')
                                    seq += 1
                                tweets = []
                            tweets.append([date, location])
                            current = user
                            skip = False    
                    # location is outside target area
                    else:
                        # 1st user? 
                        if current == None:
                            current = user
                            skip = True
                        # same user?
                        elif current == user:
                            skip = True
                        # user changed!
                        else:
                            # save data for the current user, if > 1
                            if len(tweets) > 1:
                                # but first let's check if it is not a robot
                                robot = True
                                location = None
                                for tweet in tweets:
                                    if location == None:
                                        location = tweet[1]
                                    elif location != tweet[1]:
                                        robot = False
                                        break
                                # OK, your are not a robot
                                if not robot:
                                    for tweet in tweets:
                                        output.write(str(seq) + ',' + str(tweet[0]) + ',' + str.format('{0:.5f}', tweet[1][0]) + ',' + str.format('{0:.5f}', tweet[1][1]) + '\n')
                                    seq += 1
                                tweets = []
                            current = user
                            skip = True
            # If a user limit was specified, use it.
            if self.userlimit != 0:
                numusers = subprocess.check_output(["tail", "-1",
                    self.tfilepath]).split(',')[0]
                if len(numusers) == 0:
                    raise Exception("No tweets were found matching your query.")
                else:
                    numusers = int(numusers)
                if self.userlimit >= numusers:
                    self.userlimit = numusers-1
                users = random.sample(range(1, numusers),
                        self.userlimit)
                with open(self.tfilepath, 'r+') as f, open(self.filepath, 'w+') as output:
                    for line in f:
                        if int(line.split(',')[0]) in users:
                            output.write(line)
            else:
                # No user limit, just rename the file.
                subprocess.check_call(["mv", self.tfilepath,
                    self.filepath])
            # Remove the tmp file.
            if os.path.exists(self.tfilepath):
                os.remove(self.tfilepath)

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
                "From: GeoDigger <"+self.email+">\n" +\
                "To: " + self.email + "\n" +\
                "Subject: Query Results\n\n" + msg)
            smtp.quit()
        except Exception as e:
            print e
