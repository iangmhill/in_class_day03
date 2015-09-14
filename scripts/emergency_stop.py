#!/usr/bin/env python

""" Have bot move forward at a fixed speed until it senses an obstacle via bump sensor, then stop accordingly. """

import rospy
from geometry_msgs.msg import Twist
from neato_node.msg import Bump

class Controller:
	def __init__(self):
		rospy.init_node('bump_control')
		rospy.Subscriber('/bump', Bump, self.react, queue_size=1)
		self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
		self.command = Twist()
		self.command.linear.x = 0.5
		self.command.linear.y = 0
		self.command.linear.z = 0
		self.command.angular.x = 0
		self.command.angular.y = 0	
		self.command.angular.z = 0	

	def stop(self):
		''' stop bot motion '''
		self.command.linear.x = 0
		self.pub.publish(self.command)

	def react(self, bump):
		''' callback function; react to bump info '''
		print bump.leftFront
		if bump.leftFront or bump.leftSide or bump.rightFront or bump.rightSide:
			self.stop()

	def drive(self):
		self.pub.publish(self.command)

controller = Controller()

while not rospy.is_shutdown():
	controller.drive()

# rospy.spin()