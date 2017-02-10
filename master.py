import serial, time
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
                print BLwrite("AT+INQM=1,1,5")
                print BLwrite("AT+INIT")
                print BLwrite("AT+INQ")

def parseInq(inq):
	inq = inq[ inq.find(":")+1 : inq.find(",") ]
        inq = inq.replace(":","")
	return inq


def addToList(mac):
	found = 0
	for item in macList:
		if mac in item:
			found = 1
			break
	if found is 0:
		macList.append(mac)

def printList():
	print "LIST ON"
	for item in macList:
		print item
	print "LIST OFF"

def main():
	setPin()
	openBL()
	print BLwrite("AT")
	startInq()

	while 1:
		res = BLread()
		time.sleep(0.1)
		if "OK\r" in res :
			printList()
			BLwrite("AT+INQ")
		else :
			if "+INQ" in res:
				res = parseInq(res)
				print res
				addToList(res)
#        print BLwrite("AT+INQC")
	BLser.close()
	gpio.digitalWrite(1,0)

macList = []
main()
