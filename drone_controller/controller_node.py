import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray
from .object_follower import ObjectFollower



class Controller(Node):
    def __init__(self):
        super().__init__('controller')
        self.subscription = self.create_subscription(Int32MultiArray, 'object_pos_and_distance', self.listener_callback, 10)
        self.publisher = self.create_publisher(Int32MultiArray, 'yaw_thrust_pitch', 10)
        # Instantiate an ObjectFollower object
        # PIDs must be set up by editing the constructor in object_follower.py
        self.object_follower = ObjectFollower()

    # Callback for the 'object_pos_and_distance' subscription
    def listener_callback(self, msg_in):
        # Feed values from 'object_pos_and_distance' to the object follower
        self.object_follower(x=msg_in.data[0], y=msg_in.data[1], distance=msg_in.data[2])
        msg_out = Int32MultiArray()
        # Publish object follower outputs to 'yaw_thrust_pitch' topic
        msg_out.data = [self.object_follower.yaw_out, self.object_follower.thrust_out, self.object_follower.pitch_out ]
        self.publisher.publish(msg_out)


def main(args=None):
    rclpy.init(args=args)
    controller = Controller()
    rclpy.spin(controller)
    controller.destroy_node()
    rclpy.shutdown()
    

if (__name__ == "__main__"):
    main()


