import math
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist


class Controller(Node):
    def __init__(self):
        super().__init__("controller")


        self.declare_parameter('forward_speed', 0.2)
        self.FORWARD_SPEED = self.get_parameter('forward_speed').value

        self.declare_parameter('turn_speed', math.pi/4)
        self.TURN_SPEED = self.get_parameter('turn_speed').value  # rad/s — about 45°/sec

        self.sub = self.create_subscription(
            String,
            "/drive_cmd",
            self.on_command,
            10,
        )
        self.pub = self.create_publisher(Twist, "/cmd_vel", 10)

    def on_command(self, msg):
        command = msg.data
        cmd = Twist()

        if command == "GO_FORWARD":
            cmd.linear.x = self.FORWARD_SPEED
        elif command == "STOP":
            cmd.linear.x = 0.0
        elif command == "TURN_LEFT":
            cmd.angular.z = self.TURN_SPEED
        elif command == "TURN_RIGHT":
            cmd.angular.z = -self.TURN_SPEED

        self.pub.publish(cmd)
        self.get_logger().info(
            f"cmd={command}  →  linear.x={cmd.linear.x:.2f}, angular.z={cmd.angular.z:.2f}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = Controller()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
