# GPS-Plotter

ROS based project which collects GPS and heading/compass data  from robot/rover and plot their real time location. The communication takes place via ROS over wifi (in my case).

The values are sent using a node 'send_gps' in a string format and received on a node 'receive_gps' via topic 'topic_gps'. The values are then processed and plotted on a map.

# How to Run
1. Setup your ROS environment (may take some time and effort)

2. Run roscore on a terminal window

3. Run file dummy_sender.py on a new terminal window

4. Can check if data is being sent by running command 'rostopic echo /topic_gps' on a new terminal window.

5. Run file Plot_GPS.py on another terminal window

Note1 - You can also add waypoints('\n' Separated) if you want your robot to reach to a particular GPS coordinate by typing GPS co-ordinate and clicking 'Plot WayPoints' on the GUI.

Note2 - File dummy_sender.py is just a test file to show the functioning of the GPS plotting. For further queries, feel free to drop a mail at shubh.agarwal2017@vitstudent.ac.in 

# Support Me
  If you like this, leave a star
  
  Make sure you follow me for more cool projects to come
