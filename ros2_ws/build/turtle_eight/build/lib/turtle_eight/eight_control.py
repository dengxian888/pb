import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math

class TurtleEightNode(Node):
    def __init__(self):
        super().__init__('turtle_eight_node')
        
        self.declare_parameter('linear_velocity',0.3 )
        self.declare_parameter('eight_radius', 0.8)
        self.declare_parameter('control_frequency',100 )
        
        self.v = self.get_parameter('linear_velocity').value
        self.r = self.get_parameter('eight_radius').value
        self.freq = self.get_parameter('control_frequency').value
        
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer = self.create_timer(1.0/self.freq, self.timer_callback)
        
        self.circle_time = 2 * math.pi * self.r / self.v 
        self.start_time = self.get_clock().now().seconds_nanoseconds()[0] + \
                          self.get_clock().now().seconds_nanoseconds()[1] / 1e9
        
        self.get_logger().info('节点已启动')
        self.get_logger().info(f'单个圆时间={self.circle_time:.2f}秒')


    def timer_callback(self):
        current_time = self.get_clock().now().seconds_nanoseconds()[0] + \
                       self.get_clock().now().seconds_nanoseconds()[1] / 1e9
        t = current_time - self.start_time
        
        if int(t / self.circle_time) % 2 == 0:
            angular_z = self.v / self.r  
        else:
            angular_z = -self.v / self.r  
        
        msg = Twist()
        msg.linear.x = self.v
        msg.angular.z = angular_z
        
        self.pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = TurtleEightNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
