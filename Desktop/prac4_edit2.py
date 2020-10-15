
# Import libraries
import RPi.GPIO as GPIO
import random
from time import sleep
import time
import ES2EEPROMUtils
import os

# some global variables that need to change as we run the program
end_of_game = None # set if the user wins or ends the game

# DEFINE THE PINS USED HERE
LED_value = [11, 13, 15]
LED_accuracy = 32
btn_submit = 16
btn_increase = 18
guess = 0
buzzer = None
attempts = 0
value = 0
eeprom = ES2EEPROMUtils.ES2EEPROM()
increaseButton = False
submitButton = False
attempts = 0
number_S =0

def callback_method(channel):
       print("edge detected")


# Print the game banner
def welcome():
    os.system('clear')
    print("  _   _                 _                  _____ _            __  __ _")
    print("| \ | |               | |                / ____| |          / _|/ _| |")
    print("|  \| |_   _ _ __ ___ | |__   ___ _ __  | (___ | |__  _   _| |_| |_| | ___ ")
    print("| . ` | | | | '_ ` _ \| '_ \ / _ \ '__|  \___ \| '_ \| | | |  _|  _| |/ _ \\")
    print("| |\  | |_| | | | | | | |_) |  __/ |     ____) | | | | |_| | | | | | |  __/")
    print("|_| \_|\__,_|_| |_| |_|_.__/ \___|_|    |_____/|_| |_|\__,_|_| |_| |_|\___|")
    print("")
    print("Guess the number and immortalise your name in the High Score Hall of Fame!")


# Print the game menu
def menu():
    global end_of_game
    option = input("Select an option:   H - View High Scores     P - Play Game       Q - Quit\n")
    option = option.upper()
    if option == "H":
        os.system('clear')
        print("HIGH SCORES!!")
        s_count, ss = fetch_scores()
        display_scores(s_count, ss)
    elif option == "P":
        os.system('clear')
        print("Starting a new round!")
        print("Use the buttons on the Pi to make and submit your guess!")
        print("Press and hold the guess button to cancel your game")
        global value
        value = generate_number()
        #value = 1
        print("The value is",value)
        while not end_of_game:
            # creating increase and submit pushbuttons
            increaseButton = GPIO.input(btn_increase)
            submitButton = GPIO.input(btn_submit)
            #print("Here")
            if increaseButton == False:
                print("increase button")
                btn_increase_pressed(18)
                sleep(1)
            if submitButton == False:
                btn_guess_pressed(16)
                print("Submit button")
                sleep(1)
            # the buzzer and LEDs are turned
                    
        if end_of_game == True:
            menu() 

            pass
    elif option == "Q":
        print("Come back soon!")
        exit()
    else:
        print("Invalid option. Please select a valid one!")


def display_scores(count, raw_data):
    # print the scores to the screen in the expected format
    print("There are {} scores. Here are the top 3!".format(count))
    # print out the scores in the required format
    pass


