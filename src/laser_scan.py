#!/usr/bin/env python
# coding=utf-8
"""
light
20161216
process the laser data
"""
import roslib

roslib.load_manifest('vechicle_move_control')
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
from PIL import Image
import time
import math


class LaserHandler(object):
    def __init__(self):
        rospy.init_node("laser_scan", anonymous=True)
        self.pub = rospy.Publisher('move_control', String, queue_size=1)
        rospy.on_shutdown(self.shutdown)
        rospy.Subscriber("scan", LaserScan, self.run2, queue_size=1)
        self.map_height = 800
        self.map_width = 800
        self.dynamic_map = Image.new("L", (self.map_width, self.map_height), color=255)
        self.command_list = [0 for _ in range(20)]
        self.draw_me()
        rospy.spin()

    def draw_me(self):
        for x in range(self.map_width / 2 - 9, self.map_width / 2 + 10):
            for y in range(self.map_height / 2, self.map_height / 2 + 40):
                self.dynamic_map.putpixel((x, y), 100)

    def run2(self, data):
        self.dynamic_map = Image.new("L", (self.map_width, self.map_height), color=255)
        self.draw_me()
        angle_increment = data.angle_increment  # 0.0174532923847
        # ranges = list(data.ranges)
        lis = list(data.ranges)
        ranges = lis  # [:180]
        k = 0
        costs = []
        temp = 100
        temp2 = []
        copy = []
        for i in range(0, len(ranges)):
            if ranges[i] == float("inf"):
                if i > 3:
                    ranges[i] = sum(ranges[i - 3:i]) / 3
                else:
                    ranges[i] = 1
        for i in range(0, len(ranges)):
            copy.append([i, ranges[i]])
            self.push(k * angle_increment, ranges[i], i)
            if 40 <= k <= 140:
                res = self.cost(ranges[i - 30:i + 31])
                if res < temp:
                    temp = res
                    temp2 = [k]
                elif res == temp:
                    temp2.append(k)
                costs.append(res)
            k += 1
        print(copy)
        print(temp2)
        if len(temp2) > 1:
            print("1111111111111111")
        else:
            print(123, ranges[temp2[0] - 30:temp2[0] + 31])
            if temp < 0.2:
                var = 0
            else:
                var = (temp2[0] - 90.0) / 50.0 * 1
            k = 2
            value = (sum(self.command_list[-k:]) + var) / (k + 1)
            self.command_list.append(value)
            self.send(com="go", value=value, distance=2)
        print(temp, temp2, sum(temp2) / len(temp2))

    def run(self, data):
        start_time = time.clock()
        # self.angle_min = data.angle_min     # -3.12413907051
        # self.angle_max = data.angle_max     # 3.14159274101
        angle_increment = data.angle_increment  # 0.0174532923847
        ranges = list(data.ranges)
        k = 90
        space = {"R": [], "L": [], "M": []}
        right = 0
        left = 0
        mid = 0
        distance = 3
        costs = []
        for i in range(0, len(ranges)):
            if ranges[i] != float("inf"):
                self.push(k * angle_increment, ranges[i])

            if 30 < k < 150:
                costs.append(self.cost(ranges[i - 5:i + 6]))
            if ranges[i] < 0.7:
                if 85 < k < 95:
                    if ranges[i] < distance:
                        distance = ranges[i]
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

    def cost(self, data):
        res = 0
        obstacle_distance = 0.2
        for i in range(0, 61):
            v = data[i]
            res += (0.75 + (30.0 - abs(i - 30.0)) / 120.0) * (obstacle_distance / v) ** 2
        return res

    def send(self, com, value, distance):
        dic = {"com": com, "value": value, "min_distance": distance}
        print(dic)
        self.pub.publish(str(dic))

    def push(self, angle, L, an):
        # x = int(self.map_width/2 - L*100*math.cos(angle))
        # y = int(self.map_height/2 - L*100*math.sin(angle))
        # print angle*180/math.pi
        x = int(self.map_width / 2 - L * 100 * math.cos(angle))
        y = int(self.map_height / 2 - L * 100 * math.sin(angle))
        if 0 < y <= self.map_height - 4 and 0 < x <= self.map_width - 4:
            #     for _x in range(x - 3, x + 4):
            #         for _y in range(y-3, y+4):
            self.dynamic_map.putpixel((x, y), 200 * an / 360)

    @staticmethod
    def stop_motor():
        pass

    def shutdown(self):
        print "saving..................."
        self.dynamic_map.save("/home/workstation/Desktop/1.jpg")
        self.dynamic_map.show()


if __name__ == '__main__':
    LaserHandler()
    # LaserData()
