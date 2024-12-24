"""
学生选课系统 student_controller
包含

"""
import hashlib
from threading import Thread
import json

from argon2 import hash_password


class StudentController(Thread):
    def __init__(self, client_socket, db_manager):
        super().__init__()
        self.client_socket = client_socket
        self.db_manager = db_manager

    # 密码加密方法（SHA256）
    @staticmethod
    def hash_password(password):
        sha256 = hashlib.sha256()
        sha256.update(password.encode('utf-8'))
        return sha256.hexdigest()

    # 处理学生的功能
    def handle_student_request(self, request):
        action = request.get("action")
        if action == "show_student_info_single":
            id = request.get("student_id")
            return self.show_student_info_single(id)
        elif action == "show_student_course_score":
            student_id = request.get("student_id")
            return self.show_student_course_score(student_id)
        elif action == "modify_passwd":
            student_id = request.get("student_id")
            new_password = request.get("new_password")
            new_password = hash_password(new_password)
            return self.modify_passwd(student_id, new_password)
        elif action == "show_student_course":
            return self.show_course()
        elif action == "select_course":
            student_id = request.get("student_id")
            course_list = request.get("course_list")
            return self.select_course(student_id, course_list)


        else:
            return {"status": "error", "message": "无效的请求"}

    # 运行线程
    def run(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                request = json.loads(data)
                response = self.handle_student_request(request)
                self.client_socket.sendall(json.dumps(response).encode('utf-8'))
            except Exception as e:
                print(f"学生控制器出错: {e}")
                break
        self.client_socket.close()

    def show_student_info_single(self, id):
        info = self.db_manager.show_student_info_single(id)
        if info:
            return {"status": "success", "datas": info}
        else:
            return {"status": "error", "message": "未找到学生信息"}

    def show_student_course_score(self, student_id):
        courses = self.db_manager.show_student_course_score(student_id)
        if courses:
            return {"status": "success", "datas": courses}
        else:
            return {"status": "error", "message": "未找到学生课程信息"}

    def modify_passwd(self, student_id, new_password):
        if self.db_manager.modify_passwd(student_id, new_password):
            return {"status": "success", "message": "密码修改成功"}
        else:
            return {"status": "error", "message": "密码修改失败"}

    def show_course(self):
        info = self.db_manager.show_course()
        if info:
            return {"status": "success", "datas": info}
        else:
            return {"status": "error", "message": "未找到学生课程信息"}

    def select_course(self, student_id, course_list):
        for course_name in course_list:
            if not self.db_manager.select_course(student_id, course_name):
                return {"status": "error", "message": "选课失败"}
        return {"status": "success", "message": "选课成功"}
