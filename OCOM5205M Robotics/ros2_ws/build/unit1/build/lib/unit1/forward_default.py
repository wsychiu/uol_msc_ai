# OCOM5205M - Robotics
# Instructions from ROSWorksheet5

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry


class Forward(Node):
    def __init__(self):
        super().__init__("control")

        ### Creating publisher node ###
        self.forward_publisher_ = self.create_publisher(
            Twist, "cmd_vel", 10)
        
        # create_timer(<delay>, <function/action>)
        self.forward_timer_ = self.create_timer(
            0.1, self.publish_velocity)
        
        ### Creating subscriber node ###
        self.create_subscription(Odometry, 'odom', self.odom_callback, 10)

        
        self.robot = Twist()
    
    # Defining a function to publish the velocity command
    def publish_velocity(self):
        self.robot.linear.x = .5 
        self.forward_publisher_.publish(self.robot)

    # Defining the function to subscribe to the velocity command
    def odom_callback(self, odom):
        self.get_logger().info('The odom values are "%s"' % odom)

def main(args=None):
    rclpy.init(args=args)
    node = Forward()
    rclpy.spin(node)    # spin up Forward()
    rclpy.shutdown()    # then we shut it down

if __name__ == "__main__":
    main()