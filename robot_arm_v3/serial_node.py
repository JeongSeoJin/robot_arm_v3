import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial

class SerialNode(Node):
    def __init__(self):
        super().__init__('serial_node')
        self.subscription = self.create_subscription(
            String,
            'action_topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

        # 시리얼 포트 설정
        try:
            self.serial_port = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)  # 아두이노 연결된 시리얼 포트 확인
            self.get_logger().info("Serial port opened successfully.")
        except serial.SerialException as e:
            self.get_logger().error(f"Failed to open serial port: {e}")
            self.serial_port = None

    def listener_callback(self, msg):
        self.get_logger().info(f'Received action: {msg.data}')
        if self.serial_port and self.serial_port.is_open:
            try:
                self.serial_port.write(f"{msg.data}\n".encode('utf-8'))  # 문자열을 바이트로 인코딩하여 전송
                self.get_logger().info(f'Sent to Arduino: {msg.data}')
            except serial.SerialTimeoutException as e:
                self.get_logger().error(f"Failed to send data to Arduino: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = SerialNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
