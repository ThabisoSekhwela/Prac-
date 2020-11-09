import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import threading
import datetime
import RPi.GPIO as GPIO
at_end = None
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

sample_rate = 10.0
def start_part():
 
    pass
            # call the threading function
    
def callback_method(channel):   
    pass

def setup_func():
    
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(11, GPIO.RISING, callback=callback_method,bouncetime=295)
    pass
    
def ADC_func():

    
    thread = threading.Timer(sample_rate,ADC_func) # 10 , changes the sampling time 
    thread.daemon = True  # Daemon threads exit when the program does
    thread.start()
 
    
    final = datetime.datetime.now()
    #if (datetime.datetime.now()) == sample_rate:
    print(str(final.second - start.second) + "V" + "     " + str(chan.value)+"      "+str((chan.voltage - V_0C)/TC))
    
    if (final.second - start.second) > sample_rate*6:
        break
    #if (datetime.datetime.now()) == 2*sample_rate:
    #    print(str(datetime.datetime.now()) + "V" + "     " + str(chan.value)+"      "+str((chan.voltage - V_0C)/TC))
    #       
   # if (datetime.datetime.now()) == 3*sample_rate:
    #    print(str(datetime.datetime.now()) + "V" + "     " + str(chan.value)+"      "+str((chan.voltage - V_0C)/TC))
   #
    #   print(str(datetime.datetime.now()) + "V" + "     " + str(chan.value)+"      "+str((chan.voltage - V_0C)/TC))
   
    #if (datetime.datetime.now()) == 5*sample_rate:
     #   print(str(datetime.datetime.now()) + "V" + "     " + str(chan.value)+"      "+str((chan.voltage - V_0C)/TC))
   #
    #if (datetime.datetime.now()) == 5*sample_rate:
     #   print(str(datetime.datetime.now()) + "V" + "     " + str(chan.value)+"      "+str((chan.voltage - V_0C)/TC))
 
    #if (datetime.datetime.now()) == 6*sample_rate:
     #   print(str(datetime.datetime.now()) + "V" + "     " + str(chan.value)+"      "+str((chan.voltage - V_0C)/TC))
   
    #print("Raw ADC Value: ", chan.value)
    #print("ADC Voltage: " + str(chan.voltage) + "V")
    # formula to convert to Temperature
    #temp_value = (chan.voltage - V_0C)/TC
    #print("Temperature: ", temp_value)
       
    # final print statemnet 
    pass


if __name__ == "__main__":
    try:
        # Call setup function
        setup_func()
        sample_rate =10.0
        while True:
            print("start")
            global start
           # global sample_rate
            
            
            if GPIO.input(11) == False:
                #global sample_rate
                if sample_rate == 1.0:
                    sample_rate = 10.0
                else:
                    sample_rate = sample_rate - 5.0
                    if sample_rate == 0.0:
                        sample_rate = 1.0
            print("Sample rate",sample_rate)
            start = datetime.datetime.now()
            ADC_func()
            pass
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
