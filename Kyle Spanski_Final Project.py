# -*- coding: utf-8 -*-
"""
Kyle Spanski Final


"""
#1a

import re, sqlite3, json

UserTable = '''CREATE TABLE Users
(
user_id_1 integer NOT NULL,
name varchar2(100),
screen_name varchar2(100),
description varchar2(100),
friends_count integer,
  
CONSTRAINT Twitter2_PK
    PRIMARY KEY(user_id_1)
      
);'''

TweetTable = '''CREATE TABLE Tweets
(
created_at Date,
id_str varchar2(250) NOT NULL, 
text TEXT,
source varchar2(100),
in_reply_to_user_id varchar2(30),
in_reply_to_screen_name varchar2(30),
in_reply_to_status_id varchar2(30),
retweet_count integer,
contributors varchar2(30),
user_id integer,
GeoID varchar2(60),

CONSTRAINT Twitter1_PK
    PRIMARY KEY(id_str)

CONSTRAINT Twitter1_FK
    FOREIGN KEY(user_id)
    REFERENCES Users(userid)

CONSTRAINT GeoID_FK
    FOREIGN KEY(GeoID)
    REFERENCES Geo(GeoID)    
); '''



GeoTable = '''CREATE TABLE Geo
(
GeoID varchar2(60),
type varchar2(50),
longitude varchar2(50),
latitude varchar2(50),
CONSTRAINT GeoID_PK
    PRIMARY KEY(longitude, latitude)

); '''

        
conn = sqlite3.connect("FinalDatabase.db")
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS Users;")
cursor.execute("DROP TABLE IF EXISTS Tweets;")
cursor.execute("DROP TABLE IF EXISTS Geo;")

cursor.execute(UserTable)
cursor.execute(GeoTable)
cursor.execute(TweetTable)

conn.commit()
conn.close()


#1b

import urllib.request as urllib
import codecs,time
response = urllib.urlopen("http://rasinsrv07.cstcis.cti.depaul.edu/CSC455/OneDayOfTweets.txt")
lines = []
count = 0
countgood = 0
tweetfile = codecs.open('tweetfile.txt','w','utf-8')

start = time.time()

for i in range(500000):
    tweet = response.readline().decode("utf8")
    tweetfile.write(tweet)
tweetfile.close()

end = time.time()

print ("Creating tweetfile took ", (end-start), ' seconds.') #Creating tweetfile took  588.8216786384583  seconds.


#1c
import urllib.request as urllib
import codecs,time
response = urllib.urlopen("http://rasinsrv07.cstcis.cti.depaul.edu/CSC455/OneDayOfTweets.txt")
lines = []
count = 0

start = time.time()

for i in range(500000):
    str_response = response.readline().decode("utf8")
    try:
        tDict = json.loads(str_response)
        createdat = tDict['created_at']
        idstr = tDict['id_str']
        text = tDict['text']
        source = tDict['source']
        inreplytouserid = tDict['in_reply_to_user_id']
        inreplytoscreenname = tDict['in_reply_to_screen_name']
        inreplytostatusid = tDict['in_reply_to_status_id']
        if 'retweeted_status' in tDict:
            retweetcount = tDict['retweeted_status']['retweet_count']
        else:
            retweetcount = tDict['retweet_count']
        contributors = tDict['contributors']
        userid = tDict['user']['id']
        name = tDict['user']['name']
        
        screenname = tDict['user']['screen_name']
        
        description = tDict['user']['description']
        friendscount = tDict['user']['friends_count']
        
        geo = tDict['geo']
        GeoID = 'None'
         
        if geo is None:
            pass
        else:
            geo_type = tDict['geo']['type']
            coordinates = tDict['geo']['coordinates']
            longitude = coordinates[0]
            latitude = coordinates[1]
            GeoID = str(longitude) + '-' + str(latitude)
            cursor.execute("INSERT OR IGNORE INTO Geo Values(?,?,?,?)", (GeoID, geo_type, longitude, latitude))
        
        cursor.execute("INSERT OR IGNORE INTO Users Values(?,?,?,?,?)", (userid, name, screenname, description, friendscount))
             
        cursor.execute("INSERT OR IGNORE INTO Tweets Values(?,?,?,?,?,?,?,?,?,?,?)", (createdat, idstr, text, source, inreplytouserid, inreplytoscreenname, inreplytostatusid, retweetcount, contributors, userid, GeoID))
        
        
        count +=1
        #print(countgood,' ', createdat, '\n')
    except ValueError:
        pass
       
        
end = time.time()
print ("Loading tweets to SQL from web took ", (end-start), ' seconds.') #Loading tweets to SQL from web took  585.87451004982  seconds.

print(cursor.execute("SELECT count(*) FROM Users;").fetchall())
print(cursor.execute("SELECT count(*) FROM Tweets;").fetchall())
print(cursor.execute("SELECT count(*) FROM Geo;").fetchall())

