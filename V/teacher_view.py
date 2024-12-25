import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
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
            self.teacher_window, text="查看所教课程选课信息",
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

        # 获取教师课程信息
        response = self.__handle_client.send_request({"action": "get_teacher_courses", "teacher_id": self.__id})
        status = response['status']
        if status:
            teacher_courses = response["courses"]
        else:
            messagebox.showerror("错误", "获取课程信息失败")
            return

        course_var = tk.StringVar()
        course_dropdown = ttk.Combobox(selection_window, textvariable=course_var)
        ##################################################################
        course_dropdown['values'] = teacher_courses.keys()
        course_dropdown.pack()

        def update_table(event):
            selected_course = course_var.get()
            if not selected_course:
                return

            # 获取选课学生信息
            response = self.__handle_client.send_request({"action": "show_course_students", "course": selected_course})
            if response and "students" in response:
                students = response["students"]
            else:
                messagebox.showerror("错误", "获取学生信息失败")
                return

            columns = ("学号", "姓名", "性别", "所在学院")
            tree = ttk.Treeview(selection_window, columns=columns, show="headings")

            for col in columns:
                tree.heading(col, text=col)

            for student in students:
                tree.insert("", "end", values=(student["学号"], student["姓名"], student["性别"], student["所在学院"]))

            tree.pack()

        course_dropdown.bind("<<ComboboxSelected>>", update_table)

    def enter_grades(self):
        grades_window = tk.Toplevel(self.teacher_window)
        grades_window.title("录入成绩")

        # 获取教师课程信息
        response = self.__handle_client.send_request({"action": "get_teacher_courses"})
        if response and "courses" in response:
            teacher_courses = response["courses"]
        else:
            messagebox.showerror("错误", "获取课程信息失败")
            return

        course_var = tk.StringVar()
        course_dropdown = ttk.Combobox(grades_window, textvariable=course_var)
        course_dropdown['values'] = list(teacher_courses.keys())
        course_dropdown.pack()

        def update_table_with_grades(event):
            selected_course = course_var.get()
            if not selected_course:
                return

            # 获取选课学生成绩信息
            response = self.__handle_client.send_request({"action": "show_course_students", "course": selected_course})
            if response and "students" in response:
                students = response["students"]
            else:
                messagebox.showerror("错误", "获取学生成绩信息失败")
                return

            columns = ("学号", "姓名", "性别", "所在学院", "成绩")
            tree = ttk.Treeview(grades_window, columns=columns, show="headings")

            for col in columns:
                tree.heading(col, text=col)

            for student in students:
                grade = student.get("成绩", "")
                tree.insert("", "end", values=(
                    student["学号"], student["姓名"], student["性别"], student["所在学院"], grade
                ))

            tree.pack()

            def save_grades():
                updated_grades = []
                for item in tree.get_children():
                    values = tree.item(item, "values")
                    updated_grades.append({
                        "学号": values[0], "成绩": values[-1]
                    })

                response = self.__handle_client.send_request({
                    "action": "update_scores", "data": {"course": selected_course, "grades": updated_grades}
                })
                if response and response.get("status") == "success":
                    messagebox.showinfo("提示", "成绩保存成功")
                else:
                    messagebox.showerror("错误", "保存成绩失败")

            save_button = tk.Button(grades_window, text="保存", command=save_grades)
            save_button.pack()

        course_dropdown.bind("<<ComboboxSelected>>", update_table_with_grades)


if __name__ == '__main__':
    root = tk.Tk()
    client = HandleClient()  # 假设已经定义 HandleClient 类
    app = TeacherView(root, client)
    app.open_teacher_interface()
    root.mainloop()
