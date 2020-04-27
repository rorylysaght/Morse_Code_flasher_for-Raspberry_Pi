# ######
#	Web Interface for Raspberry Pi 4 GPIO Control
#    By Rory MacLysaght, rorylysaght@gmail.com
# ######
import RPi.GPIO as GPIO
from flask import Flask, render_template, request
import time
app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# this is the GPIO pin we will Flash
# edit as necessary for your board
pinOut = 21
# connect this to relay to flash higher-wattage lamp

GPIO.setup(pinOut, GPIO.OUT)

@app.route("/")
def action():
     msg = request.args.get('msg')
     msg = msg.upper() # Morse Code ignores case, so make everything uppercase
     print(msg)
     morse = encrypt(msg)
     for i in(morse):
          if i == '.':
               GPIO.output(pinOut, GPIO.HIGH)
               time.sleep(.3)
               GPIO.output(pinOut, GPIO.LOW)
               time.sleep(.2)
          elif i == '-':
               GPIO.output(pinOut, GPIO.HIGH)
               time.sleep(.6)
               GPIO.output(pinOut, GPIO.LOW)
               time.sleep(.2)
          elif i == ' ':
               GPIO.output(pinOut, GPIO.LOW)
               time.sleep(.6)

     return render_template('index.html',original=msg,morse=morse,keys=keys,values=values)


# Encrypt the string according to morse code dictionary below
def encrypt(message):
    cipher = ''
    message_cleaned = message
    # first scrub non-allowed characters
    # also do this initially in Javascript on the page
    for letter in message:
        if letter not in MORSE_CODE_DICT.keys():
             message_cleaned = message.replace(letter,'')
             print("Illegal char: " + letter)

    for letter in message_cleaned:
        if letter != ' ':
            # Looks up the dictionary and adds the
            # correspponding morse code
            # along with a space to separate
            # morse codes for different characters
            cipher += MORSE_CODE_DICT[letter] + ' '
        else:
            # 1 space indicates different characters
            # and 2 indicates different words
            cipher += '  '

    return cipher

# Dictionary representing the morse code chart
MORSE_CODE_DICT = { 'A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.',
'F':'..-.', 'G':'--.', 'H':'....', 'I':'..', 'J':'.---', 'K':'-.-', 'L':'.-..',
'M':'--', 'N':'-.', 'O':'---', 'P':'.--.', 'Q':'--.-', 'R':'.-.', 'S':'...',
'T':'-', 'U':'..-', 'V':'...-', 'W':'.--', 'X':'-..-', 'Y':'-.--', 'Z':'--..',
'1':'.----', '2':'..---', '3':'...--', '4':'....-', '5':'.....', '6':'-....',
'7':'--...', '8':'---..', '9':'----.', '0':'-----', ', ':'--..--', '.':'.-.-.-',
'?':'..--..', '/':'-..-.', '-':'-....-', '(':'-.--.', ')':'-.--.-'}

# Transform dictionary into 2 lists, so we can iterate them for the Morse Code chart in template
keys, values = zip(*MORSE_CODE_DICT.items())

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)
# Morse encryption based on code by:
# https://www.geeksforgeeks.org/morse-code-translator-python/
