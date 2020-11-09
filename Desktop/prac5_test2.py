import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import threading
import datetime

at_end = None
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_UP)

sample_rate = 10
# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)
# create the mcp object
mcp = MCP.MCP3008(spi, cs)
# create an analog input channel on pin 0
chan = AnalogIn(mcp, MCP.P1)
    
    

# constants
V_0C = 0.5# in V
TC = 0.01# mV/Degree_Celcius

#sample_rate = 1

    
def callback_method(channel):  
    
    # change sampling rate
    if sample_rate == 1.0:
        sample_rate = 10.0
    else:
        sample_rate = sample_rate - 5.0
        if sample_rate == 0.0:
            sample_rate = 1.0
    start = datetime.datetime.now()
    ADC_func()
    
    pass

    
def ADC_func():
    
    global sample_rate    
    thread = threading.Timer(sample_rate,ADC_func) # 10 , changes the sampling time 
    thread.daemon = True  # Daemon threads exit when the program does
    thread.start()
 
    
    final = datetime.datetime.now()
    #if (datetime.datetime.now()) == sample_rate:
    print(str(final.second - start.second) + "s" + "     " + str(chan.value)+"      "+str((chan.voltage - V_0C)/TC))
     
    pass


if __name__ == "__main__":
    start = datetime.datetime.now()
    print("Runtime       Temp      Reading Temp")
    ADC_func()
            
  