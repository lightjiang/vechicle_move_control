# coding=utf-8
"""
light
20161216
process the laser data
"""
import rospy
from std_msgs.msg import String


class Control(object):
    def __init__(self, data):
        print data


def listener():
    rospy.init_node('steer_node', anonymous=True)
    rospy.Subscriber("move_control", String, Control)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
    # LaserData()