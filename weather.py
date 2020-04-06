

import RPi.GPIO as GPIO
import time
GPIO.setmode (GPIO.BCM)
GPIO.setwarnings(False)

min_degree = 5
max_degree = 13

if min_degree < 10:
    d1 = 0
    d2 = min_degree % 10
else:
    d1 = min_degree / 10
    d2 = min_degree % 10

if max_degree < 10:
    d3 = 0
    d4 = max_degree % 10
else:
    d3 = max_degree / 10
    d4 = max_degree % 10

# d1d2 is min degree, d3d4 is max degree


seg = (15,16,17,18,19,20,21,22)
coms = (23,24,25,26) #left -> right

num = [
    [0,0,0,0,0,0,1,1], #0
    [1,0,0,1,1,1,1,1],
    [0,0,1,0,0,1,0,1],
    [0,0,0,0,1,1,0,1],
    [1,0,0,1,1,0,0,1],
    [0,1,0,0,1,0,0,1],
    [1,1,0,0,0,0,0,1],
    [0,0,0,1,1,1,1,1],
    [0,0,0,0,0,0,0,1],
    [0,0,0,1,1,0,0,1], #9
    [0,0,0,0,0,0,0,0] #empty
]

for pin in seg:
    GPIO.setup(pin, GPIO.OUT)

for com in coms:
    GPIO.setup(com, GPIO.OUT)
    GPIO.output(com, 0)

while True:
    for i in range(4):
        digit = 0
        if i == 0:
            digit = d1
        elif i == 1:
            digit = d2
        elif i == 2:
            digit = d3
        elif i == 3:
            digit = d4

        GPIO.output(coms[i],1)
        for j in range(8):
            GPIO.output(seg[j], num[digit][j])

        time.sleep(0.001)
        GPIO.output(coms[i],0)
