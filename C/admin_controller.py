import hashlib
from threading import Thread
import json

from argon2 import hash_password


class AdminController(Thread):
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

    # 处理管理员请求
    def handle_admin_request(self, request):
        action = request.get("action")

        if action == "show_student_info":
            return self.show_student_info()
        elif action == "update_students":
            updated_students = request.get("data")
            return self.update_students(updated_students)
        elif action == "add_course":
            course = request.get("data")
            return self.add_course(course)
        elif action == "show_courses_teachers":
            return self.show_courses_teachers()
        elif action == "assign_teacher":
            course = request.get("course_id")
            teacher = request.get("teacher_id")
            return self.assign_teacher(course, teacher)
        elif action == "show_course_students":
            course_id = request.get("course_id")
            return self.show_course_students(course_id)
        elif action == "modify_passwd":
            new_passwd = request.get("new_passwd")
            new_passwd = hash_password(new_passwd)
            account_id = request.get("account_id")
            return self.modify_passwd(account_id, new_passwd)
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
                response = self.handle_admin_request(request)
                self.client_socket.sendall(json.dumps(response).encode('utf-8'))
            except Exception as e:
                print(f"管理员控制器出错: {e}")
                break
        self.client_socket.close()

    def show_student_info(self):
        students_info_list = self.db_manager.show_student_info()
        if students_info_list:
            return {"status": "success", "datas": students_info_list}
        else:
            return {"status": "error", "message": "获取学生信息失败"}

    def update_students(self, updated_students):
        if self.db_manager.update_students(updated_students):
            return {"status": "success", "message": "学生信息已更新"}
        else:
            return {"status": "error", "message": "更新学生信息失败"}

    def add_course(self, course):
        if self.db_manager.add_course(course):
            return {"status": "success", "message": "课程添加成功"}
        else:
            return {"status": "error", "message": "课程添加失败"}

    def show_courses_teachers(self):
        courses_teachers = self.db_manager.show_courses_teachers()
        if courses_teachers:
            return {"status": "success", "datas": courses_teachers}
        else:
            return {"status": "error", "message": "获取课程教师信息失败"}

    def assign_teacher(self, course, teacher):
        if self.db_manager.assign_teacher(course, teacher):
            return {"status": "success", "message": "教师分配成功"}
        else:
            return {"status": "error", "message": "教师分配失败"}

    def show_course_students(self, course_id):
        course_students = self.db_manager.show_course_students(course_id)
        if course_students:
            return {"status": "success", "datas": course_students}
        else:
            return {"status": "error", "message": "获取课程学生信息失败"}

    def update_scores(self, updated_scores):
        if self.db_manager.update_scores(updated_scores):
            return {"status": "success", "message": "成绩已更新"}
        else:
            return {"status": "error", "message": "更新成绩失败"}

    def modify_passwd(self, account_id, new_password):
        if self.db_manager.modify_passwd(account_id, new_password):
            return {"status": "success", "message": "密码修改成功"}
        else:
            return {"status": "error", "message": "密码修改失败"}
