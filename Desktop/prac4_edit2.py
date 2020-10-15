
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
    global p
    global ledDim
    ledDim = GPIO.PWM(32,10)
    ledDim.start(0)
    p = GPIO.PWM(33,10)  
    p.start(1)  #Duty circle of brackets
    
    # Setup debouncing and callbacks
    GPIO.add_event_detect(18, GPIO.RISING, callback=callback_method,bouncetime=300)
    GPIO.add_event_detect(16, GPIO.RISING, callback=callback_method,bouncetime=300)
    pass


# Load high scores
def fetch_scores():
    # get however many scores there are
    eeprom.populate_mock_scores()
    global score_count
    score_count = eeprom.read_byte(0)
    

    # Get the scores
    #Byt_arr = eeprom.read_byte(1,4*number_S)
    
    print(score_count)
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
    #new_arr = []
    number_S, new_arr = fetch_scores()
    number_S = number_S + 1
    # include new score
    new_arr.append(["name",0])
    new_arr[number_S-1][0] = username
    new_arr[number_S-1][1] = attempts
    #print(new_arr)
    # sort
    new_arr.sort(key=lambda x: x[1])

    # update total amount of scores
    #score_count = number_S
    

    # write new scores
    new_arr_write = []

    eeprom.write_byte(0,number_S)
    for content in new_arr:
          for y in content[0]:
                new_arr_write.append(ord(y))
                new_arr_write.append(content[1])
          eeprom.write_block(1, new_arr_write)
    print(new_arr_write)
    
   # eeprom.write_block(0, number_S) # count number of scores in first block
    pass


# Generate guess number
def generate_number():
    return random.randint(0, pow(2, 3)-1)
    

# Increase button pressed

def btn_increase_pressed(channel):
    global guess
    
    print("The guess is",guess)
    if guess == 7:
        guess = 0 # restart the count from zero
    # Increase the value shown on the LEDs   
    # You can choose to have a global variable store the user's current guess, 
    # or just pull the value off the LEDs when a user makes a guess
    guess += 1
    led_Switch()
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
    print("Here in guess after submit")
    start_time = time.time()
    buttonTime = time.time() - start_time
    if buttonTime < 1: 
       # count number of attempts
        global attempts
        attempts = attempts + 1
        print("Counting number of attempts")
    
        accuracy_leds()
        # Compare the actual value with the user value displayed on the LEDs
        # if it's close enough, adjust the buzzer
        
        if guess == value:
            print("guess = value")
            p.stop()
            GPIO.output(32, False)
            GPIO.output(33, False)
            save_scores()
            menu()
        else:
            print("In Buzzer")
            trigger_buzzer()
        
        # Change the PWM LED
        
        # if it's an exact guess:
        # - Disable LEDs and Buzzer
        print("skipped guess = value")
            
    else:# when button pressed for more than 1 sec
        print("Holding State")
        end_of_game = True # stops the games
        GPIO.output(32, False)
        GPIO.output(33, False)
        
    # - tell the user and prompt them for a name
    #  name  = input("Enter your name:")
    # - fetch all the scores
    # - add the new score
    # - sort the scores
    # - Store the scores back to the EEPROM, being sure to update the score count
    pass


# LED Brightness
def accuracy_leds():
    # Set the brightness of the LED based on how close the guess is to the answer
    # - The % brightness should be directly proportional to the % "closeness"
    # - For example if the answer is 6 and a user guesses 4, the brightness should be at 4/6*100 = 66%
    # - If they guessed 7, the brightness would be at ((8-7)/(8-6)*100 = 50%
    led_inp = (8-guess)/(8-value)*100
    ledDim.ChangeDutyCycle(led_inp)
    GPIO.output(32, True)
    print("In accurate led changing duty circle")
    pass

# Sound Buzzer
def trigger_buzzer():
    # The buzzer operates differently from the LED
    # While we want the brightness of the LED to change(duty cycle), we want the frequency of the buzzer to change
    # The buzzer duty cycle should be left at 50%
     
    # p.start(0)
    # p.ChangeDutyCycle(dc)
    
    if abs(value-guess)==3:
    # If the user is off by an absolute value of 3, the buzzer should sound once every second     
       #GPIO.PWM(33,10).start(1)
       p.ChangeFrequency(1)
       GPIO.output(33, True)
       #p.stop()
    
    if abs(value-guess)==2:
    # If the user is off by an absolute value of 2, the buzzer should sound twice every second
       #GPIO.PWM(33,10).start(1)
       p.ChangeFrequency(2)
       GPIO.output(33, True)
       #p.stop()

    if abs(value-guess)==1:
    # If the user is off by an absolute value of 1, the buzzer should sound 4 times a second
       #GPIO.PWM(33,10).start(1)
       p.ChangeFrequency(4)
       GPIO.output(33, True)
       #p.stop()
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
