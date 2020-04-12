#Function for displaying the amount of particulate matter (microgram / m^3)
#PM level:
#   average = 0 ~ 35   -> B
#   bad = 36 ~ 75      -> G
#   very bad = 76 ~    -> R

def pm(dust):
    import RPi.GPIO as GPIO
    import time

    GPIO.setmode (GPIO.BCM)

    r = 20
    g = 21
    b = 22
    GPIO.setwarnings(False)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(r,GPIO.OUT) #Red
    GPIO.setup(g,GPIO.OUT) #Green
    GPIO.setup(b,GPIO.OUT) #Blue

    #initially turn off all LEDs
    GPIO.output(r, False)
    GPIO.output(g, False)
    GPIO.output(b, False)

    if dust <= 35:
        GPIO.output(b, True)
    elif dust > 35 and dust <= 75:
        GPIO.output(g, True)
    elif dust > 75:
        GPIO.output(r, True)
