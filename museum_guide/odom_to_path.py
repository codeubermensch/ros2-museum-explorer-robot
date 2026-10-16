import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry, Path
from geometry_msgs.msg import PoseStamped


class OdomToPath(Node):
    def __init__(self):
        super().__init__("odom_to_path")

        self.MAX_POSES = 1000

        self.sub = self.create_subscription(
            Odometry,
            "/odom",
            self.odom_callback,
            10,
        )
        self.pub = self.create_publisher(Path, "/path", 10)

        self.path = Path()
        self.path.header.frame_id = "odom"

        self.create_timer(1.0, self.publish_path)

    def odom_callback(self, msg):
        pose_stamped = PoseStamped()
        pose_stamped.header = msg.header
        pose_stamped.pose = msg.pose.pose

        self.path.poses.append(pose_stamped)
        # Trim from the front to keep the list bounded.
        if len(self.path.poses) > self.MAX_POSES:
            self.path.poses.pop(0)

    def publish_path(self):
        self.path.header.stamp = self.get_clock().now().to_msg()
        self.pub.publish(self.path)


def main(args=None):
    rclpy.init(args=args)
    node = OdomToPath()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
