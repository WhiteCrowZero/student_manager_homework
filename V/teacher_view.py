import tkinter as tk
from tkinter import ttk, messagebox

from C.handle_client import HandleClient


class TeacherView:
    def __init__(self, root, handle_client, id):
        self.__id = id
        self.teacher_window = root
        self.__handle_client = handle_client

    def open_teacher_interface(self):
        self.teacher_window.title("教师界面")
        self.teacher_window.geometry("400x300")

        button_font = ("宋体", 15, "bold")

        btn_show_teacher_course_selection_info = tk.Button(
            self.teacher_window, text="查看所教课程信息",
            command=self.show_teacher_course_selection_info, font=button_font
        )
        btn_show_teacher_course_selection_info.pack(pady=10)

        btn_enter_grades = tk.Button(
            self.teacher_window, text="录入课程成绩",
            command=self.enter_grades, font=button_font
        )
        btn_enter_grades.pack(pady=10)

        self.teacher_window.mainloop()

    def show_teacher_course_selection_info(self):
        selection_window = tk.Toplevel(self.teacher_window)
        selection_window.title("我的课程")
        selection_window.geometry("400x300")
        columns = ("课程号", "课程名", "学分")
        tree = ttk.Treeview(selection_window, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)

        # 从服务端获取课程数据
        courses = self.__handle_client.send_request({"action": "get_teacher_courses", "teacher_id": self.__id})
        print(courses)
        status = courses.get("status")
        if status:
            courses = courses.get("datas")
            for course in courses:
                tree.insert("", "end", values=(course))
            tree.pack()
        else:
            messagebox.showerror("错误", "获取课程信息失败")

    def enter_grades(self):
        grades_window = tk.Toplevel(self.teacher_window)
        grades_window.title("录入成绩")
        grades_window.geometry("300x200")

        # 获取教师课程信息
        response = self.__handle_client.send_request({"action": "get_teacher_courses", "teacher_id": self.__id})
        if not response.get("status"):
            messagebox.showerror("错误", "获取课程信息失败")
            return

        teacher_courses = response.get("datas", [])
        if not teacher_courses:
            messagebox.showinfo("提示", "当前没有可用课程")
            return

        # 下拉框选择课程
        tk.Label(grades_window, text="选择课程:").pack(pady=5)
        course_var = tk.StringVar()
        course_dropdown = ttk.Combobox(grades_window, textvariable=course_var, state="readonly", width=25)
        course_dropdown['values'] = [(teacher_course[0], teacher_course[1]) for teacher_course in teacher_courses]
        course_dropdown.pack(pady=5)

        # 输入学号和成绩
        tk.Label(grades_window, text="输入学号:").pack(pady=5)
        student_id_entry = tk.Entry(grades_window)
        student_id_entry.pack(pady=5)

        tk.Label(grades_window, text="输入成绩:").pack(pady=5)
        grade_entry = tk.Entry(grades_window)
        grade_entry.pack(pady=5)

        # 保存成绩的函数
        def save_grade():
            selected_course = course_var.get()
            student_id = student_id_entry.get().strip()
            grade = grade_entry.get().strip()

            if not selected_course:
                messagebox.showwarning("警告", "请选择课程")
                return
            if not student_id or not grade:
                messagebox.showwarning("警告", "请输入学号和成绩")
                return

            # 提交成绩
            course_id = selected_course.split(" ", 1)[0]
            request = {
                "action": "update_scores",
                "course_id": course_id, "student_id": student_id, "score": grade
            }
            print(request)
            response = self.__handle_client.send_request(request)
            if response.get("status") == 'success':
                messagebox.showinfo("提示", "成绩保存成功")
            else:
                messagebox.showerror("错误", "保存成绩失败")

        # 保存按钮
        save_button = tk.Button(grades_window, text="保存成绩", command=save_grade)
        save_button.pack(pady=10)


if __name__ == '__main__':
    root = tk.Tk()
    client = HandleClient()  # 假设已经定义 HandleClient 类
    app = TeacherView(root, client)
    app.open_teacher_interface()
    root.mainloop()
