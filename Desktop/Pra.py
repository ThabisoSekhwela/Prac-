import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import threading
import datetime
import time
import RPi.GPIO as GPIO
import ES2EEPROMUtils
import os
EEP = ES2EEPROMUtils.ES2EEPROM()
#import OPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)
chan = AnalogIn(mcp, MCP.P1)
at_end = None
sec = 0
minute = 00
hour = 00
pos = 0
var = 0  

# constants
V_0C = 0.5# in V
TC = 0.01# mV/Degree_Celcius

sample_rate = 5
state = False

def setup():
    global Buzzer_sound
    GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(17, GPIO.RISING, callback=callback_method, bouncetime=200)
    mcp = MCP.MCP3008(spi, cs)
    chan = AnalogIn(mcp, MCP.P1)
    #GPIO.setup(13, GPIO.OUT) 
    #Buzzer_sound = GPIO.PWM(13,10)
 
#def savetoEEP():
def fetch_data():   
    j = 0
    f = 1
    dataitem = []
    for i in range(20):                   
        strr1 = ""
        strr2 = ""
        for x in range(4):  # storing letters            
            
            strr1 = strr1 + str(EEP.read_byte((i+j)*4 + x))
            strr2 = strr2 + str(EEP.read_byte((i+f)*4 + x))
        dataitem.append(strr1 + strr2)
        j = j + 1
        f = f + 1
    return dataitem

def save_data(new_arr):    
    print("data) store")
    # 40 blocks
    for i in range(40):
        for j in range(4):
            new_arr_write = int(new_arr[i][j])
            EEP.write_byte(4*i+j, new_arr_write)
    print("done storing")
    pass

       
#arr = ["17301650"]*20
def store(data):
    global pos
    arr[pos] = data
    pos = pos + 1
    if pos == 20:
        pos = 0
    pass

# break HHHMMSSTT data to HHMM and SSTT
store_arr = ["KKKK"]*40
def break_func():
    
    # store odd position
    j = 0
    k = 0    
    for i in range(len(arr)):        
        v = i + j
        store_arr[v] = arr[i][:4]
        j = j + 1
    
    
    # store even postion
    f = 1
    for i in range(len(arr)):
        v = i + f
        store_arr[v] = arr[i][4:]
        f = f + 1
    save_data(store_arr)
    
    

def callback_method(channel):
    
    
    # changong the button state
    global arr
    print("event detect")   
    global state
    global sec
    
    if state == True:
        print("False")
        state = False
        sec = 0
        print(arr)
        print("Break dwon func")
        break_func()
    elif state == False:
        
        print("True")
        arr = fetch_data()
        state = True
   
    
    pass

    
def ADC_func():
    
    print("in ADC")
    global thread,final
    global sec, minute , hour
    
    thread = threading.Timer(sample_rate,ADC_func) # 10 , changes the sampling time 
    thread.daemon = True  # Daemon threads exit when the program does
    thread.start()  
    
    if GPIO.input(17) == state:
        
      
       
        final = datetime.datetime.now()
        time_now = str(final)[11:]
        time_now = time_now[:8]
        
        sec_p = str(sec)
        if len(str(sec))==len('0'):
            sec_p = ('0'+str(sec))
        
        minute_p = str(minute)
        if len(str(minute))==len('0'):
            minute_p = ( '0'+str(minute))
        
        hour_p = str(hour)
        if len(str(hour))==len('0'):
            hour_p = ('0'+str(hour))
        
        temp = str(round((chan.voltage - V_0C)/TC))
        
        temp_sign = 1
        if len(temp)==len('ooo'):
            temp_sign = -1
            temp = temp[1:]
            
            
        store(time_now[:2]+time_now[3:5]+time_now[6:8]+temp)
        
        
        print(str(time_now)  + "   " +str(hour_p)+":"+str(minute_p)+":"+str(sec_p)+"   "+ temp+'C')
        sec = sec + 5
        
        if sec == 60:
            minute = minute + 1
            sec = 0
        if minute == 60:
            hour = hour + 1
            minute = 0
    

if __name__ == "__main__":
        
    setup()
         
    global start
    
    #y = fetch_data()
    #print(y)
    
    start = datetime.datetime.now()
    ADC_func()
    #fetch_scores()
    while 1:
        
        pass
    
  
    
    
  



