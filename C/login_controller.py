"""
学生选课系统 login_controller
包含
    1. 登录
    2. 注册
    3. 退出
注：
    1. 密码使用SHA256加密



    1. 登录不同的账户，进入不同的功能界面
"""
import socket
import hashlib
import json
from threading import Thread
from C.student_controller import StudentController
from C.teacher_controller import TeacherController
from C.admin_controller import AdminController
from M.db_manager import DatabaseManager


class LoginController:
    def __init__(self, host='127.0.0.1', port=8888):
        super().__init__()
        self.db_manager = None
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []

    # 密码加密方法（SHA256）
    @staticmethod
    def hash_password(password):
        sha256 = hashlib.sha256()
        sha256.update(password.encode('utf-8'))
        return sha256.hexdigest()

    # 启动服务，连接数据库
    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print("服务器已启动，等待客户端连接...")

    # 处理客户端请求
    # 处理登录
    def login(self, username, password):
        pass


    # 处理注册
    def register(self, username, password):
        pass

    # 处理退出
    def exit(self, client_socket):
        client_socket.close()
        self.clients.remove(client_socket)

    # 处理客户端的请求消息
    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break

                request = json.loads(data)
                action = request.get("action")

                if action == "login":
                    username = request.get("username")
                    password = request.get("password")
                    user = self.authenticate(username, password)

                    if user:
                        role = user["role"]
                        if role == "student":
                            StudentController(client_socket, self.db_manager).start()
                        elif role == "teacher":
                            TeacherController(client_socket, self.db_manager).start()
                        elif role == "admin":
                            AdminController(client_socket, self.db_manager).start()
                        break
                    else:
                        response = {"status": "error", "message": "登录失败"}
                        client_socket.sendall(json.dumps(response).encode('utf-8'))
                else:
                    response = {"status": "error", "message": "无效请求"}
                    client_socket.sendall(json.dumps(response).encode('utf-8'))
            except Exception as e:
                print(f"处理客户端时出错: {e}")
                break
        client_socket.close()

    # 主线程：等待客户端连接
    def main(self):
        self.start_server()
        self.db_manager = DatabaseManager() # 连接数据库类

        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"客户端已连接: {addr}")
            self.clients.append(client_socket)

            # 为每个客户端启动独立线程
            client_thread = Thread(target=self.handle_client, args=(client_socket,))
            client_thread.daemon = True
            client_thread.start()

    # 运行服务器
    def run(self):
        try:
            self.main()
        except KeyboardInterrupt:
            print("服务器已关闭")
        finally:
            if self.server_socket:
                self.server_socket.close()

    def authenticate(self, username, password):
        pass


if __name__ == '__main__':
    server = LoginController()
    server.run()