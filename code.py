import sensor
import image
import lcd
import time
from machine import Timer, PWM

# setup our servos
tim1 = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PWM)
tim2 = Timer(Timer.TIMER1, Timer.CHANNEL1, mode=Timer.MODE_PWM)
ch1 = PWM(tim1, freq=50, duty=0, pin=1)
ch2 = PWM(tim2, freq=50, duty=0, pin=2)

# Enable our camera.
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_hmirror(1)
sensor.run(1)

# 58. 77-58


def move(x, y, direction=-1):
    print(x, y)
    # figure out direction
    lo = (x/360.0)

    print('A', 20*direction*(1-lo))
    print('B', 20*direction*lo)

    duty1 = 100*((77+(20*direction*(1-lo)))/1024)
    duty2 = 100*((77-(20*direction*(lo)))/1024)

    ch1.duty(duty1)
    ch2.duty(duty2)


def stop():
    ch1.duty(0)
    ch2.duty(0)


# Color threshold to search for. mostly a guess.
threshold = (60, 100, 40, 110, -10, 20)
prev_x = []
prev_y = []
missed = 0
# Main loop,
while True:
    img = sensor.snapshot()
    # Go through the list of blobs we have found, and average location.
    blobs = img.find_blobs([threshold], area_threshold=15)
    if len(blobs) > 0:
        x, y = (0, 0)
        tot = 0
        # do the averaging
        for blob in blobs:
            x = blob.cx()*blob.pixels()
            y = blob.cy()*blob.pixels()
            tot += blob.pixels()
        prev_x.append(x/tot)
        prev_y.append(y/tot)
    else:
        missed += 1

    if missed > 5:
        stop()
        missed = 0

    if len(prev_x) >= 3:
        x = sum(prev_x) / 3
        y = sum(prev_y) / 3
        prev_x = []
        prev_y = []
        move(x, y)

sensor.shutdown(0)
