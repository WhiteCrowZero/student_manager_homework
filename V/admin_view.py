import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from C.handle_client import HandleClient


class AdminView:
    def __init__(self, root, handle_client, id):
        self.admin_window = root
        self.__handle_client = handle_client
        self.__id = id

    def open_admin_interface(self):
        self.admin_window.title("管理员界面")
        self.admin_window.geometry("400x300")

        button_font = ("宋体", 15, "bold")

        btn_show_student_info = ttk.Button(self.admin_window, text="显示学生信息", command=self.show_student_info,
                                           style="TButton")
        btn_show_student_info.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        btn_modify_student_info = ttk.Button(self.admin_window, text="修改学生信息", command=self.modify_student_info,
                                             style="TButton")
        btn_modify_student_info.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        btn_enter_course = ttk.Button(self.admin_window, text="录入课程信息", command=self.enter_course,
                                      style="TButton")
        btn_enter_course.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        btn_modify_score = ttk.Button(self.admin_window, text="修改成绩", command=self.modify_score, style="TButton")
        btn_modify_score.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)

        btn_assign_course = ttk.Button(self.admin_window, text="分配教师任教课程", command=self.assign_course,
                                       style="TButton")
        btn_assign_course.grid(row=4, column=0, sticky="nsew", padx=10, pady=10)

        btn_assign_account = ttk.Button(self.admin_window, text="修改账号密码", command=self.modify_passwd,
                                        style="TButton")
        btn_assign_account.grid(row=5, column=0, sticky="nsew", padx=10, pady=10)

        self.admin_window.columnconfigure(0, weight=1)
        for i in range(5):
            self.admin_window.rowconfigure(i, weight=1)

        self.admin_window.mainloop()

    def show_student_info(self):
        response = self.__handle_client.send_request({"action": "show_student_info"})
        status = response['status']
        if status == 'success':
            info_window = tk.Toplevel(self.admin_window)
            info_window.title("学生信息")

            tree = ttk.Treeview(info_window, columns=("学号", "账号ID", "姓名", "性别", "所在学院", "班级"),
                                show="headings")
            tree.heading("学号", text="学号")
            tree.heading("账号ID", text="账号ID")
            tree.heading("姓名", text="姓名")
            tree.heading("性别", text="性别")
            tree.heading("所在学院", text="所在学院")
            tree.heading("班级", text="班级")

            students = response["datas"]
            for student in students:
                tree.insert("", "end", values=student)
            tree.pack()
        else:
            messagebox.showerror("错误", "获取学生信息失败")
            print("获取学生信息失败")

    # 下面的UI要改成可编辑的
    def modify_student_info(self):
        response = self.__handle_client.send_request({"action": "show_student_info"})
        status = response['status']
        if status:
            students = response["datas"]
            modify_window = tk.Toplevel(self.admin_window)
            modify_window.title("修改学生信息")

            tree = ttk.Treeview(modify_window, columns=("学号", "账号ID", "姓名", "性别", "所在学院", "班级"),
                                show="headings")
            tree.heading("学号", text="学号")  # 要设置成只读，因为是主键
            tree.heading("账号ID", text="账号ID")
            tree.heading("姓名", text="姓名")
            tree.heading("性别", text="性别")
            tree.heading("所在学院", text="所在学院")
            tree.heading("班级", text="班级")

            for student in students:
                tree.insert("", "end", values=student)

            tree.pack()

            save_btn = ttk.Button(modify_window, text="保存", command=lambda: self.save_student_changes(tree), style="TButton")
            save_btn.pack()
        else:
            messagebox.showerror("错误", "修改学生信息失败")
            print("修改学生信息失败")

    def save_student_changes(self, tree):
        updated_students = []
        for item in tree.get_children():
            values = tree.item(item)["values"]
            updated_students.append(values)
        response = self.__handle_client.send_request(
            {"action": "update_students", "updated_students": updated_students})
        if response and response.get("status") == "success":
            messagebox.showinfo("提示", "学生信息已更新")
            print("学生信息已更新")
        else:
            messagebox.showerror("错误", "更新学生信息失败")
            print("更新学生信息失败")

    def enter_course(self):
        course_window = tk.Toplevel(self.admin_window)
        course_window.title("录入课程信息")

        tree = ttk.Treeview(course_window, columns=("课程号", "课程名", "学分"), show="headings")
        tree.heading("课程号", text="课程号")
        tree.heading("课程名", text="课程名")
        tree.heading("学分", text="学分")

        tree.pack()

        add_course_btn = ttk.Button(course_window, text="添加", command=lambda: self.add_course(tree), style="TButton")
        add_course_btn.pack()

    def add_course(self, tree):
        course_id = simpledialog.askstring("课程号", "请输入课程号")
        course_name = simpledialog.askstring("课程名", "请输入课程名")
        credit = simpledialog.askstring("学分", "请输入学分")

        if course_id and course_name and credit:
            response = self.__handle_client.send_request(
                {"action": "add_course", "course_id": course_id, "course_name": course_name, "credit": credit})
            if response and response.get("status") == "success":
                tree.insert("", "end", values=(course_id, course_name, credit))
                messagebox.showinfo("提示", "课程信息已更新")
                print("课程添加成功")
            else:
                messagebox.showerror("错误", "添加课程失败")
                print("添加课程失败")
        else:
            messagebox.showwarning("警告", "请输入完整信息")
            print("请输入完整信息")
    def assign_course(self):
        try:
            assign_window = tk.Toplevel(self.admin_window)
            assign_window.title("分配教师任教课程")

            # 输入框及标签
            ttk.Label(assign_window, text="课程号:").pack(pady=5)
            course_id_entry = ttk.Entry(assign_window)
            course_id_entry.pack(pady=5)

            ttk.Label(assign_window, text="教师工号:").pack(pady=5)
            teacher_id_entry = ttk.Entry(assign_window)
            teacher_id_entry.pack(pady=5)

            ttk.Label(assign_window, text="教学班级:").pack(pady=5)
            class_name_entry = ttk.Entry(assign_window)
            class_name_entry.pack(pady=5)

            # 分配按钮
            def assign_teacher():
                course_id = course_id_entry.get().strip()
                teacher_id = teacher_id_entry.get().strip()
                class_name = class_name_entry.get().strip()

                if not course_id or not teacher_id:
                    messagebox.showwarning("警告", "课程号和教师工号不能为空")
                    return

                # 发送分配请求
                response = self.__handle_client.send_request(
                    {"action": "assign_teacher", "teacher_id": teacher_id, "course_id": course_id,
                     "class_name": class_name}
                )
                if response and response.get("status") == "success":
                    messagebox.showinfo("提示", "教师分配成功")
                    print("教师分配成功")
                else:
                    messagebox.showerror("错误", "教师分配失败")
                    print("教师分配失败")

            assign_btn = ttk.Button(assign_window, text="分配", command=assign_teacher, style="TButton")
            assign_btn.pack(pady=10)

        except Exception as e:
            messagebox.showerror("错误", "无法创建分配窗口")
            print(e)

    def modify_score(self):
        # 创建窗口
        student_id_window = tk.Toplevel(self.admin_window)
        student_id_window.title("请输入学生账户ID")

        # 标签与输入框
        ttk.Label(student_id_window, text="学生账户ID：").pack(pady=5)
        student_id_entry = ttk.Entry(student_id_window)
        student_id_entry.pack(pady=5)

        def fetch_scores():
            student_account_id = student_id_entry.get().strip()
            if not student_account_id:
                messagebox.showwarning("警告", "请输入学生账户ID")
                return

            # 发送请求获取学生成绩
            response = self.__handle_client.send_request(
                {"action": "show_student_course_score", "student_id": student_account_id})
            status = response.get("status")
            if status == 'success':
                scores = response.get("datas")
                student_id_window.destroy()  # 关闭输入窗口
                self.show_scores_window(scores, student_account_id)
            else:
                messagebox.showerror("错误", "获取学生成绩失败")
                print("获取学生成绩失败")

        fetch_btn = ttk.Button(student_id_window, text="查询", command=fetch_scores, style="TButton")
        fetch_btn.pack(pady=10)

    def show_scores_window(self, scores, student_id):
        score_window = tk.Toplevel(self.admin_window)
        score_window.title(f"{student_id} 的成绩")

        # 创建表格显示成绩
        tree = ttk.Treeview(score_window, columns=("课程号", "课程名", "学分", "成绩"), show="headings")
        tree.heading("课程号", text="课程号")
        tree.heading("课程名", text="课程名")
        tree.heading("学分", text="学分")
        tree.heading("成绩", text="成绩")

        for score in scores:
            tree.insert("", "end", values=score)

        tree.pack()

        # 保存按钮
        save_btn = ttk.Button(score_window, text="保存", command=lambda: self.save_score_changes(tree, student_id),
                              style="TButton")
        save_btn.pack(pady=10)

    def save_score_changes(self, tree, student_id):
        updated_scores = []
        for item in tree.get_children():
            values = tree.item(item)["values"]
            updated_scores.append(values)
        response = self.__handle_client.send_request(
            {"action": "update_scores", "updated_scores": updated_scores, "student_id": student_id})
        if response and response.get("status") == "success":
            messagebox.showinfo("提示", "成绩已更新")
            print("成绩更新成功")
        else:
            messagebox.showerror("错误", "更新成绩失败")
            print("更新成绩失败")

    def modify_passwd(self):
        modify_window = tk.Toplevel(self.admin_window)
        modify_window.title("修改账号密码")

        # 创建标签与输入框
        ttk.Label(modify_window, text="请输入新密码：").pack(pady=5)
        new_passwd_entry = ttk.Entry(modify_window, show="*")
        new_passwd_entry.pack(pady=5)

        def update_passwd():
            new_passwd = new_passwd_entry.get().strip()
            if not new_passwd:
                messagebox.showwarning("警告", "密码不能为空")
                return

            # 请求修改密码
            response = self.__handle_client.send_request(
                {"action": "modify_passwd", "new_passwd": new_passwd})
            if response and response.get("status") == "success":
                messagebox.showinfo("提示", "密码修改成功")
                print("密码修改成功")
            else:
                messagebox.showerror("错误", "密码修改失败")
                print("密码修改失败")

        modify_btn = ttk.Button(modify_window, text="修改密码", command=update_passwd, style="TButton")
        modify_btn.pack(pady=10)