print(count)


#1d
import urllib.request as urllib
import codecs,time
response = codecs.open("C:/Users/Kyle/Documents/DePaul Classes/CSC 455/Final/tweetfile.txt",'r','utf-8')
lines = []
count = 0

start = time.time()

for i in range(500000):
    str_response = response.readline()
    try:
        tDict = json.loads(str_response)
        createdat = tDict['created_at']
        idstr = tDict['id_str']
        text = tDict['text']
        source = tDict['source']
        inreplytouserid = tDict['in_reply_to_user_id']
        inreplytoscreenname = tDict['in_reply_to_screen_name']
        inreplytostatusid = tDict['in_reply_to_status_id']
        if 'retweeted_status' in tDict:
            retweetcount = tDict['retweeted_status']['retweet_count']
        else:
            retweetcount = tDict['retweet_count']
        contributors = tDict['contributors']
        userid = tDict['user']['id']
        name = tDict['user']['name']
        
        screenname = tDict['user']['screen_name']
        
        description = tDict['user']['description']
        friendscount = tDict['user']['friends_count']
        
        geo = tDict['geo']
        GeoID = 'None'
         
        if geo is None:
            pass
        else:
            geo_type = tDict['geo']['type']
            coordinates = tDict['geo']['coordinates']
            longitude = coordinates[0]
            latitude = coordinates[1]
            GeoID = str(longitude) + '-' + str(latitude)
            cursor.execute("INSERT OR IGNORE INTO Geo Values(?,?,?,?)", (GeoID, geo_type, longitude, latitude))
        
        cursor.execute("INSERT OR IGNORE INTO Users Values(?,?,?,?,?)", (userid, name, screenname, description, friendscount))
             
        cursor.execute("INSERT OR IGNORE INTO Tweets Values(?,?,?,?,?,?,?,?,?,?,?)", (createdat, idstr, text, source, inreplytouserid, inreplytoscreenname, inreplytostatusid, retweetcount, contributors, userid, GeoID))
        
        
        count +=1
        #print(countgood,' ', createdat, '\n')
    except ValueError:
        pass
       
        
end = time.time()
print ("Loading tweets to SQL from file took ", (end-start), ' seconds.') #Loading tweets to SQL from file took  325.9846453666687  seconds.

print(cursor.execute("SELECT count(*) FROM Users;").fetchall())
print(cursor.execute("SELECT count(*) FROM Tweets;").fetchall())
print(cursor.execute("SELECT count(*) FROM Geo;").fetchall())

print(count)



#1e

import urllib.request as urllib
import codecs,time


def loadTweets(tweetLines):

    # Collect multiple rows so that we can use "executemany".  We do
    # not want to collect all of the numLines rows because there may
    # not be enough memory for that. So we insert batchRows at a time
    batchRows = 50
    batchedInserts = []

    # as long as there is at least one line remaining
    while len(tweetLines) > 0:
        line = tweetLines.pop(0) # take off the first element from the list, removing it
    
        jsonobject = json.loads(line)

        newRow = [] # hold individual values of to-be-inserted row
        
        user_id = jsonobject['user']['id']
        
        geo = jsonobject['geo']
        GeoID = 'None'
         
        if geo is None:
            pass
        else:
            coordinates = jsonobject['geo']['coordinates']
            longitude = coordinates[0]
            latitude = coordinates[1]
            GeoID = str(longitude) + '-' + str(latitude)
            
        tweetKeys = ['created_at','id_str','text','source','in_reply_to_user_id', 'in_reply_to_screen_name', 'in_reply_to_status_id', 'retweet_count', 'contributors',"'"+user_id+"'","'"+GeoID+"'"]

        for key in tweetKeys:
            # Treat '', [] and 'null' as NULL
            if jsonobject[key] in ['',[],'null']:
                newRow.append(None)
            else:
                newRow.append(jsonobject[key])

        # Add the new row to the collected batch
        batchedInserts.append(newRow)

        # If we have reached # of batchRows, use executemany to insert what we collected
        # so far, and reset the batchedInserts list back to empty
        if len(batchedInserts) >= batchRows or len(tweetLines) == 0:
            conn.executemany('INSERT INTO Tweets VALUES(?,?,?,?,?,?,?,?,?,?,?)', batchedInserts)
            # Reset the batching process
            batchedInserts = []

start = time.time()
fd = open('tweetfile.txt', 'r', encoding='utf8')

loadTweets( fd.readlines() )

end   = time.time()

print ("loadTweets took ", (end-start), ' seconds.')
print ("Loaded ", conn.execute('SELECT COUNT(*) FROM Tweets').fetchall()[0], " rows")

#####################################   




