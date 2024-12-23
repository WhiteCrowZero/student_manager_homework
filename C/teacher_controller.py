from threading import Thread
import json


class TeacherController(Thread):
    def __init__(self, client_socket, db_manager):
        super().__init__()
        self.client_socket = client_socket
        self.db_manager = db_manager

    # 处理教师的功能
    def handle_teacher_request(self, request):
        action = request.get("action")
        if action == "add_course":
            course_name = request.get("course_name")
            return self.add_course(course_name)
        elif action == "view_students":
            course_id = request.get("course_id")
            return self.view_students(course_id)
        else:
            return {"status": "error", "message": "无效的请求"}

    # 添加课程
    def add_course(self, course_name):
        query = "INSERT INTO courses (name) VALUES (%s)"
        self.db_manager.execute(query, (course_name,))
        return {"status": "success", "message": "课程添加成功"}

    # 查看课程的学生
    def view_students(self, course_id):
        query = """
            SELECT s.id, s.name
            FROM students s
            INNER JOIN student_courses sc ON s.id = sc.student_id
            WHERE sc.course_id = %s
        """
        students = self.db_manager.query(query, (course_id,))
        return {"status": "success", "data": students}

    # 运行线程
    def run(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                request = json.loads(data)
                response = self.handle_teacher_request(request)
                self.client_socket.sendall(json.dumps(response).encode('utf-8'))
            except Exception as e:
                print(f"教师控制器出错: {e}")
                break
        self.client_socket.close()
