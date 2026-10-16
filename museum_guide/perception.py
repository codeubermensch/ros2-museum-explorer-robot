import math

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point

class Perception(Node):
    def __init__(self):
        super().__init__('perception')
        self.sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10,
        )
        self.front_pub = self.create_publisher(
            Float32,
            '/front_distance',
            10
        )

        self.left_pub = self.create_publisher(Float32, "/left_distance", 10)
        self.right_pub = self.create_publisher(Float32, "/right_distance", 10)
        self.back_pub = self.create_publisher(Float32, "/back_distance", 10)

        self.marker_pub = self.create_publisher(
            MarkerArray,
            '/perception/markers',
            10
        )
        


    def angle_at(self,msg,i):
        return msg.angle_min + i*msg.angle_increment

    def index_at(self, msg, angle):
        return round((angle-msg.angle_min)/msg.angle_increment)%len(msg.ranges)

    def valid_ranges(self,msg):
        valid = []
        for i in range(len(msg.ranges)):
            if msg.range_min < msg.ranges[i] < msg.range_max:
                valid.append(msg.ranges[i])
        return valid

    def min_in_window(self, msg, center_angle, half_width):
        center = self.index_at(msg, center_angle)
        half_count = round(half_width/msg.angle_increment)
        n = len(msg.ranges)

        closest = float('inf')
        for i in range(-half_count,half_count+1):

            index = (i+center)%n
            distance = msg.ranges[index]
            if msg.range_min < distance < msg.range_max:
               closest = min(closest, distance )
    
        return closest

    def make_window_marker(self, marker_id, center_angle, half_width, distance, color):
        m = Marker()
        m.header.frame_id = 'base_scan'
        m.header.stamp = self.get_clock().now().to_msg()
        m.ns = 'perception_windows'
        m.id = marker_id
        m.type = Marker.LINE_STRIP
        m.action = Marker.ADD
        m.scale.x = 0.02 #line width in meters
        m.color.r, m.color.g, m.color.b, m.color.a = color
        m.pose.orientation.w = 1.0

        n_steps = max(2, int(math.degrees(2*half_width)/2))
        points = [Point(x=0.0, y=0.0, z=0.0)]
        for i in range(n_steps+1):
            theta = center_angle - half_width + (2*half_width)*i / n_steps
            points.append(Point(
                x=distance*math.cos(theta),
                y=distance*math.sin(theta),
                z=0.0,
            ))
        points.append(Point(x=0.0, y=0.0, z=0.0))
        m.points = points
        return m

    def scan_callback(self, msg):
        front = self.min_in_window(msg, 0.0, math.pi / 12)
        left  = self.min_in_window(msg, math.pi / 2, math.pi / 12)
        back  = self.min_in_window(msg, math.pi, math.pi / 12)
        right = self.min_in_window(msg, -math.pi / 2, math.pi / 12)
        self.get_logger().info(
            f'front={front:.2f}m  left={left:.2f}m  '
            f'back={back:.2f}m  right={right:.2f}m'
        )
        msg_out = Float32()
        msg_out.data = front
        self.front_pub.publish(msg_out)

        msg_right = Float32()
        msg_right.data = right
        self.right_pub.publish(msg_right)

        msg_left = Float32()
        msg_left.data = left
        self.left_pub.publish(msg_left)

        msg_back = Float32()
        msg_back.data = back
        self.back_pub.publish(msg_back)

        markers = MarkerArray()
        markers.markers = [
            self.make_window_marker(
                marker_id=0,
                center_angle=0.0,
                half_width=math.pi / 12,
                distance=front,
                color=(0.2, 0.9, 0.3, 0.6),
            ),
            self.make_window_marker(
                marker_id=1,
                center_angle=math.pi/2,
                half_width=math.pi / 12,
                distance=left,
                color=(0.3, 0.5, 0.95, 0.6),
            ),
            self.make_window_marker(
                marker_id=2,
                center_angle=math.pi,
                half_width=math.pi / 12,
                distance=back,
                color=(0.95, 0.85, 0.2, 0.6),
            ),
            self.make_window_marker(
                marker_id=3,
                center_angle= -math.pi/2,
                half_width=math.pi / 12,
                distance=right,
                color=(0.95, 0.3, 0.3, 0.6),
            ),
        ]
        self.marker_pub.publish(markers)

def main(args=None):
    rclpy.init(args=args)
    node = Perception()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()