#2ai 
start = time.time()
print(cursor.execute("SELECT id_str FROM Tweets WHERE id_str LIKE '%44%' OR '%77%';").fetchall())
end   = time.time()
print ("query took ", (end-start), ' seconds.')#query took  0.22001266479492188  seconds.


#2aii
start = time.time()
print(cursor.execute("SELECT COUNT(DISTINCT(in_reply_to_user_id)) FROM Tweets;").fetchall())
end   = time.time()
print ("query took ", (end-start), ' seconds.')#query took  0.8740499019622803  seconds.


#2aiii
start = time.time()
print(cursor.execute("SELECT id_str, text FROM Tweets WHERE LENGTH(text) = (SELECT MAX(LENGTH(text)) FROM Tweets);").fetchall())
end   = time.time()
print ("query took ", (end-start), ' seconds.')#query took  1.2190697193145752  seconds.


#2aiv
start = time.time()
print(cursor.execute("SELECT avg(longitude), avg(latitude) FROM Geo;").fetchall())
end   = time.time()
print ("query took ", (end-start), ' seconds.')#query took  0.00500035285949707  seconds.


#2v
start = time.time()
for i in range(10):
    cursor.execute("SELECT avg(longitude), avg(latitude) FROM Geo;").fetchall()
end   = time.time()
print ("query x10 took ", (end-start), ' seconds.')#query x10 took  0.06000328063964844  seconds.


start = time.time()
for i in range(100):
    cursor.execute("SELECT avg(longitude), avg(latitude) FROM Geo;").fetchall()
end   = time.time()
print ("query x100 took ", (end-start), ' seconds.')#query x100 took  0.44202542304992676  seconds.

#It seems that the query speeds up as you increase the number of iterations (pulling a query 100x does not take 100x as long)

#2bi

import sqlite3, json
import urllib.request as urllib
import codecs,time
response = codecs.open("C:/Users/Kyle/Documents/DePaul Classes/CSC 455/Final/tweetfile.txt",'r','utf-8')
DictID_count = []
DictID7744_count = []
y = '77'
x = '44' 

start = time.time()
for i in range(500000):
    str_response = response.readline()  
    try:
        tDict = json.loads(str_response)
        DictID_count.append(tDict['id_str'])     
    except(ValueError):
        pass
for i in DictID_count:
    if x in i:
        DictID7744_count.append(i)
for i in DictID_count:
    if y in i:
        DictID7744_count.append(i)
       
        
print(DictID7744_count )
end   = time.time()
print ("using python for 2i took ", (end-start), ' seconds.')#using python for 2bi took  105.5790388584137  seconds.

###########################################################################

#2bii
import sqlite3, json
import urllib.request as urllib
import codecs,time
response = codecs.open("C:/Users/Kyle/Documents/DePaul Classes/CSC 455/Final/tweetfile.txt",'r','utf-8')

ReplyUserID_count = []
UniqueReplyUserID_count = []
start = time.time()
for i in range(500000):
    str_response = response.readline()  
    try:
        tDict = json.loads(str_response)
        ReplyUserID_count.append(tDict['in_reply_to_user_id'])     
    except(ValueError):
        pass

for i in ReplyUserID_count:
    if i in UniqueReplyUserID_count:
        pass
    else:
        UniqueReplyUserID_count.append(i)
       
        
print(len(UniqueReplyUserID_count) )#90523
end   = time.time()
print ("using python for 2ii took ", (end-start), ' seconds.')#using python for 2bii took  241.39580702781677  seconds.

#The run time is much longer for this way than just querying the SQL table

#2d

import sqlite3, json
import urllib.request as urllib
import codecs,time
response = codecs.open("C:/Users/Kyle/Documents/DePaul Classes/CSC 455/Final/tweetfile.txt",'r','utf-8')

Longitudes = []
Latitudes = []

start = time.time()
for i in range(500000):
    str_response = response.readline()  
    try:
        tDict = json.loads(str_response)
        geo = tDict['geo']
        if geo is None:
            pass
        else:
            coordinates = tDict['geo']['coordinates']
            longitude = coordinates[0]
            latitude = coordinates[1]
            Longitudes.append(longitude)
            Latitudes.append(latitude)
    except(ValueError):
        pass

   
        
print(sum(Longitudes) / len(Longitudes) ) #15.036995659853126
print(sum(Latitudes) / len(Latitudes) ) #-41.38876593125317
end   = time.time()
print ("using python for 2iv took ", (end-start), ' seconds.')#using python for 2d took  53.597065687179565  seconds.

##########################################################################################

#3a
import codecs,time

start = time.time()

UsersInsertCount = print(cursor.execute("SELECT COUNT(*) FROM Users;").fetchall()) #447299

UsersInsertValues = cursor.execute("SELECT * FROM Users;").fetchall()

UsersInsertsfile = codecs.open('UsersInsertsfile.txt','w','utf-8')

