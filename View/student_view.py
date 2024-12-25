import tkinter as tk
from tkinter import ttk, messagebox
from Controller.handle_client import HandleClient


class StudentView:
    def __init__(self, root, handle_client, id):
        self.student_window = root
        self.__handle_client = handle_client
        self.__id = id

    def open_student_interface(self):
        # 创建学生界面窗口
        self.student_window.title("学生界面")
        self.student_window.geometry("400x300")
        title_label = ttk.Label(self.student_window, text="学生选课系统", font=("宋体", 16, "bold"))
        title_label.grid(row=0, padx=10, pady=10)

        # 配置行和列的权重，使标签居中
        self.student_window.grid_rowconfigure(0, weight=1)
        self.student_window.grid_columnconfigure(0, weight=1)

        style = ttk.Style()
        style.configure('TButton', font=('黑体', 12))

        btn_show_student_info = ttk.Button(self.student_window, text="查看信息", command=self.show_student_info,
                                           style="TButton", width=20)
        btn_show_student_info.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        btn_show_course_selection = ttk.Button(self.student_window, text="查看课程并选课",
                                               command=self.show_course_selection,
                                               style="TButton", width=20)
        btn_show_course_selection.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        btn_show_selected_course_grades = ttk.Button(self.student_window, text="查看所选课程成绩",
                                                     command=self.show_selected_course_grades,
                                                     style="TButton", width=20)
        btn_show_selected_course_grades.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)

        btn_modify_password = ttk.Button(self.student_window, text="修改自己的密码", command=self.modify_passwd,
                                         style="TButton",
                                         width=20)
        btn_modify_password.grid(row=4, column=0, sticky="nsew", padx=10, pady=10)

        btn_ai_for_student = ttk.Button(self.student_window, text="向AI助教询问", command=self.ai_for_student,
                                        style="TButton", width=20)
        btn_ai_for_student.grid(row=5, column=0, sticky="nsew", padx=10, pady=10)

        self.student_window.columnconfigure(0, weight=1)
        for i in range(6):
            self.student_window.rowconfigure(i, weight=1)

        self.student_window.mainloop()

    def show_student_info(self):
        info_window = tk.Toplevel(self.student_window)
        info_window.title("学生信息")
        info_window.geometry("600x400")

        columns = ("学号", "姓名", "性别", "所在学院", "班级")
        tree = ttk.Treeview(info_window, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")

        # 从服务端获取学生数据
        resp = self.__handle_client.send_request({"action": "show_student_info_single", "account_id": self.__id})
        status = resp.get("status")
        if status:
            student = resp.get("datas")
            tree.insert("", "end", values=(student))

        tree.pack(fill="both", expand=True)

    def show_course_selection(self):
        selection_window = tk.Toplevel(self.student_window)
        selection_window.title("选课界面")
        selection_window.geometry("600x400")

        columns = ("课程号", "课程名", "学分", "任课教师")
        tree = ttk.Treeview(selection_window, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")

        # 从服务端获取课程数据
        courses = self.__handle_client.send_request({"action": "show_course", "account_id": self.__id})
        status = courses.get("status")
        if status:
            courses = courses.get("datas")
            for course in courses:
                tree.insert("", "end", values=(course))

        tree.pack(fill="both", expand=True)

        submit_button = ttk.Button(selection_window, text="提交", command=lambda: self.submit_selection(tree))
        submit_button.pack(pady=10)

    def submit_selection(self, tree):
        for item in tree.selection():
            course_values = tree.item(item, "values")
            course_id = course_values[0]  # 课程号是第一列

            # 向服务端提交选课数据
            resp = self.__handle_client.send_request(
                {"action": "select_course", "student_id": self.__id, "course_id": course_id})
            status = resp.get("status")
            if not status:
                messagebox.showerror("错误", "选课失败")
        messagebox.showinfo("提示", "选课成功")

    def show_selected_course_grades(self):
        grades_window = tk.Toplevel(self.student_window)
        grades_window.title("成绩界面")
        grades_window.geometry("600x400")

        columns = ("课程号", "课程名", "成绩")
        tree = ttk.Treeview(grades_window, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")

        # 从服务端获取成绩数据
        grades_data = self.__handle_client.send_request(
            {"action": "show_student_course_score", "student_id": self.__id})
        status = grades_data.get("status")
        if status:
            grades_data = grades_data.get("datas")
            for grade in grades_data:
                tree.insert("", "end", values=(grade))

        tree.pack(fill="both", expand=True)

    def modify_passwd(self):
        password_window = tk.Toplevel(self.student_window)
        password_window.title("修改密码")
        password_window.geometry("300x200")

        new_password_label = ttk.Label(password_window, text="新密码:")
        new_password_label.pack(pady=5)
        new_password_entry = ttk.Entry(password_window, show="*")
        new_password_entry.pack(pady=5)

        confirm_password_label = ttk.Label(password_window, text="确认新密码:")
        confirm_password_label.pack(pady=5)
        confirm_password_entry = ttk.Entry(password_window, show="*")
        confirm_password_entry.pack(pady=5)

        submit_button = ttk.Button(
            password_window,
            text="提交",
            command=lambda: self.check_password(new_password_entry.get(), confirm_password_entry.get()),
        )
        submit_button.pack(pady=10)

    def check_password(self, new_password, confirm_password):
        if new_password == confirm_password:
            response = self.__handle_client.send_request(
                {"action": "modify_passwd", "id": self.__id, "new_password": new_password})
            if response["status"] == "success":
                messagebox.showinfo("成功", "密码修改成功")
            else:
                messagebox.showerror("错误", response.get("message", "未知错误"))
        else:
            messagebox.showerror("错误", "两次输入密码不一致，请重新输入")

    def ai_for_student(self):
        from View.ai_view import StudentAIHelper
        ai_view = StudentAIHelper(self.student_window, self.__handle_client, self.__id)
        ai_view.ai_for_student()


# 主程序示例
if __name__ == "__main__":
    root = tk.Tk()
    handle_client = HandleClient()
    student_view = StudentView(root, handle_client, "test_id")
    student_view.open_student_interface()
    root.mainloop()
