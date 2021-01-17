import datetime
import time
import atexit
from decimal import *

getcontext().prec = 15
start = datetime.datetime.now()
time.sleep(5)

delta = (datetime.datetime.now()-start).total_seconds()


#read old total
with open("uptime.txt",'r') as file:
    olduptime = file.readline()
    print(olduptime)

#add old total to current uptime
newuptime = round(Decimal(delta)) + round(Decimal(olduptime))

#write new uptime to file
def updateuptime():
    with open("uptime.txt", "w") as outfile:
        #print(str(newuptime))
        outfile.write(str(newuptime))
        #print(datetime.timedelta(seconds=newuptime))
atexit.register(updateuptime)