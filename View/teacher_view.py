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
        self.teacher_window.geometry("300x200")

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

        # 设置提示标签
        ttk.Label(selection_window, text="双击课程查看学生成绩", font=("宋体", 12)).pack(pady=10)

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

            def on_course_double_click(event):
                """处理双击课程事件"""
                # 获取双击的行
                item = tree.selection()[0]
                # 获取课程信息
                course_info = tree.item(item, "values")
                # 根据课程信息获取学生成绩
                course_id = course_info[0]  # 假设课程号是第一个元素
                scores = self.__handle_client.send_request({"action": "get_student_scores", "course_id": course_id})
                status = scores.get("status")

                if status == "success":
                    scores = scores.get("datas")
                    if scores:
                        # 展示学生成绩
                        self.show_student_scores(scores)
                    else:
                        messagebox.showinfo("提示", "该课程没有学生选课")
                else:
                    messagebox.showerror("错误", "获取学生成绩失败")

            # 绑定双击事件
            tree.bind("<Double-1>", on_course_double_click, "+")
        else:
            messagebox.showerror("错误", "获取课程信息失败")

    def show_student_scores(self, scores):
        score_window = tk.Toplevel(self.teacher_window)

        # 创建表格显示成绩
        tree = ttk.Treeview(score_window, columns=("学号", "姓名", "班级", "课程名", "成绩"), show="headings")
        tree.heading("学号", text="学号")
        tree.heading("姓名", text="姓名")
        tree.heading("班级", text="班级")
        tree.heading("课程名", text="课程名")
        tree.heading("成绩", text="成绩")

        for score in scores:
            tree.insert("", "end", values=score)

        tree.pack()

    def enter_grades(self):
        """双击修改成绩"""
        grades_window = tk.Toplevel(self.teacher_window)
        grades_window.title("修改成绩")
        grades_window.geometry("600x400")

        # 设置提示标签
        ttk.Label(grades_window, text="双击修改成绩", font=("宋体", 12)).pack(pady=10)

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

        # 成绩表格
        columns = ("student_id", "student_name", "score")
        tree = ttk.Treeview(grades_window, columns=columns, show="headings")
        tree.heading("student_id", text="学号")
        tree.heading("student_name", text="姓名")
        tree.heading("classname", text="班级")
        tree.heading("course", text="课程")
        tree.heading("score", text="成绩")
        tree.pack(fill=tk.BOTH, expand=True, pady=10)

        def load_grades():
            """加载成绩信息"""
            selected_course = course_var.get()
            if not selected_course:
                messagebox.showwarning("警告", "请选择课程")
                return

            course_id = selected_course.split(" ")[0]
            response = self.__handle_client.send_request({"action": "get_student_scores", "course_id": course_id})
            if not response.get("status"):
                messagebox.showerror("错误", "获取成绩信息失败")
                return

            # 清空表格
            for row in tree.get_children():
                tree.delete(row)

            # 插入数据
            for student_score in response.get("datas", []):
                tree.insert("", tk.END, values=(student_score))

        def on_double_click(event):
            """双击修改成绩"""
            item = tree.selection()[0]
            student_id, student_name, old_score = tree.item(item, "values")

            def save_new_score():
                new_score = score_entry.get().strip()
                try:
                    new_score = float(new_score)
                except ValueError:
                    messagebox.showwarning("警告", "成绩必须是数字")
                    return

                selected_course = course_var.get()
                course_id = selected_course.split(" ")[0]

                # 提交修改
                request = {
                    "action": "update_scores",
                    "course_id": course_id,
                    "student_id": student_id,
                    "score": new_score
                }
                response = self.__handle_client.send_request(request)
                if response.get("status") == "success":
                    messagebox.showinfo("提示", "成绩修改成功")
                    tree.item(item, values=(student_id, student_name, new_score))
                    edit_window.destroy()
                else:
                    messagebox.showerror("错误", "成绩修改失败")

            # 弹出编辑窗口
            edit_window = tk.Toplevel(grades_window)
            edit_window.title("修改成绩")
            ttk.Label(edit_window, text=f"学号: {student_id}").pack(pady=5)
            ttk.Label(edit_window, text=f"姓名: {student_name}").pack(pady=5)
            ttk.Label(edit_window, text="修改成绩:").pack(pady=5)
            score_entry = ttk.Entry(edit_window)
            score_entry.insert(0, old_score)
            score_entry.pack(pady=5)
            ttk.Button(edit_window, text="保存", command=save_new_score).pack(pady=10)

        tree.bind("<Double-1>", on_double_click)

        # 加载按钮
        ttk.Button(grades_window, text="加载成绩", command=load_grades).pack(pady=5)
        ttk.Button(grades_window, text="关闭", command=grades_window.destroy).pack(pady=5)


# 以下代码用于测试
if __name__ == '__main__':
    root = tk.Tk()
    handle_client = HandleClient()
    app = TeacherView(root, handle_client, "T001")  # 假设教师ID为 T001
    app.open_teacher_interface()
    root.mainloop()
