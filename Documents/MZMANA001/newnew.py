import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import RPi.GPIO as GPIO
import datetime
import time

#Setup GPIO
GPIO.setmode(GPIO.BCM)
buttonPin = 17 # use pin 17 as pushbutton; add event listener on pin 17
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
begin = datetime.datetime.now()
# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D24)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

#Delay factor
delayFactor = [5000, 2900, 1555]      #5000 for 10 second delay; 2900 for 5 second delay; and 1550 for 1 second delay
timeDelay = [10,5,1]


def Thread():

    # create an analog input channel on pin1 which is channel_0
    chan = AnalogIn(mcp, MCP.P0)
    end = datetime.datetime.now()
    print(end.second())
    print(format(str(timeDelay[3-len(delayFactor)])+'s','<15'), format(str(chan.value),'<15'),str((chan.voltage-0.5)/0.01)+' °C', sep='')


    for i in range(delayFactor[0]):
        for j in range(delayFactor[0]):
            #
            pass

def button_Callback(channel):
    global delayFactor
    if len(delayFactor)>0:
        delayFactor.pop(0)
    if len(delayFactor)==0:
        delayFactor = [5000, 2900, 1555]

GPIO.add_event_detect(buttonPin, GPIO.FALLING, callback=button_Callback, bouncetime=200)

if __name__ == "__main__":
    print(format("Runtime",'<15'),format("Temp Reading", '<15'),"Temp", sep='')
    Thread()
        
    while True:
        pass
        
   

