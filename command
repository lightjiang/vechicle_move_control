/home/pi/catkin_ws/src/vechicle_move_control/laser_sdk/output/Linux/Release/ultra_simple
rosrun rviz rviz -d  /home/workstation/catkin_ws/src/vechicle_move_control/rviz/rplidar.rviz
rosrun rqt_graph rqt_graph

rosrun gmapping slam_gmapping scan:=scan


