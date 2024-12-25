import tkinter as tk
from tkinter import ttk, messagebox
from Controller.handle_client import HandleClient


class LoginView:
    def __init__(self, root):
        self.root = root
        self.root.title("学生选课管理系统")
        self.root.geometry("400x300+500+200")
        self.__handle_client = HandleClient()
        self.setup_ui()
        self.id = None

    def setup_ui(self):
        """设置登录界面UI"""
        # 标题
        title_label = ttk.Label(self.root, text="学生选课管理系统", font=("黑体", 16, "bold"))
        title_label.pack(pady=10)

        # 用户名
        username_label = ttk.Label(self.root, text="账号:", font=("黑体", 13))
        username_label.pack(pady=5)
        self.username_entry = ttk.Entry(self.root, font=("黑体", 13))
        self.username_entry.pack(pady=5)

        # 密码
        password_label = ttk.Label(self.root, text="密码:", font=("黑体", 13))
        password_label.pack(pady=5)
        self.password_entry = ttk.Entry(self.root, show="*", font=("黑体", 13))
        self.password_entry.pack(pady=5)

        # 身份选择
        user_type_label = ttk.Label(self.root, text="选择身份:", font=("黑体", 13))
        user_type_label.pack(pady=5)
        self.user_type_combobox = ttk.Combobox(self.root, font=("黑体", 13), state="readonly")
        self.user_type_combobox['values'] = ("学生", "管理员", "教师")
        self.user_type_combobox.set("学生")
        self.user_type_combobox.pack(pady=5)

        # 登录按钮
        login_button = ttk.Button(self.root, text="确认登录", command=self.login)
        login_button.pack(pady= 10)

    def validate_login(self, username, password):
        """验证登录信息"""
        request_data = {
            "action": "login",
            "username": username,
            "password": password,
        }
        self.__handle_client.connect()
        resp = self.__handle_client.send_request(request_data)
        if resp["status"] == "success":
            return True, resp["category"], resp["id"]
        else:
            self.__handle_client.close()
            return False, resp["message"], None

    def login(self):
        """处理登录逻辑"""
        role_dict = {
            "管理员": "admin",
            "学生": "student",
            "教师": "teacher"
        }
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role_input = role_dict[self.user_type_combobox.get()]

        if not username or not password:
            messagebox.showerror("错误", "请输入用户名和密码")
            return

        status, role, user_id = self.validate_login(username, password)
        if status:
            if role != role_input:
                messagebox.showerror("错误", "身份不匹配")
                return
            self.id = user_id
            messagebox.showinfo("成功", "登录成功！")
            self.root.destroy()  # 关闭登录窗口

            if role == "admin":
                self.open_admin_interface()
            elif role == "student":
                self.open_student_interface()
            elif role == "teacher":
                self.open_teacher_interface()
        else:
            messagebox.showerror("错误", role)

    def open_admin_interface(self):
        """打开管理员界面"""
        from View.admin_view import AdminView
        admin_root = tk.Tk()
        admin_root.geometry("400x300+500+200")
        admin_app = AdminView(admin_root, self.__handle_client, self.id)
        admin_app.open_admin_interface()

    def open_student_interface(self):
        """打开学生界面"""
        from View.student_view import StudentView
        student_root = tk.Tk()
        student_root.geometry("400x300+500+200")
        student_app = StudentView(student_root, self.__handle_client, self.id)
        student_app.open_student_interface()

    def open_teacher_interface(self):
        """打开教师界面"""
        from View.teacher_view import TeacherView
        teacher_root = tk.Tk()
        teacher_root.geometry("400x300+500+200")
        teacher_app = TeacherView(teacher_root, self.__handle_client, self.id)
        teacher_app.open_teacher_interface()


if __name__ == '__main__':
    root = tk.Tk()
    login_view = LoginView(root)
    root.mainloop()
