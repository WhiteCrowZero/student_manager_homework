"""
学生选课系统 login_controller
包含
    1. 登录
注：
    1. 密码使用SHA256加密
    2. 登录不同的账户，使用不同的逻辑管理器
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
    def __init__(self, host='127.0.0.1', port=12345):
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
    def login(self, request, client_socket):
        username = request.get("username")
        password = request.get("password")
        password = self.hash_password(password)
        user = self.authenticate(username, password)

        if user:
            self.handle_role(user, client_socket)
            role = user["role"]
            response = {"status": "success", "role": role}
            client_socket.sendall(json.dumps(response).encode('utf-8'))
            return True
        else:
            response = {"status": "error", "message": "登录失败"}
            client_socket.sendall(json.dumps(response).encode('utf-8'))
            return False

    # 处理退出
    def exit(self, client_socket):
        client_socket.close()
        self.clients.remove(client_socket)

    # 处理客户端的请求消息
    def handle_client(self, client_socket):
        # 主要处理部分，采用分支结构，不同的账户登录，使用不同的管理器
        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                # 卫语句，及时退出
                if not data:
                    break

                # 接收请求，处理登录身份验证和注册
                request = json.loads(data)
                action = request.get("action")

                # 处理登录请求
                if action == "login":
                    if self.login(request, client_socket):
                        break
                else:
                    response = {"status": "error", "message": "无效请求"}
                    client_socket.sendall(json.dumps(response).encode('utf-8'))
            except Exception as e:
                print(f"处理客户端时出错: {e}")
                break
        self.exit(client_socket)

    # 主线程：等待客户端连接
    def main(self):
        self.start_server()
        self.db_manager = DatabaseManager()  # 连接数据库类

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

    # 验证用户身份
    def authenticate(self, username, password):
        result = self.db_manager.authenticate(username, password)
        if result:
            return result  # 返回用户信息
        return None

    # 处理不同身份
    def handle_role(self, user, client_socket):
        role = user["role"]
        if role == "student":
            StudentController(client_socket, self.db_manager).start()
        elif role == "teacher":
            TeacherController(client_socket, self.db_manager).start()
        elif role == "admin":
            AdminController(client_socket, self.db_manager).start()


if __name__ == '__main__':
    server = LoginController()
    server.run()
