#!/usr/bin/env python

import sqlite3, time
from datetime import time as dttime
from datetime import datetime

def showDB():
	print "Showing DB Entries"
	global curs
	for row in curs.execute("SELECT * FROM BTmac"):
		print row

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
	addToDB("Hello2")
	showDB()

main()

#t = datetime.now()
#print t.hour print t.minute print t.second
#t2 = dttime(5,22,0)
#print t2 - t
#datetime(2017,4,22,05,12,36)