for entry in UsersInsertValues:
    UsersInsertsfile.write('INSERT INTO Users VALUES (' + str(entry[0]) + ',' + str(entry[1]) + ',' + str(entry[2]) + ','+ str(entry[3]) + ','+ str(entry[4]) + ');\n')

UsersInsertsfile.close()

end   = time.time()
print ("creating INSERT statements took ", (end-start), ' seconds.')#creating INSERT statements took  3.704211711883545  seconds.






#3b
import sqlite3, json
import urllib.request as urllib
import codecs,time
fd = codecs.open("C:/Users/Kyle/Documents/DePaul Classes/CSC 455/Final/tweetfile.txt",'r','utf-8')

start = time.time()
for i in range(500000):
    allLines = fd.readline()
    try:
        tDict = json.loads(allLines)
        userid = tDict['user']['id']
        name = tDict['user']['name']       
        screenname = tDict['user']['screen_name']
        description = tDict['user']['description']
        friendscount = tDict['user']['friends_count']
    except ValueError:
        pass    
    UserData = [userid, name, screenname, description, friendscount]  
    cursor.execute('INSERT OR IGNORE INTO Users VALUES (?,?,?,?,?);', UserData)

end   = time.time()
print ("Populating Users table from file took ", (end-start), ' seconds.')#Populating Users table from file took  154.1478168964386  seconds.



#################################################
#4a
GeoCount = print(cursor.execute("SELECT COUNT(*) FROM Geo;").fetchall()) #11849

GeoValues = cursor.execute("SELECT GeoID, type, ROUND(longitude,4), ROUND(latitude,4) FROM Geo;").fetchall()

Geofile = codecs.open('Geofile.txt','w','utf-8')

Geofile.write('Unknown')
Geofile.write("|")
Geofile.write('Unknown')
Geofile.write("|")
Geofile.write('Unknown')
Geofile.write("|")
Geofile.write('Unknown')
Geofile.write('\n')



for entry in GeoValues:
    Geofile.write(entry[0])
    Geofile.write("|")
    Geofile.write(entry[1])
    Geofile.write("|")
    Geofile.write(str(entry[2]))
    Geofile.write("|")
    Geofile.write(str(entry[3]))
    Geofile.write("|")


Geofile.close()


#4b
TweetsCount = print(cursor.execute("SELECT COUNT(*) FROM Tweets;").fetchall()) #499776

TweetsValues = cursor.execute("SELECT * FROM Tweets;").fetchall()

Tweetsfile = codecs.open('Tweetsfile.txt','w','utf-8')

for entry in TweetsValues:
    Tweetsfile.write(entry[0])
    Tweetsfile.write("|")
    Tweetsfile.write(entry[1])
    Tweetsfile.write("|")
    Tweetsfile.write(entry[2])
    Tweetsfile.write("|")
    Tweetsfile.write(entry[3])
    Tweetsfile.write("|")
    Tweetsfile.write(str(entry[4]))
    Tweetsfile.write("|")
    Tweetsfile.write(str(entry[5]))
    Tweetsfile.write("|")
    Tweetsfile.write(str(entry[6]))
    Tweetsfile.write("|")
    Tweetsfile.write(str(entry[7]))
    Tweetsfile.write("|")
    Tweetsfile.write(str(entry[8]))
    Tweetsfile.write("|")
    Tweetsfile.write(str(entry[9]))
    Tweetsfile.write("|")
    if entry[10] == 'None':
        Tweetsfile.write('Unknown')
    else:
        Tweetsfile.write(entry[10])
    Tweetsfile.write('\n')

Tweetsfile.close()


#4c
UsersCount = print(cursor.execute("SELECT COUNT(*) FROM Users;").fetchall()) #447299

UsersValues = cursor.execute("SELECT * FROM Users;").fetchall()

UsersValues = UsersValues[0:5]
print(UsersValues)

Usersfile = codecs.open('Usersfile.txt','w','utf-8')


for entry in UsersValues:
    Usersfile.write("\n")
    Usersfile.write(str(entry[0]))
    Usersfile.write("|")
    Usersfile.write(entry[1])
    Usersfile.write("|")
    Usersfile.write(entry[2])
    Usersfile.write("|")
    Usersfile.write(entry[3])
    Usersfile.write("|")
    Usersfile.write(str(entry[4]))
    Usersfile.write("|")
    if entry[1] in entry[2] or entry[1] in entry[3]:
        Usersfile.write('True')
    else:
        Usersfile.write('False')
    Usersfile.write("\n")

Usersfile.close()

#Extra Credit
#I found that loading from local files takes significantly less time than loading 
#data directly from a website. Also data loading/manipulation does not necessarily 
#scale lineraly with the amount being loaded (i.e. 10x data may take 5x as long).
#I also found that batching can speed up loading to Sql by a moderate amount.