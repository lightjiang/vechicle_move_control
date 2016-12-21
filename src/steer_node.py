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


class Control(object):
    def __init__(self, data):
        data = eval(data.data)
        print(data)
        com = data["com"]
        value = data["value"]
        min_distance = data["min_distance"]
        if min_distance < 0.2:
            w = 0.08
        elif min_distance < 0.3:
            w = 0.05
        elif min_distance < 0.5:
            w = 0.02
        else:
            w = 0.01
        angle_s = 7.5
        if com == "R":
            angle_s = 7.5 + value * w
        elif com == "L":
            angle_s = 7.5 - value * w
        p.ChangeDutyCycle(angle_s)
        print(angle_s)


def listener():
    rospy.init_node('steer_node', anonymous=True)
    rospy.Subscriber("move_control", String, Control)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
    # LaserData()