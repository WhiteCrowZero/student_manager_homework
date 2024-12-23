import hashlib
from threading import Thread
import json


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
        if action == "add_student":
            student_name = request.get("student_name")
            return self.add_student(student_name)
        elif action == "add_teacher":
            teacher_name = request.get("teacher_name")
            return self.add_teacher(teacher_name)
        elif action == "delete_course":
            course_id = request.get("course_id")
            return self.delete_course(course_id)
        elif action == "view_all_users":
            return self.view_all_users()
        else:
            return {"status": "error", "message": "无效的请求"}

    # 添加学生
    def add_student(self, student_name):
        query = "INSERT INTO students (name) VALUES (%s)"
        self.db_manager.execute(query, (student_name,))
        return {"status": "success", "message": f"学生 {student_name} 添加成功"}

    # 添加教师
    def add_teacher(self, teacher_name):
        query = "INSERT INTO teachers (name) VALUES (%s)"
        self.db_manager.execute(query, (teacher_name,))
        return {"status": "success", "message": f"教师 {teacher_name} 添加成功"}

    # 删除课程
    def delete_course(self, course_id):
        query = "DELETE FROM courses WHERE id = %s"
        self.db_manager.execute(query, (course_id,))
        return {"status": "success", "message": f"课程 ID {course_id} 已删除"}

    # 查看所有用户
    def view_all_users(self):
        query_students = "SELECT id, name, 'student' AS role FROM students"
        query_teachers = "SELECT id, name, 'teacher' AS role FROM teachers"
        students = self.db_manager.query(query_students)
        teachers = self.db_manager.query(query_teachers)
        return {"status": "success", "data": {"students": students, "teachers": teachers}}

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
