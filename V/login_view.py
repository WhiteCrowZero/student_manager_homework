import tkinter as tk
from tkinter import ttk, messagebox
from C.handle_client import HandleClient


class LoginView:
    def __init__(self, root):
        self.root = root
        self.root.title("学生选课管理系统")
        self.root.geometry("400x300+500+200")
        self.__handle_client = HandleClient()
        self.setup_ui()
        self.id = None

    def setup_ui(self):
        title_label = tk.Label(self.root, text="学生选课管理系统", font=("黑体", 16, "bold"))
        title_label.pack(pady=10)

        username_label = tk.Label(self.root, text="账号:", font=("黑体", 15, "bold"))
        username_label.pack()
        self.username_entry = tk.Entry(self.root, font=("黑体", 15, "bold"))
        self.username_entry.pack()

        password_label = tk.Label(self.root, text="密码:", font=("黑体", 15, "bold"))
        password_label.pack()
        self.password_entry = tk.Entry(self.root, show="*", font=("黑体", 15, "bold"))
        self.password_entry.pack()

        login_button = tk.Button(self.root, text="确认登录",
                                 command=self.login,
                                 font=("黑体", 15, "bold"))
        login_button.pack(pady=10)

    def validate_login(self, username, password):
        request_data = {
            "action": "login",
            "username": username,
            "password": password,
        }
        resp = self.__handle_client.send_request(request_data)
        if resp["status"] == "success":
            return True, resp["role"], resp["id"]
        else:
            return False, resp["message"], None

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        status, role, id = self.validate_login(username, password)

        if status:
            self.id = id
            messagebox.showinfo("成功", "登录成功！")
            self.root.withdraw()  # Hide the login window

            if role == "管理员":
                self.open_admin_interface()
            elif role == "学生":
                self.open_student_interface()
            elif role == "教师":
                self.open_teacher_interface()
        else:
            messagebox.showerror("错误", role)  # 实际这里的 role 变量包含的就是报错信息了

    def open_admin_interface(self):
        from admin_view import AdminView
        self.__handle_client.connect()
        admin_view = AdminView(self.root, self.__handle_client, self.id)
        admin_view.open_admin_interface()

    def open_student_interface(self):
        from student_view import StudentView
        self.__handle_client.connect()
        student_view = StudentView(self.root, self.__handle_client, self.id)
        student_view.open_student_interface()

    def open_teacher_interface(self):
        from teacher_view import TeacherView
        self.__handle_client.connect()
        teacher_view = TeacherView(self.root, self.__handle_client, self.id)
        teacher_view.open_teacher_interface()


if __name__ == '__main__':
    root = tk.Tk()
    login_view = LoginView(root)
    root.mainloop()
