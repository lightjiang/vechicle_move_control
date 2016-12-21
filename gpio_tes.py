# coding=utf-8
"""
light
20161216
process the laser data
"""
import rospy
from std_msgs.msg import String
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
p = GPIO.PWM(12, 50)
p.start(7.5)
while 1:
    a = float(input("num="))
    p.ChangeDutyCycle(a)