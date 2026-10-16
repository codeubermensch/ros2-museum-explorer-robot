import rclpy
from rclpy.node import Node

from std_msgs.msg import String

class HelloPublisher(Node):
    def __init__(self):
        super().__init__('hello_pub')
        self.pub = self.create_publisher(
            String,
            '/hello',
            10
        )
        self.timer = self.create_timer(1.0,self.publish_hello)
        self.count = 0

    def publish_hello(self):
        msg = String()
        msg.data = f'Hello {self.count}'
        self.pub.publish(msg)
        self.get_logger().info(f'Published: "{msg.data}"')
        self.count += 1

def main(args=None):
    rclpy.init(args=args)
    node = HelloPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()