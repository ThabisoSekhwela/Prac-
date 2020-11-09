import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import threading
import datetime
import time
import RPi.GPIO as GPIO
#import OPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)
chan = AnalogIn(mcp, MCP.P1)
at_end = None
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_UP)


    

# constants
V_0C = 0.5# in V
TC = 0.01# mV/Degree_Celcius

sample_rate = 10.0

def setup():    
    GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(17, GPIO.RISING, callback=callback_method, bouncetime=200)
    mcp = MCP.MCP3008(spi, cs)
    chan = AnalogIn(mcp, MCP.P1)

def callback_method(channel):
    global sample_rate
    print("in callback")
    global start
    
    #if GPIO.event_detected(17):
    print("event detect")   
    global sample_rate
    sample = sample_rate
        # change sampling rate
    if sample_rate == 1.0:
        sample_rate = 10.0
    else:
        sample_rate = sample_rate - 5.0
        if sample_rate == 0.0:
            sample_rate = 1.0  
    print("before start")
    
    #ADC_func()
    pass

    
def ADC_func():
    #GPIO.wait_for_edge(11, GPIO.RISING)
    #global start
    
    #callback_method()
    print("in ADC")
    global sample_rate
    
    thread = threading.Timer(sample_rate,ADC_func) # 10 , changes the sampling time 
    thread.daemon = True  # Daemon threads exit when the program does
    thread.start()  
    final = datetime.datetime.now()
        #if (datetime.datetime.now()) == sample_rate:
    
    print(str(final.second - start.second) + "s" + "     " + str(chan.value)+"      "+str((chan.voltage - V_0C)/TC))
    #if GPIO.event_detected(17):
        #callback_method(17)
      #  print("In callbacl")
    
    
  
    print("im here")
    #else:
    #    pass
        


    

if __name__ == "__main__":
    
 
    
    setup()
            #GPIO.add_event_detect(11, GPIO.RISING)
    print("Runtime       Temp      Reading Temp")       
    global start
    #callback_method(sample_rate)
    start = datetime.datetime.now()
    ADC_func()   
    while 1:
        
        pass
    
  
    
    
  
