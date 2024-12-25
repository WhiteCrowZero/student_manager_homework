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
            updated_students = request.get("updated_students")
            return self.update_students(updated_students)
        elif action == "add_course":
            course_id = request.get("course_id")
            course_name = request.get("course_name")
            credit = request.get("credit")
            return self.add_course(course_id, course_name, credit)
        elif action == "get_teacher_courses":
            teacher_id = request.get("teacher_id")
            return self.get_teacher_courses(teacher_id)
        elif action == "assign_teacher":
            teacher = request.get("teacher_id")
            course = request.get("course_id")
            class_name = request.get("class_name")
            return self.assign_teacher(teacher, course, class_name)
        elif action == "show_student_course_score":
            student_id = request.get("student_id")
            return self.show_student_course_score(student_id)
        elif action == "update_scores":
            course_id = request.get("course_id")
            student_id = request.get("student_id")
            score = request.get("score")
            return self.update_scores(course_id, student_id, score)
        elif action == "modify_passwd":
            account_id = request.get("account_id")
            new_password = request.get("new_password")
            return self.modify_passwd(account_id, new_password)

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

    def add_course(self, course_id, course_name, credit):
        if self.db_manager.add_course(course_id, course_name, credit):
            return {"status": "success", "message": "课程添加成功"}
        else:
            return {"status": "error", "message": "课程添加失败"}

    def get_teacher_courses(self, teacher_id):
        courses_teachers = self.db_manager.get_teacher_courses(teacher_id)
        if courses_teachers:
            return {"status": "success", "datas": courses_teachers}
        else:
            return {"status": "error", "message": "获取课程教师信息失败"}

    def assign_teacher(self, teacher, course, class_name):
        if self.db_manager.assign_teacher(teacher, course, class_name):
            return {"status": "success", "message": "教师分配成功"}
        else:
            return {"status": "error", "message": "教师分配失败"}

    def modify_passwd(self, account_id, new_password):
        new_password = self.hash_password(new_password)
        if self.db_manager.modify_passwd(account_id, new_password):
            return {"status": "success", "message": "密码修改成功"}
        else:
            return {"status": "error", "message": "密码修改失败"}

    def show_student_course_score(self, student_id):
        student_course_score = self.db_manager.show_student_course_score(student_id)
        if student_course_score:
            return {"status": "success", "datas": student_course_score}
        else:
            return {"status": "error", "message": "获取学生课程成绩失败"}

    def update_scores(self, course_id, student_id, score):
        if self.db_manager.update_students_with_account_id(course_id, student_id, score):
            return {"status": "success", "message": "成绩已更新"}
        else:
            return {"status": "error", "message": "更新成绩失败"}
