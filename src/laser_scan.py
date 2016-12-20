# coding=utf-8
"""
light
20161216
process the laser data
"""
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
from PIL import Image
import time
import math
import json


dynamic_map = Image.new("L", (500, 500), color=255)
for _x in range(250 - 18, 250 + 19):
    for _y in range(250 - 10, 250 + 71):
        dynamic_map.putpixel((_x, _y), 100)


class LaserData(object):
    def __init__(self, data):
        self.start_time = time.clock()
        self.pub = rospy.Publisher('chatter', String, queue_size=10)
        self.pub.publish(json.dumps({"abc": 1}))
        self.angle_min = data.angle_min     # -3.12413907051
        self.angle_max = data.angle_max     # 3.14159274101
        self.dynamic_map = dynamic_map
        self.angle_increment = data.angle_increment     # 0.0174532923847
        self.ranges = list(data.ranges)
        k = 180
        for i in self.ranges:
            if i < 1:
                self.push(k*self.angle_increment, i)
            k += 1
        self.dynamic_map.save("/home/workstation/Desktop/1.jpg")
        print(time.clock() - self.start_time)

    def push(self, angle, L):
        x = int(250 + L*200*math.cos(angle))
        y = int(250 + L*200*math.sin(angle))
        for _x in range(x - 2, x + 3):
            for _y in range(y-2, y+3):
                self.dynamic_map.putpixel((_x, _y), 0)


def listener():
    rospy.init_node('LaserScanListener', anonymous=True)
    rospy.Subscriber("scan", LaserScan, LaserData)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
    # LaserData()