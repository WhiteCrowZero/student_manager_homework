"""
学生选课系统 student_controller
包含

"""
from threading import Thread
import json

class StudentController(Thread):
    def __init__(self, client_socket, db_manager):
        super().__init__()
        self.client_socket = client_socket
        self.db_manager = db_manager

    # 处理学生的功能
    def handle_student_request(self, request):
        action = request.get("action")
        if action == "view_courses":
            return self.view_courses()
        elif action == "select_course":
            course_id = request.get("course_id")
            student_id = request.get("student_id")
            return self.select_course(student_id, course_id)
        else:
            return {"status": "error", "message": "无效的请求"}

    # 查看课程
    def view_courses(self):
        query = "SELECT * FROM courses"
        courses = self.db_manager.query(query)
        return {"status": "success", "data": courses}

    # 选择课程
    def select_course(self, student_id, course_id):
        query = "INSERT INTO student_courses (student_id, course_id) VALUES (%s, %s)"
        self.db_manager.execute(query, (student_id, course_id))
        return {"status": "success", "message": "选课成功"}

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
