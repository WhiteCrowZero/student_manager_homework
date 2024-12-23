import tkinter as tk
from tkinter import ttk, messagebox as msgbox
from C.handle_client import HandleClient

class StudentView:
    def __init__(self, root, handle_client):
        self.root = root
        self.student_window = None
        self.__handle_client = handle_client

    def open_student_interface(self):
        # 创建学生界面窗口
        self.student_window = tk.Toplevel(self.root)
        self.student_window.title("学生界面")
        self.student_window.geometry("500x400")

        # 设置按钮字体样式
        button_font = ("宋体", 15, "bold")

        # 添加按钮
        buttons = [
            ("查看自己学生信息", self.show_student_info),
            ("查看课程信息并选课", self.show_course_selection),
            ("查看所选课程成绩", self.show_selected_course_grades),
            ("修改自己密码", self.change_password),
        ]

        for text, command in buttons:
            btn = tk.Button(self.student_window, text=text, command=command, font=button_font)
            btn.pack(pady=10)

    def show_student_info(self):
        info_window = tk.Toplevel(self.student_window)
        info_window.title("学生信息")
        columns = ("学号", "姓名", "性别", "所在学院")
        tree = ttk.Treeview(info_window, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)

        # 从服务端获取学生数据
        students = self.handleClient("get_student_info")
        if students:
            for student in students:
                tree.insert("", "end", values=(student["学号"], student["姓名"], student["性别"], student["所在学院"]))

        tree.pack()

    def show_course_selection(self):
        selection_window = tk.Toplevel(self.student_window)
        selection_window.title("选课界面")
        columns = ("课程号", "课程名", "学分", "任课教师")
        tree = ttk.Treeview(selection_window, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)

        # 从服务端获取课程数据
        courses = self.handleClient("get_courses")
        if courses:
            for course in courses:
                tree.insert("", "end", values=(course["课程号"], course["课程名"], course["学分"], course["任课教师"]))

        tree.pack()

        submit_button = tk.Button(selection_window, text="提交", command=lambda: self.submit_selection(tree))
        submit_button.pack()

    def submit_selection(self, tree):
        selected_items = []
        for item in tree.selection():
            selected_items.append(tree.item(item, "values"))

        # 向服务端提交选课数据
        print("选课记录:", selected_items)

    def show_selected_course_grades(self):
        grades_window = tk.Toplevel(self.student_window)
        grades_window.title("成绩界面")
        columns = ("课程号", "学号", "成绩")
        tree = ttk.Treeview(grades_window, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)

        # 从服务端获取成绩数据
        grades_data = self.handleClient("get_grades")
        if grades_data:
            for grade in grades_data:
                tree.insert("", "end", values=(grade["课程号"], grade["学号"], grade["成绩"]))

        tree.pack()

    def change_password(self):
        password_window = tk.Toplevel(self.student_window)
        password_window.title("修改密码")

        new_password_label = tk.Label(password_window, text="新密码:")
        new_password_label.pack()
        new_password_entry = tk.Entry(password_window, show="*")
        new_password_entry.pack()

        confirm_password_label = tk.Label(password_window, text="确认新密码:")
        confirm_password_label.pack()
        confirm_password_entry = tk.Entry(password_window, show="*")
        confirm_password_entry.pack()

        submit_button = tk.Button(
            password_window,
            text="提交",
            command=lambda: self.check_password(new_password_entry.get(), confirm_password_entry.get()),
        )
        submit_button.pack()

    def check_password(self, new_password, confirm_password):
        if new_password == confirm_password:
            response = self.handleClient("change_password", {"new_password": new_password})
            if response["status"] == "success":
                msgbox.showinfo("成功", "密码修改成功")
            else:
                msgbox.showerror("错误", response.get("message", "未知错误"))
        else:
            msgbox.showerror("错误", "两次输入密码不一致，请重新输入")

# 主程序示例
if __name__ == "__main__":
    root = tk.Tk()
    handle_client = HandleClient()
    student_view = StudentView(root, handle_client)
    student_view.open_student_interface()
    root.mainloop()
