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


class LaserHandler(object):
    def __init__(self):
        rospy.init_node("LaserScanListener", anonymous=True)
        self.pub = rospy.Publisher('move_control', String, queue_size=1)
        rospy.on_shutdown(self.shutdown)
        rospy.Subscriber("scan", LaserScan, self.run, queue_size=1)
        self.map_height = 1000
        self.map_width = 1000
        self.dynamic_map = Image.new("L", (self.map_width, self.map_height), color=255)
        for x in range(self.map_width / 2 - 9, self.map_width / 2 + 10):
            for y in range(self.map_height - 40, self.map_height):
                self.dynamic_map.putpixel((x, y), 100)

        self.command_list = []
        rospy.spin()

    def run(self, data):
        start_time = time.clock()
        # self.angle_min = data.angle_min     # -3.12413907051
        # self.angle_max = data.angle_max     # 3.14159274101
        angle_increment = data.angle_increment     # 0.0174532923847
        ranges = list(data.ranges[0:180])
        k = 0
        space = {"R": [], "L": [], "M": []}
        right = 0
        left = 0
        mid = 0
        distance = 1
        for i in range(0, len(ranges)):
            if ranges[i] < 0.7:
                if 85 < k < 95:
                    if ranges[i] < distance:
                        distance = ranges[i]
                self.push(k*angle_increment, ranges[i])
            else:
                if 30 < k <= 85:
                    left += 1
                    space["L"].append(k)
                elif 150 > k >= 95:
                    right += 1
                    space["R"].append(k)
                elif 85 < k < 95:
                    mid += 1
                    space["M"].append(k)
            k += 1
        if left - right > 10:
            if "R" in self.command_list[-10:-1]:
                self.send("M", 1, distance)
            else:
                self.send("L", left - right, distance)
        elif right - left > 10:
            if "L" in self.command_list[-10:-1]:
                self.send("M", 1, distance)
            else:
                self.send("R", right - left, distance)
        else:
            self.send("M", 1, distance)
        # self.predict()
        print("end", time.clock() - start_time)
        self.stop_motor()

    def send(self, com, value, distance):
        dic = {"com": com, "value": value, "min_distance": distance}
        print(dic)
        self.command_list.append(com)
        self.pub.publish(str(dic))

    def push(self, angle, L):
        x = int(self.map_width/2 - L*100*math.cos(angle))
        y = int(self.map_height - L*100*math.sin(angle))
        if y <= self.map_height -4 and x <= self.map_width - 4:
            for _x in range(x - 3, x + 4):
                for _y in range(y-3, y+4):
                    self.dynamic_map.putpixel((_x, _y), 0)

    @staticmethod
    def stop_motor():
        pass

    def shutdown(self):
        print "saving..................."
        self.dynamic_map.save("/home/workstation/Desktop/1.jpg")

if __name__ == '__main__':
    LaserHandler()
    # LaserData()