import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from Controller.handle_client import HandleClient


class AdminView:
    def __init__(self, root, handle_client, id):
        self.admin_window = root
        self.__handle_client = handle_client
        self.__id = id

    def open_admin_interface(self):
        self.admin_window.title("管理员界面")
        self.admin_window.geometry("400x300")
        title_label = ttk.Label(self.admin_window, text="学生选课管理系统", font=("宋体", 16, "bold"))
        title_label.grid(row=0, padx=10, pady=10)

        # 配置行和列的权重，使标签居中
        self.admin_window.grid_rowconfigure(0, weight=1)
        self.admin_window.grid_columnconfigure(0, weight=1)

        style = ttk.Style()
        style.configure('TButton', font=('黑体', 12))

        btn_show_student_info = ttk.Button(self.admin_window, text="显示学生信息", command=self.show_student_info,
                                           style="TButton", width=20)
        btn_show_student_info.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        btn_modify_student_info = ttk.Button(self.admin_window, text="修改学生信息", command=self.modify_student_info,
                                             style="TButton", width=20)
        btn_modify_student_info.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        btn_enter_course = ttk.Button(self.admin_window, text="录入课程信息", command=self.enter_course,
                                      style="TButton", width=20)
        btn_enter_course.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)

        btn_modify_score = ttk.Button(self.admin_window, text="修改成绩", command=self.modify_score, style="TButton",
                                      width=20)
        btn_modify_score.grid(row=4, column=0, sticky="nsew", padx=10, pady=10)

        btn_assign_course = ttk.Button(self.admin_window, text="分配教师任教课程", command=self.assign_course,
                                       style="TButton", width=20)
        btn_assign_course.grid(row=5, column=0, sticky="nsew", padx=10, pady=10)

        btn_assign_account = ttk.Button(self.admin_window, text="修改账号密码", command=self.modify_passwd,
                                        style="TButton", width=20)
        btn_assign_account.grid(row=6, column=0, sticky="nsew", padx=10, pady=10)

        self.admin_window.columnconfigure(0, weight=1)
        for i in range(7):
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

    def modify_student_info(self):
        response = self.__handle_client.send_request({"action": "show_student_info"})
        status = response['status']
        if status:
            students = response["datas"]
            modify_window = tk.Toplevel(self.admin_window)
            modify_window.title("修改学生信息")

            ttk.Label(modify_window, text="双击修改信息").pack()

            tree = ttk.Treeview(modify_window, columns=("学号", "账号ID", "姓名", "性别", "所在学院", "班级"),
                                show="headings")
            tree.heading("学号", text="学号")
            tree.heading("账号ID", text="账号ID")
            tree.heading("姓名", text="姓名")
            tree.heading("性别", text="性别")
            tree.heading("所在学院", text="所在学院")
            tree.heading("班级", text="班级")

            # 禁止双击排序列标题
            tree.bind("<Double-1>", lambda e: "break")

            # 向树形表格中插入数据
            for student in students:
                tree.insert("", "end", values=student)
            tree.pack()

            # 允许编辑单元格
            def start_edit(event):
                # 获取用户双击的列
                col = tree.identify_column(event.x)
                if col == "#1" or col == "#2":  # 如果点击的是“学号”/“账户ID”列，不允许编辑
                    return

                col_index = int(col[1:]) - 1  # 解析列索引
                item = tree.selection()[0]
                value = tree.item(item, "values")[col_index]  # 获取选中的单元格的当前值

                # 创建编辑框，并将其放置在对应单元格的位置
                bbox = tree.bbox(item, col)  # 获取单元格的位置
                x, y, width, height = bbox
                entry = tk.Entry(tree)
                entry.insert(0, value)  # 设置当前值为输入框的默认值
                entry.place(x=x, y=y, width=width, height=height)

                def update_value(event=None):
                    # 更新树形表格中的值
                    new_value = entry.get()
                    values = list(tree.item(item, "values"))
                    values[col_index] = new_value
                    tree.item(item, values=values)  # 更新树形表格中的数据

                    # 删除输入框
                    entry.destroy()

                # 绑定回车和失去焦点事件，确保用户完成编辑时会保存修改
                entry.bind("<FocusOut>", update_value)
                entry.bind("<Return>", update_value)
                entry.focus_set()

            # 绑定双击事件，触发开始编辑
            tree.bind("<Double-1>", start_edit)

            # 保存按钮，保存修改的学生信息
            save_btn = ttk.Button(modify_window, text="保存", command=lambda: self.save_student_changes(tree),
                                  style="TButton")
            save_btn.pack()
        else:
            messagebox.showerror("错误", "修改学生信息失败")
            print("修改学生信息失败")

    def save_student_changes(self, tree):
        # 提取当前表格中的所有数据并发送请求
        updated_students = []
        for item in tree.get_children():
            values = tree.item(item, "values")
            updated_students.append({
                "student_id": values[0],  # 学号
                "account_id": values[1],  # 账号ID
                "name": values[2],  # 姓名
                "gender": values[3],  # 性别
                "school": values[4],  # 所在学院
                "class": values[5]  # 班级
            })
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

        resp = self.__handle_client.send_request({"action": "show_course_info"})
        if resp and resp.get("status") == "success":
            courses = resp.get("datas")
            for course in courses:
                tree.insert("", "end", values=course)
        else:
            messagebox.showerror("错误", "获取课程信息失败")
            return

        add_course_btn = ttk.Button(course_window, text="添加", command=lambda: self.admin_add_course(tree),
                                    style="TButton")
        add_course_btn.pack()

    def admin_add_course(self, tree):
        # 创建新窗口用于录入课程信息
        add_course_window = tk.Toplevel(self.admin_window)
        add_course_window.title("添加课程信息")

        # 创建输入框及标签
        tk.Label(add_course_window, text="课程号:").grid(row=0, column=0, padx=10, pady=5)
        course_id_entry = tk.Entry(add_course_window)
        course_id_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(add_course_window, text="课程名:").grid(row=1, column=0, padx=10, pady=5)
        course_name_entry = tk.Entry(add_course_window)
        course_name_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(add_course_window, text="学分:").grid(row=2, column=0, padx=10, pady=5)
        credit_entry = tk.Entry(add_course_window)
        credit_entry.grid(row=2, column=1, padx=10, pady=5)

        # 提交按钮
        def submit_course():
            course_id = course_id_entry.get().strip()
            course_name = course_name_entry.get().strip()
            credit = credit_entry.get().strip()

            if not (course_id and course_name and credit):
                messagebox.showwarning("警告", "请完整填写所有信息")
                return

            response = self.__handle_client.send_request(
                {"action": "add_course", "course_id": course_id, "course_name": course_name, "credit": credit})
            if response and response.get("status") == "success":
                tree.insert("", "end", values=(course_id, course_name, credit))  # 更新Treeview
                messagebox.showinfo("提示", "课程添加成功")
                add_course_window.destroy()  # 关闭窗口
            else:
                messagebox.showerror("错误", "添加课程失败")

        ttk.Button(add_course_window, text="提交", command=submit_course).grid(row=3, column=0, columnspan=2, pady=10)

        add_course_window.transient(self.admin_window)  # 设置为模态窗口
        add_course_window.grab_set()
        add_course_window.mainloop()

    def assign_course(self):
        try:
            assign_window = tk.Toplevel(self.admin_window)
            assign_window.title("分配教师任教课程")
            # 设置窗口大小
            assign_window.geometry("400x300")

            # 创建并配置样式，调整字体大小
            style = ttk.Style()
            style.configure('TLabel', font=('黑体', 12))
            style.configure('TEntry', font=('黑体', 12))

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
        student_id_window.title("请输入学生学号")
        # 设置窗口大小
        student_id_window.geometry("300x200")

        # 创建并配置样式，调整字体大小
        style = ttk.Style()
        style.configure('TLabel', font=('黑体', 12))
        style.configure('TEntry', font=('黑体', 12))

        # 标签与输入框
        ttk.Label(student_id_window, text="学生学号：").pack(pady=5)
        student_id_entry = ttk.Entry(student_id_window)
        student_id_entry.pack(pady=5)

        def fetch_scores():
            stu_id = student_id_entry.get().strip()
            if not stu_id:
                messagebox.showwarning("警告", "请输入学生学号")
                return
            resp = self.__handle_client.send_request({"action": "stu_id2account_id", "stu_id": stu_id})
            status = resp.get("status")
            if status == "success":
                student_account_id = resp.get("datas")
            else:
                messagebox.showerror("错误", "获取学生学号失败")
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
        score_window.title(f"ID{student_id} 的成绩")

        ttk.Label(score_window, text="学生成绩", font=("宋体", 16, "bold")).pack(pady=10)
        ttk.Label(score_window, text=f"双击修改成绩").pack(pady=5)

        # 创建表格显示成绩
        tree = ttk.Treeview(score_window, columns=("课程号", "课程名", "成绩"), show="headings")
        tree.heading("课程号", text="课程号")
        tree.heading("课程名", text="课程名")
        tree.heading("成绩", text="成绩")

        for score in scores:
            tree.insert("", "end", values=score)

        tree.pack()

        # 允许编辑单元格
        def start_edit(event):
            col = tree.identify_column(event.x)
            if col == "#1" or col == "#2":  # 禁止编辑“课程号”和“课程名”列
                return

            col_index = int(col[1:]) - 1  # 获取列索引
            item = tree.selection()[0]
            value = tree.item(item, "values")[col_index]

            # 获取单元格的位置
            bbox = tree.bbox(item, col)
            if not bbox:
                return
            x, y, width, height = bbox

            # 创建输入框并放置在单元格上
            entry = tk.Entry(tree)
            entry.insert(0, value)
            entry.place(x=x, y=y, width=width, height=height)

            def update_value(event=None):
                new_value = entry.get()
                values = list(tree.item(item, "values"))
                values[col_index] = new_value  # 更新对应列的值
                tree.item(item, values=values)  # 更新树形表格
                entry.destroy()  # 删除输入框

            # 绑定事件
            entry.bind("<FocusOut>", update_value)
            entry.bind("<Return>", update_value)
            entry.focus_set()

        # 绑定双击事件
        tree.bind("<Double-1>", start_edit)

        # 保存按钮
        save_btn = ttk.Button(score_window, text="保存", command=lambda: self.save_score_changes(tree, student_id),
                              style="TButton")
        save_btn.pack(pady=10)

    def save_score_changes(self, tree, student_id):
        for item in tree.get_children():
            course_id = tree.item(item, "values")[0]
            score = tree.item(item, "values")[2]
            response = self.__handle_client.send_request(
                {"action": "update_scores", "course_id": course_id, "student_id": student_id, "score": score})
            if not response or response.get("status") == "error":
                messagebox.showerror("错误", "更新成绩失败")
                print("更新成绩失败")
        messagebox.showinfo("提示", "成绩已更新")
        print("成绩更新成功")

    def modify_passwd(self):
        modify_window = tk.Toplevel(self.admin_window)
        modify_window.title("修改账号密码")
        # 设置窗口大小
        modify_window.geometry("300x200")

        # 创建并配置样式，调整字体大小
        style = ttk.Style()
        style.configure('TLabel', font=('黑体', 12))
        style.configure('TEntry', font=('黑体', 12))

        # 创建标签与输入框
        ttk.Label(modify_window, text="请输入账户ID：").pack(pady=5)
        account_id_entry = ttk.Entry(modify_window)
        account_id_entry.pack(pady=5)

        ttk.Label(modify_window, text="请输入新密码：").pack(pady=5)
        new_passwd_entry = ttk.Entry(modify_window, show="*")
        new_passwd_entry.pack(pady=5)

        def update_passwd():
            account_id = account_id_entry.get().strip()
            new_passwd = new_passwd_entry.get().strip()
            if not new_passwd:
                messagebox.showwarning("警告", "密码不能为空")
                return

            # 请求修改密码
            response = self.__handle_client.send_request(
                {"action": "modify_passwd", "account_id": account_id, "new_password": new_passwd})
            if response and response.get("status") == "success":
                messagebox.showinfo("提示", "密码修改成功")
                print("密码修改成功")
            else:
                messagebox.showerror("错误", "密码修改失败")
                print("密码修改失败")

        modify_btn = ttk.Button(modify_window, text="修改密码", command=update_passwd, style="TButton")
        modify_btn.pack(pady=10)


if __name__ == '__main__':
    root = tk.Tk()
    handle_client = HandleClient()
    admin_view = AdminView(root, handle_client, "test_id")
    admin_view.open_admin_interface()
    root.mainloop()
