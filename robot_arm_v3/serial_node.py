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

        # 타이머 설정 (0.1초마다 시리얼 포트에서 데이터 읽기 시도)
        self.timer = self.create_timer(0.1, self.read_serial_data)

    def listener_callback(self, msg):
        self.get_logger().info(f'Received action: {msg.data}')
        if self.serial_port and self.serial_port.is_open:
            try:
                self.serial_port.write(f"{msg.data}\n".encode('utf-8'))  # 문자열을 바이트로 인코딩하여 전송
                self.get_logger().info(f'Sent to Arduino: {msg.data}')
            except serial.SerialTimeoutException as e:
                self.get_logger().error(f"Failed to send data to Arduino: {e}")

    def read_serial_data(self):
        if self.serial_port and self.serial_port.is_open:
            try:
                if self.serial_port.in_waiting > 0:  # 읽을 데이터가 있는지 확인
                    arduino_data = self.serial_port.readline().decode('utf-8').strip()  # 아두이노로부터 데이터 읽기
                    self.get_logger().info(f'Received from Arduino: {arduino_data}')
            except serial.SerialException as e:
                self.get_logger().error(f"Failed to read from Arduino: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = SerialNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
