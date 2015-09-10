# Sample Program: Hello with counter and history!
# Original code sourced from fork of:
#    https://github.com/mcowger/hello-python
# Because the program always exits at the 'return' You
# are forced to store values you want to keep (like a counter)
# in some sort of external structure
# (unless you want self-modifying code) (yikes!)
# So since a flat file was already done by somebody else
# I decided to do something different and perhaps add in
# an extra feature in the process...
# (yes, what I added could also have been done in a flat file),
# but this was more fun to play with the ever insecure 'pickle'..
# ~ LeeMikeS    2015-09-09, Ver. 0.12
#
# Some helpful tutorials:
#   https://docs.python.org/2/library/pickle.html#usage
#   https://wiki.python.org/moin/UsingPickle
#   http://www.tutorialspoint.com/python/python_date_time.htm
#   http://showmedo.com/videotutorials/series?name=inivcfz5b
#   http://effbot.org/zone/python-list.htm

import os
import uuid
from flask import Flask
from flask import request   # So can request remote ip
import pickle               # The pickle database
import time                 # So I can get current date/time


app = Flask(__name__)
my_uuid = str(uuid.uuid1())

filename = "pickle.db"

BLUE = "#0099FF"
GREEN = "#33CC33"
TEAL = "#008080"

COLOR = TEAL

def get_ip():
    return request.remote_addr

def get_record():
        if os.path.exists(filename):
            # Open the database file for reading
            fileObject = open(filename, 'r+')
            # load the list from the file into var mydata
            therecord = pickle.load(fileObject)
            # close the file
            fileObject.close()
        else:
            therecord = [str(0),"Beginning of Time and Space","0.0.0.0"]
        return therecord
def put_record(newhitcount,newlocaltime,fromip):
    # update the database with the new info
    newrecord = [str(newhitcount),str(newlocaltime),str(fromip)]
    # Open the database file for writing
    fileObject = open(filename, 'wb')
    # load the list from the file into var mydata
    mydata = pickle.dump(newrecord,fileObject)
    # close the file
    fileObject.close()

@app.route('/')

def hello():
    localtime = time.asctime( time.localtime(time.time()) )

    yourip = get_ip()

    mydata = get_record()
    # read back the prev. hitcount (first item in the list)
    hitcount = int(mydata[0])
    # read back the prev. hitdate (second item in list)
    oldhitdate = str(mydata[1])
    # read back the prev. GUID (second item in list)
    remoteip = str(mydata[2])

    hitcount += 1

    put_record(hitcount,localtime,yourip)

    return """
    <html>
    <body bgcolor="{}">

    <center><h1><font color="blue">Your App Instance GUID is:<br/>
    {}</br>
    from: {}</br>

    <center><font color="red">Page Hit Count is now:
    {}</br>

    <center><font color="red">on:
    {} GMT</br>

    <center><font color="purple">The last time this page was hit was on:<br/>
    {} GMT</br>

    </center>

    </body>
    </html>
    """.format(COLOR,my_uuid,remoteip,hitcount,localtime,oldhitdate)

if __name__ == "__main__":
	app.run(debug=True,host='0.0.0.0',
    port=int(os.getenv('VCAP_APP_PORT', '5000'))
    )
