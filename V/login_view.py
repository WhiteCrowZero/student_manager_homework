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

        # 身份选择下拉框
        self.user_type_label = ttk.Label(self.root, text="选择身份:", font=("黑体", 15, "bold"))
        self.user_type_label.pack()
        self.user_type_combobox = ttk.Combobox(self.root, font=("黑体", 15, "bold"))
        self.user_type_combobox['values'] = ("学生", "管理员", "教师")
        self.user_type_combobox.set("学生")
        self.user_type_combobox.pack()

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
        self.__handle_client.connect()
        resp = self.__handle_client.send_request(request_data)
        if resp["status"] == "success":
            return True, resp["category"], resp["id"]
        else:
            self.__handle_client.close()
            return False, resp["message"], None

    def login(self):
        role_dict = {
            "管理员": "admin",
            "学生": "student",
            "教师": "teacher"
        }
        username = self.username_entry.get()
        password = self.password_entry.get()
        role_input = role_dict[self.user_type_combobox.get()]
        if not username or not password:
            messagebox.showerror("错误", "请输入用户名和密码")
            return
        status, role, id = self.validate_login(username, password)

        if status:
            if role != role_input:
                messagebox.showerror("错误", "身份不匹配")
                return
            self.id = id
            messagebox.showinfo("成功", "登录成功！")
            self.root.destroy()  # 关闭主窗口

            if role == "admin":
                self.open_admin_interface()
            elif role == "student":
                self.open_student_interface()
            elif role == "teacher":
                self.open_teacher_interface()
        else:
            messagebox.showerror("错误", role)  # 实际这里的 role 变量包含的就是报错信息了

    def open_admin_interface(self):
        from V.admin_view import AdminView
        admin_root = tk.Tk()
        a = AdminView(admin_root, self.__handle_client, self.id)
        a.open_admin_interface()

    def open_student_interface(self):
        from V.student_view import StudentView
        student_root = tk.Tk()
        s = StudentView(student_root, self.__handle_client, self.id)
        s.open_student_interface()

    def open_teacher_interface(self):
        from V.teacher_view import TeacherView
        teacher_root = tk.Tk()
        t = TeacherView(teacher_root, self.__handle_client, self.id)
        t.open_teacher_interface()


if __name__ == '__main__':
    root = tk.Tk()
    login_view = LoginView(root)
    root.mainloop()
