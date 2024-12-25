import json
import socket


class HandleClient:
    def __init__(self, host="localhost", port=12345):
        self.host = host
        self.port = port
        self.client_socket = None

    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
        except Exception as e:
            print(f"连接到服务器失败: {e}")

    def send_request(self, request_data):
        try:
            message = json.dumps(request_data).encode('utf-8')
            self.client_socket.send(message)
            # print('send message')
            response = self.client_socket.recv(4096)
            # print(response)
            return json.loads(response.decode('utf-8'))
        except Exception as e:
            print(f"请求发送失败: {e}")
            return None

    def close(self):
        if self.client_socket:
            self.client_socket.close()
