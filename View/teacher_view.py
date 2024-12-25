import tkinter as tk
from tkinter import ttk, messagebox

from Controller.handle_client import HandleClient


class TeacherView:
    def __init__(self, root, handle_client, teacher_id):
        self.__id = teacher_id  # 教师ID
        self.teacher_window = root  # 主窗口
        self.__handle_client = handle_client  # 客户端通信句柄

    def open_teacher_interface(self):
        """打开教师主界面"""
        self.teacher_window.title("教师界面")
        self.teacher_window.geometry("400x300")

        # 主界面布局使用 ttk 样式按钮
        style = ttk.Style()
        style.configure('TButton', font=('黑体', 12))

        ttk.Label(self.teacher_window, text="教师管理系统", font=("宋体", 16, "bold")).pack(pady=10)

        # 查看所教课程信息按钮
        style = ttk.Style()
        btn_show_teacher_course_selection_info = ttk.Button(
            self.teacher_window, text="查看所教课程信息",
            command=self.show_teacher_course_selection_info
        )
        btn_show_teacher_course_selection_info.pack(padx=10, pady=10)

        # 录入课程成绩按钮
        btn_enter_grades = ttk.Button(
            self.teacher_window, text="录入课程成绩",
            command=self.enter_grades
        )
        btn_enter_grades.pack(padx=10, pady=10)

        self.teacher_window.mainloop()

    def show_teacher_course_selection_info(self):
        """显示教师所教课程信息"""
        selection_window = tk.Toplevel(self.teacher_window)
        selection_window.title("我的课程")
        selection_window.geometry("400x300")

        # 表格样式
        columns = ("课程号", "课程名", "学分")
        tree = ttk.Treeview(selection_window, columns=columns, show="headings")

        # 设置表头
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=100)

        # 从服务端获取课程数据
        courses = self.__handle_client.send_request({"action": "get_teacher_courses", "teacher_id": self.__id})
        status = courses.get("status")

        if status == "success":
            courses = courses.get("datas")
            for course in courses:
                tree.insert("", "end", values=course)
            tree.pack(fill="both", expand=True, padx=10, pady=10)
        else:
            messagebox.showerror("错误", "获取课程信息失败")

        ttk.Button(selection_window, text="关闭", command=selection_window.destroy).pack(pady=10)

    def enter_grades(self):
        """录入成绩"""
        grades_window = tk.Toplevel(self.teacher_window)
        grades_window.title("录入成绩")
        grades_window.geometry("300x250")

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
        ttk.Label(grades_window, text="选择课程:").pack(pady=5)
        course_var = tk.StringVar()
        course_dropdown = ttk.Combobox(grades_window, textvariable=course_var, state="readonly", width=25)
        course_dropdown['values'] = [f"{course[0]} {course[1]}" for course in teacher_courses]
        course_dropdown.pack(pady=5)
        course_dropdown.current(0)

        # 输入学号和成绩
        ttk.Label(grades_window, text="输入学号:").pack(pady=5)
        student_id_entry = ttk.Entry(grades_window)
        student_id_entry.pack(pady=5)

        ttk.Label(grades_window, text="输入成绩:").pack(pady=5)
        grade_entry = ttk.Entry(grades_window)
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

            try:
                # 转换成绩为数值
                grade = float(grade)
            except ValueError:
                messagebox.showwarning("警告", "成绩必须是数字")
                return

            # 提交成绩
            course_id = selected_course.split(" ")[0]
            request = {
                "action": "update_scores",
                "course_id": course_id,
                "student_id": student_id,
                "score": grade
            }
            response = self.__handle_client.send_request(request)
            if response.get("status") == "success":
                messagebox.showinfo("提示", "成绩保存成功")
            else:
                messagebox.showerror("错误", "保存成绩失败")

        # 保存按钮
        ttk.Button(grades_window, text="保存成绩", command=save_grade).pack(pady=10)
        ttk.Button(grades_window, text="关闭", command=grades_window.destroy).pack(pady=5)


# 以下代码用于测试
if __name__ == '__main__':
    root = tk.Tk()
    handle_client = HandleClient()
    app = TeacherView(root, handle_client, "T001")  # 假设教师ID为 T001
    app.open_teacher_interface()
    root.mainloop()
