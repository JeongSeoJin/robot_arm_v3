import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial

class serial_node(Node):
    def __init__(self):
        super().__init__('data_subscriber')
        self.subscription = self.create_subscription(String,'action_topic',self.listener_callback,10)
        self.subscription
        self.serial_port = serial.Serial('/dev/ttyUSB0', 115200)  # 시리얼 포트 설정
        # self.timer = self.create_timer(0.1, self.read_serial_data)  # 0.1초마다 데이터 읽기

    # def listener_callback(self, msg):
    #     self.get_logger().info(f'I heard: {msg.data}')

    def listener_callback(self, msg):
        if self.serial_port.in_waiting > 0:
            self.get_logger().info(f'I heard: {msg.data}')
            self.serial_port.write(f"{msg.data}\n")
            data = self.serial_port.readline().decode('utf-8').strip()
            print("recieved from arudino : {} ".format(data))

def main(args=None):
    rclpy.init(args=args)
    node = serial_node()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
