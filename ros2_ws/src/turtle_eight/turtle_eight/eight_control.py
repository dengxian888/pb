import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math

class TurtleEightNode(Node):
    def __init__(self):
        super().__init__('turtle_eight_node')
        #声明参数
        self.declare_parameter('linear_velocity',0.3 )
        self.declare_parameter('eight_radius', 0.8)
        self.declare_parameter('control_frequency',100 )
        #读取yaml的数值
        self.v = self.get_parameter('linear_velocity').value
        self.r = self.get_parameter('eight_radius').value
        self.freq = self.get_parameter('control_frequency').value
        #向/turtle1/cmd_vel话题发布Twist信息
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer = self.create_timer(1.0/self.freq, self.timer_callback)
        #计算时间
        self.circle_time = 2 * math.pi * self.r / self.v 
        self.start_time = self.get_clock().now().seconds_nanoseconds()[0] + \
                          self.get_clock().now().seconds_nanoseconds()[1] / 1e9
        
        self.get_logger().info('节点已启动')
        self.get_logger().info(f'单个圆时间={self.circle_time:.2f}秒')

    #创建计时器
    def timer_callback(self):
        current_time = self.get_clock().now().seconds_nanoseconds()[0] + \
                       self.get_clock().now().seconds_nanoseconds()[1] / 1e9
        t = current_time - self.start_time
        #按时间来反转转动方向
        if int(t / self.circle_time) % 2 == 0:
            angular_z = self.v / self.r  
        else:
            angular_z = -self.v / self.r  
        #创建一个空的Twist类型信息
        msg = Twist()
        msg.linear.x = self.v
        msg.angular.z = angular_z
        #发布msg
        self.pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)#初始化ros2
    node = TurtleEightNode()#创建节点
    rclpy.spin(node)#一直运行直到定时器触发
    node.destroy_node()#推出是销毁
    rclpy.shutdown()#关闭

if __name__ == '__main__':
    main()
