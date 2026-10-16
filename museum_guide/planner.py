import math
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point


class Planner(Node):
    INTENT_COLORS = {
        "GO_FORWARD": (0.2, 0.9, 0.3, 0.9),  # green
        "STOP": (0.6, 0.6, 0.6, 0.9),  # gray
        "TURN_LEFT": (0.3, 0.5, 0.95, 0.9),  # blue
        "TURN_RIGHT": (0.95, 0.3, 0.3, 0.9),  # red
    }

    ARROW_TIPS = {
        "GO_FORWARD": (0.5, 0.0),
        "TURN_LEFT": (0.0, 0.5),
        "TURN_RIGHT": (0.0, -0.5),
    }

    def __init__(self):
        super().__init__("planner")

        self.declare_parameter('stop_distance', 1.0)
        self.STOP_DISTANCE = self.get_parameter('stop_distance').value

        self.front_distance = math.inf
        self.left_distance = math.inf
        self.right_distance = math.inf
        self.back_distance = math.inf

        self.create_subscription(Float32, "/front_distance", self.on_front, 10)
        self.create_subscription(Float32, "/left_distance", self.on_left, 10)
        self.create_subscription(Float32, "/right_distance", self.on_right, 10)
        self.create_subscription(Float32, "/back_distance", self.on_back, 10)

        self.pub = self.create_publisher(String, "/drive_cmd", 10)
        self.marker_pub = self.create_publisher(MarkerArray, "/planner/markers", 10)

    def make_intent_markers(self, command):
        color = self.INTENT_COLORS.get(command, (0.9, 0.9, 0.9, 0.9))
        now = self.get_clock().now().to_msg()

        arrow = Marker()
        arrow.header.frame_id = "base_footprint"
        arrow.header.stamp = now
        arrow.ns = "planner_intent"
        arrow.id = 0
        arrow.type = Marker.ARROW
        arrow.scale.x = 0.04
        arrow.scale.y = 0.08
        arrow.scale.z = 0.10
        arrow.color.r, arrow.color.g, arrow.color.b, arrow.color.a = color
        arrow.pose.orientation.w = 1.0

        if command == "STOP":
            arrow.action = Marker.DELETE
        else:
            arrow.action = Marker.ADD
            dx, dy = self.ARROW_TIPS.get(command, (0.0, 0.0))
            arrow.points = [
                Point(x=0.0, y=0.0, z=0.05),
                Point(x=dx, y=dy, z=0.05),
            ]

        text = Marker()
        text.header.frame_id = "base_footprint"
        text.header.stamp = now
        text.ns = "planner_intent"
        text.id = 1
        text.type = Marker.TEXT_VIEW_FACING
        text.action = Marker.ADD
        text.scale.z = 0.18
        text.color.r, text.color.g, text.color.b, text.color.a = color
        text.pose.position.z = 0.4
        text.pose.orientation.w = 1.0
        text.text = command

        return [arrow, text]

    def on_front(self, msg):
        self.front_distance = msg.data
        self.decide()

    def on_left(self, msg):
        self.left_distance = msg.data

    def on_right(self, msg):
        self.right_distance = msg.data

    def on_back(self, msg):
        self.back_distance = msg.data

    def decide(self):
        if self.front_distance >= self.STOP_DISTANCE:
            decision = "GO_FORWARD"
        elif (
            self.left_distance < self.STOP_DISTANCE
            and self.right_distance < self.STOP_DISTANCE
        ):
            decision = "STOP"
        elif self.left_distance > self.right_distance:
            decision = "TURN_LEFT"
        else:
            decision = "TURN_RIGHT"

        cmd = String()
        cmd.data = decision
        self.pub.publish(cmd)

        markers = MarkerArray()
        markers.markers = self.make_intent_markers(decision)
        self.marker_pub.publish(markers)

        self.get_logger().info(
            f"F={self.front_distance:.2f} L={self.left_distance:.2f} "
            f"R={self.right_distance:.2f}  →  {decision}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = Planner()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
