import rclpy
from rclpy.node import Node

class HelloNode(Node):
    def __init__(self):
        super().__init__('hello_node')
        self.timer = self.create_timer(1.0,self.tick)
        self.count = 0
    def tick(self):
        self.count += 1
        self.get_logger().info(f'Tick {self.count}')

def main(args=None):
    rclpy.init(args=args)
    node = HelloNode()
    try:
      rclpy.spin(node)
    except KeyboardInterrupt:
      pass
    finally: 
      node.destroy_node()
      rclpy.shutdown()

if __name__ == '__main__':
    main()