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

def main():
	setPin()
	openBL()
	print BLwrite("AT")
	res = BLwrite("AT+STATE?")
	print res
	if "INQUIRING" not in res:
		print BLwrite("AT+ROLE=1")
		print BLwrite("AT+INQM=1,1,5")
        	print BLwrite("AT+INIT")
		print BLwrite("AT+INQ")

	while 1:
		res = BLread()
		time.sleep(0.1)
		if "OK\r" in res :
			BLwrite("AT+INQ")
		else :
			if "+INQ" in res:
				print res
#        print BLwrite("AT+INQC")
	BLser.close()
	gpio.digitalWrite(1,0)

main()
