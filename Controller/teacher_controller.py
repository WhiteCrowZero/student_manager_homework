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
        if action == "get_teacher_courses":
            teacher_id = request.get("teacher_id")
            return self.get_teacher_courses(teacher_id)
        elif action == "update_scores":
            course_id = request.get("course_id")
            studetn_id = request.get("student_id")
            score = request.get("score")
            return self.update_scores(course_id, studetn_id, score)
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
                response = self.handle_teacher_request(request)
                self.client_socket.sendall(json.dumps(response).encode('utf-8'))
            except Exception as e:
                print(f"教师控制器出错: {e}")
                break
        self.client_socket.close()

    def get_teacher_courses(self, teacher_id):
        courses = self.db_manager.get_teacher_courses(teacher_id)
        if courses:
            return {"status": "success", "datas": courses}
        else:
            return {"status": "error", "message": "未找到该教师的课程"}

    def update_scores(self, course_id, student_id, score):
        if self.db_manager.update_scores(course_id, student_id, score):
            return {"status": "success", "message": "更新成功"}
        else:
            return {"status": "error", "message": "更新失败"}
