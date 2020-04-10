def temperature(min_degree, max_degree):
    import RPi.GPIO as GPIO
    import time
    GPIO.setwarnings(False)
    GPIO.setmode (GPIO.BCM)

    data = 2
    latch = 3
    clock = 4

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

    coms = (10,11,12,13) #left -> right controls which segment to use

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

    print("testing")

    GPIO.setup(data, GPIO.OUT)
    GPIO.setup(latch, GPIO.OUT)
    GPIO.setup(clock, GPIO.OUT)

    for com in coms:
        GPIO.setup(com, GPIO.OUT)
        GPIO.output(com, 0)

    while True:
        for i in range(4):
            digit = 0
            if i == 0:
                digit = int(d1)
            elif i == 1:
                digit = int(d2)
            elif i == 2:
                digit = int(d3)
            elif i == 3:
                digit = int(d4)

            GPIO.output(coms[i], 1)

            for j in range(8):
                GPIO.output(data, num[digit][j])
                GPIO.output(clock, 1)
                time.sleep(0.01)
                GPIO.output(clock, 0)

            GPIO.output(latch, 1)
            time.sleep(0.01)
            GPIO.output(latch, 0)

            GPIO.output(coms[i], 0)
            #time.sleep(0.01)
        time.sleep(0.001)

temperature(15, 31)
