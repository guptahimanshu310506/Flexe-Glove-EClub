import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import time
import mido
from mido import Message
port_name = 'Virtual Raw MIDI 2-0:VirMIDI 2-0 24:0'

try:
    outport = mido.open_output(port_name)
    print(f"Connected to: {port_name}")
except Exception as e:
    print(f"Failed to open MIDI port: {e}")
    exit()


# Send a Control Change message: CC 7 (Volume), value 100, channel 0
cc_msg = mido.Message('control_change', control=7, value=100, channel=0)
outport.send(cc_msg)
print(f"Sent CC → control: {cc_msg.control}, value: {cc_msg.value}, channel: {cc_msg.channel}")


class JointToSound(Node):

    def __init__(self):
        super().__init__('joint_to_sound')
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.listener_callback,
            10)
        self.joint_sound_triggered = {}  # To track per-joint state

    def listener_callback(self, msg):
        for i, joint_name in enumerate(msg.name):
            angle = msg.position[i]

            # Play note if joint crosses threshold and wasn't already triggered
            if joint_name == 'base_link_WS-2':
                if angle > 0.6 and not self.joint_sound_triggered.get(joint_name, False):
                    self.get_logger().info(f'{joint_name} moved to {angle} – PLAY NOTE')
                    self.play_tom(joint_name)
                    self.joint_sound_triggered[joint_name] = True

                elif angle <= 0.6:
                    self.joint_sound_triggered[joint_name] = False  # Reset when back

            if joint_name == 'base_link_SR-2':
                if angle > 0.6 and not self.joint_sound_triggered.get(joint_name, False):
                    self.get_logger().info(f'{joint_name} moved to {angle} – PLAY NOTE')
                    self.play_kick(joint_name)
                    self.joint_sound_triggered[joint_name] = True

                elif angle <= 0.6:
                    self.joint_sound_triggered[joint_name] = False  # Reset when back

            if joint_name == 'base_link_SE-2':
                if angle > 0.9 and not self.joint_sound_triggered.get(joint_name, False):
                    self.get_logger().info(f'{joint_name} moved to {angle} – PLAY NOTE')
                    self.play_hhc(joint_name)
                    self.joint_sound_triggered[joint_name] = True

                elif angle <= 0.9:
                    self.joint_sound_triggered[joint_name] = False  # Reset when back
            
            if joint_name == 'base_link_KU-2':
                if angle > 1.0 and not self.joint_sound_triggered.get(joint_name, False):
                    self.get_logger().info(f'{joint_name} moved to {angle} – PLAY NOTE')
                    self.play_snare(joint_name)
                    self.joint_sound_triggered[joint_name] = True

                elif angle <= 1.0:
                    self.joint_sound_triggered[joint_name] = False  # Reset when back

            if joint_name == 'base_link_MA-2':
                if angle > 0.6 and not self.joint_sound_triggered.get(joint_name, False):
                    self.get_logger().info(f'{joint_name} moved to {angle} – PLAY NOTE')
                    self.play_hho(joint_name)
                    self.joint_sound_triggered[joint_name] = True

                elif angle <= 0.6:
                    self.joint_sound_triggered[joint_name] = False  # Reset when back

            


    def play_tom(self, joint_name):

        msg = Message('control_change', control=20, value=127, channel=0)
        outport.send(msg)

    def play_kick(self, joint_name):

        msg = Message('control_change', control=21, value=127, channel=0)
        outport.send(msg)

    def play_hhc(self, joint_name):

        msg = Message('control_change', control=22, value=127, channel=0)
        outport.send(msg)
    
    def play_hho(self, joint_name):

        msg = Message('control_change', control=23, value=127, channel=0)
        outport.send(msg)
    
    def play_snare(self, joint_name):

        msg = Message('control_change', control=24, value=127, channel=0)
        outport.send(msg)

def main(args=None):
    rclpy.init(args=args)
    node = JointToSound()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
