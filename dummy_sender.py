#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import time

def send_data():
	rospy.init_node('send_gps', anonymous=True)
	pub_gps = rospy.Publisher('topic_gps', String, queue_size=1)
	
	lat = 12.0
	lon = 79.0
	angle = 0
	rate = rospy.Rate(5) #5Hz
	while(True):
		data = str(lat) + ' ' + str(lon) + ' ' + str(angle)
		print 'Publishing: ', data
		pub_gps.publish(data)
		lat = round( lat + 0.1, 6 )
		lon = round( lon + 0.1, 6 )
		angle = (angle+30)%360
		rate.sleep()

if __name__ == '__main__':
	send_data()
