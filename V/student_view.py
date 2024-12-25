import tkinter as tk
from tkinter import ttk, messagebox as msgbox, messagebox
from turtledemo.penrose import start

from C.handle_client import HandleClient


class StudentView:
    def __init__(self, root, handle_client, id):
        self.student_window = root
        self.__handle_client = handle_client
        self.__id = id

    def open_student_interface(self):
        # 创建学生界面窗口
        self.student_window.title("学生界面")
        self.student_window.geometry("500x400")

        # 设置按钮字体样式
        button_font = ("宋体", 15, "bold")

        # 添加按钮
        buttons = [
            ("查看信息", self.show_student_info),
            ("查看课程信息并选课", self.show_course_selection),
            ("查看所选课程成绩", self.show_selected_course_grades),
            ("修改自己密码", self.modify_passwd),
            ("向AI助教询问", self.ai_for_student),
        ]

        for text, command in buttons:
            btn = tk.Button(self.student_window, text=text, command=command, font=button_font)
            btn.pack(pady=10)

        self.student_window.mainloop()

    def show_student_info(self):
        info_window = tk.Toplevel(self.student_window)
        info_window.title("学生信息")
        columns = ("学号", "姓名", "性别", "所在学院", "班级")
        tree = ttk.Treeview(info_window, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)

        # 从服务端获取学生数据
        resp = self.__handle_client.send_request({"action": "show_student_info_single", "account_id": self.__id})
        status = resp.get("status")
        if status:
            student = resp.get("datas")
            print(student)
            tree.insert("", "end", values=(student))

        tree.pack()

    def show_course_selection(self):
        selection_window = tk.Toplevel(self.student_window)
        selection_window.title("选课界面")
        columns = ("课程号", "课程名", "学分", "任课教师")
        tree = ttk.Treeview(selection_window, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)

        # 从服务端获取课程数据
        courses = self.__handle_client.send_request({"action": "show_course", "account_id": self.__id})
        print(courses)
        status = courses.get("status")
        if status:
            courses = courses.get("datas")
            for course in courses:
                tree.insert("", "end", values=(course))
        tree.pack()

        submit_button = tk.Button(selection_window, text="提交", command=lambda: self.submit_selection(tree))
        submit_button.pack()

    def submit_selection(self, tree):
        # 获取选中的课程号
        selected_courses = []
        for item in tree.selection():
            course_values = tree.item(item, "values")
            course_id = course_values[0]  # 假设课程号是第一列
            selected_courses.append(course_id)

        # 检查是否有选中课程
        if not selected_courses:
            messagebox.showwarning("提示", "请选择至少一门课程")
            return

        # 向服务端提交选课数据
        resp = self.__handle_client.send_request(
            {"action": "select_course", "student_id": self.__id, "course_list": selected_courses})
        status = resp.get("status")
        if status:
            messagebox.showinfo("提示", "选课成功")
        else:
            messagebox.showerror("错误", "选课失败")

    def show_selected_course_grades(self):
        grades_window = tk.Toplevel(self.student_window)
        grades_window.title("成绩界面")
        columns = ("课程号", "课程名", "成绩")
        tree = ttk.Treeview(grades_window, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)

        # 从服务端获取成绩数据
        grades_data = self.__handle_client.send_request(
            {"action": "show_student_course_score", "student_id": self.__id})
        status = grades_data.get("status")
        if status:
            grades_data = grades_data.get("datas")
            for grade in grades_data:
                tree.insert("", "end", values=(grade))

        tree.pack()

    def modify_passwd(self):
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
            response = self.__handle_client.send_request(
                {"action": "modify_passwd", "id": self.__id, "new_password": new_password})
            if response["status"] == "success":
                msgbox.showinfo("成功", "密码修改成功")
            else:
                msgbox.showerror("错误", response.get("message", "未知错误"))
        else:
            msgbox.showerror("错误", "两次输入密码不一致，请重新输入")

    def ai_for_student(self):
        from V.ai_view import StudentAIHelper
        ai_view = StudentAIHelper(self.student_window, self.__handle_client, self.__id)
        ai_view.ai_for_student()


# 主程序示例
if __name__ == "__main__":
    root = tk.Tk()
    handle_client = HandleClient()
    student_view = StudentView(root, handle_client)
    student_view.open_student_interface()
    root.mainloop()
