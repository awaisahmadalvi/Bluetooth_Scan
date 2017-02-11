#!/usr/bin/env python

import serial, time, sqlite3
import wiringpi2 as gpio

def BLwrite(str):
        BLser.write(str+"\r\n")
	time.sleep(0.5)
	return BLread()

def BLread():
	return BLser.readline()

def setPin():
	gpio.wiringPiSetup()

	gpio.pinMode(1,1)

	gpio.digitalWrite(1,0)
	time.sleep(0.3)
	gpio.digitalWrite(1,1)


def openBL():
	try:
		global BLser 
		BLser = serial.Serial(port="/dev/ttyS1",
                                    baudrate=38400,
                                    timeout=0.01,
                                    bytesize=serial.EIGHTBITS,
                                    parity=serial.PARITY_NONE,
                                    stopbits=serial.STOPBITS_ONE,
                                    xonxoff=False,
                                    rtscts=False,
                                    dsrdtr=False)
	except serial.serialutil.SerialException:
		print("Unable to open port '%s'\r" % port)

def startInq():
	res = BLwrite("AT+STATE?")
        print res
        if "INQUIRING" not in res:
                print BLwrite("AT+ROLE=1")
                print BLwrite("AT+INQM=1,10,48")
                print BLwrite("AT+INIT")
                print BLwrite("AT+INQ")

def parseInq(inq):
	inq = inq[ inq.find(":")+1 : inq.find(",") ]
        inq = inq.replace(":","")
	return inq

def addToDB(mac):
        global curs
        found = 0
        for row in curs.execute("SELECT * FROM BTmac WHERE tdate > datetime('now', '-5 seconds') AND mac=(?)", (mac,)):
                found = 1
                curs.execute("UPDATE BTmac SET tdate=datetime('now'), mac=(?) WHERE tdate=?", (mac,row[0]))
                db.commit()
                print "found"
                print row
                break
        if found is 0:
                print "not found"
                curs.execute("INSERT INTO BTmac values(datetime('now'), (?))", (mac,))
                found = 0
                db.commit()

def showDB():
	print "Showing DB Entries"
	global curs
	for row in curs.execute("SELECT * FROM BTmac"):
		print row


def createDBtable():
	global curs
	curs.execute("CREATE TABLE IF NOT EXISTS BTmac (tdate DATETIME, mac TEXT);")

def connectDB():
	global db
	db=sqlite3.connect('busesMac.db')
	global curs
	curs=db.cursor()

def main():

	connectDB()
	createDBtable()

	setPin()
	openBL()
	print BLwrite("AT")
	startInq()

	while 1:
		res = BLread()
		time.sleep(0.1)
		if "OK\r" in res :
			showDB()
			BLwrite("AT+INQ")
		else :
			if "+INQ" in res:
				res = parseInq(res)
				print res
				addToDB(res)
#        print BLwrite("AT+INQC")
	BLser.close()
	gpio.digitalWrite(1,0)

macList = []
main()
#connectDB()
#createDBtable()
#showDB()
#t = time.localtime(time.time())
##print t
##t2 = time.localtime(time.time()+2)
#print t2
#print t2 - t
