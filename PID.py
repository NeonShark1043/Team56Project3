#FeedbackControl_Example.py
# Program provides feedback control based on motor encoder readings
# Developed for in class activity
# ENGR 162, Spring 2018
# Revised for Spring 2025

import time     # import the time library for the sleep function
from buildhat import Motor
from basehat import Button

# Tuning parameters
KP = 0.0 # proportional control gain
KI = 0.0 # integral control gain
KD = 0.0 # derivative control gain

dT = 0.02 # time step

target_pos = 0

current_pos = 0

P = 0
I = 0
D = 0
e_prev = 0

# --------------------------------
# Hardware initialization
# --------------------------------
button = Button(22)
motor = Motor('A')
motor.plimit(.5)
# --------------------------------
# ---------------------------------------------------------
# Control loop -- run infinitely until a keyboard interrupt
# ---------------------------------------------------------
try:
    while True:
        sig = button.value
        # get current position
        current_pos = motor.get_position()
        #print("current position: " + str(current_pos) )
        e = target_pos - current_pos # error
        print("error is " + str(e))

        # set up P,I,D, terms for control inputs
        P = KP * e
        I += KI * e * dT/2
        D = KD * (e - e_prev)/ dT

        #print("D" + str(D))
        if sig == 1:
            # control input for motor
            power_in = P + I + D
            if power_in > 100:
                speed = 100
            elif power_in < -100:
                speed = -100
            else:
                speed = power_in
            motor.start(speed)
            # save error for this step; needed for D
            e_prev = e
        else:
            motor.stop()
            motor.float()
        time.sleep(dT)

# ---------------------------------------------------------------------
# If a problem occurs with the while or an interrupt from the keyboard
# ---------------------------------------------------------------------
except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    motor.stop()
    motor.float()