# Setup Pins
def setup():
    global Buzzer_sound , ledDim
    # Setup board mode
    GPIO.setmode(GPIO.BOARD)

    # Setup regular GPIO
    GPIO.setup(11, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(15, GPIO.OUT)
    GPIO.setup(32, GPIO.OUT)
    GPIO.setup(16, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(33, GPIO.OUT) # PWM pin

    # Setup PWM channels   
    ledDim = GPIO.PWM(32,10)
    ledDim.start(0)
    
    Buzzer_sound = GPIO.PWM(33,10)  
    Buzzer_sound.start(50)  
    
    # Setup debouncing and callbacks
    GPIO.add_event_detect(18, GPIO.RISING, callback=callback_method,bouncetime=295)
    GPIO.add_event_detect(16, GPIO.RISING, callback=callback_method,bouncetime=295)
    pass


# Load high scores
def fetch_scores():
    # get however many scores there are
    #eeprom.populate_mock_scores()
    global score_count
    global score
    score_count = eeprom.read_byte(0)
    

    scores = []
    for i in range(score_count):           
        scores.append(['name',0])        
        strr = ""
        for j in range(3):  # storing letters            
            print("j = ",j)
            strr = strr + chr(eeprom.read_byte(4 + i*4 + j))
            print(strr)
        scores[i][0] = strr
        #print(scores)
         # storing score
        scores[i][1] = eeprom.read_byte((i*4+3)+4)
        print(scores)
    
    


    # convert the codes back to ascii
    # converted on method above

    # return back the results
    return score_count, scores






# Save high scores
def save_scores():
 
    username  = input("Enter your name:")
    if len(username) > 3:
       username = username[:3]
    
    # fetch scores
    
    score_count, new_arr = fetch_scores()
    score_count = score_count + 1
    
    # include new score
    new_arr.append(["name",0])
    new_arr[score_count-1][0] = username
    new_arr[score_count-1][1] = attempts
    
    # sort
    new_arr.sort(key=lambda x: x[1])
    print(new_arr)
    
    # write new scores
    # update total amount of scores
    new_arr_write = []

    eeprom.write_byte(0,score_count)
    for content in new_arr:
          for y in content[0]:
                new_arr_write.append(ord(y))
          new_arr_write.append(content[1])
          eeprom.write_block(1, new_arr_write)
    
    pass


# Generate guess number
def generate_number():
    return random.randint(0, pow(2, 3)-1)
    

# Increase button pressed

def btn_increase_pressed(channel):
    global guess
    global attempts
   
        
    # Increase the value shown on the LEDs   
    # You can choose to have a global variable store the user's current guess, 
    # or just pull the value off the LEDs when a user makes a guess    
    attempts = attempts + 1
    led_Switch()
    guess += 1
    if guess == 8:
        guess = 0
    pass

def led_Switch():
    if guess == 0:
        GPIO.output(11, False)
        GPIO.output(13, False)
        GPIO.output(15, False)
    elif guess == 1:
        GPIO.output(11, False)
        GPIO.output(13, False)
        GPIO.output(15, True)
    elif guess == 2:        
        GPIO.output(11, False)
        GPIO.output(13, True)
        GPIO.output(15, False)
    elif guess == 3:
        GPIO.output(11, False)
        GPIO.output(13, True)
        GPIO.output(15, True)
    elif guess == 4:
        GPIO.output(11, True)
        GPIO.output(13, False)
        GPIO.output(15, False)
    elif guess == 5:
        GPIO.output(11, True)
        GPIO.output(13, False)
        GPIO.output(15, True)
    elif guess == 6:       
        GPIO.output(11, True)
        GPIO.output(13, True)
        GPIO.output(15, False)
    elif guess == 7:
        GPIO.output(11, True)
        GPIO.output(13, True)
        GPIO.output(15, True)
    pass
# Guess button
def btn_guess_pressed(channel):
    # If they've pressed and held the button, clear up the GPIO and take them back to the menu screen
    start_time = time.time()
    buttonTime = time.time() - start_time
    print(buttonTime)
    if buttonTime < 1: 
       # count number of attempts
        #global attempts
        
    
        accuracy_leds()
        # Compare the actual value with the user value displayed on the LEDs
        # if it's close enough, adjust the buzzer
        
        print("Guess before ===", guess)
        if guess == value:
            ledDim.stop()
            Buzzer_sound.stop()
            GPIO.output(32, False)
            GPIO.output(33, False)
            save_scores()
            
        else:
            
            trigger_buzzer()
        
        # Change the PWM LED
        
        # if it's an exact guess:
        # - Disable LEDs and Buzzer
        
          
    else:# when button pressed for more than 1 sec
        
        end_of_game = True # stops the games
        GPIO.output(32, False)
        GPIO.output(33, False)
        
    # - tell the user and prompt them for a name
    # - fetch all the scores
    # - add the new score
    # - sort the scores
    # - Store the scores back to the EEPROM, being sure to update the score count
    pass


# LED Brightness
def accuracy_leds():
    # Set the brightness of the LED based on how close the guess is to the answer
    
    led_inp = (8-guess)/(8-value)*100
    if (8-guess)>(8-value):
        led_inp = 15
        
    ledDim.ChangeDutyCycle(led_inp)
    GPIO.output(32, True)
    pass

# Sound Buzzer
def trigger_buzzer():
    
    if abs(value-guess)==3:
    # If the user is off by an absolute value of 3, the buzzer should sound once every second     
       Buzzer_sound.ChangeFrequency(1)
       GPIO.output(33, True)
       
    
    if abs(value-guess)==2:
    # If the user is off by an absolute value of 2, the buzzer should sound twice every second
       Buzzer_sound.ChangeFrequency(2)
       GPIO.output(33, True)
       

    if abs(value-guess)==1:
    # If the user is off by an absolute value of 1, the buzzer should sound 4 times a second
       Buzzer_sound.ChangeFrequency(4)
       GPIO.output(33, True)
       
    else:
        pass
    pass


if __name__ == "__main__":
    try:
        # Call setup function
        setup()
        welcome()
        while True:
            menu()
            pass
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
