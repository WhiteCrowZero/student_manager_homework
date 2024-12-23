import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from C.handle_client import HandleClient


class AdminView:
    def __init__(self, root, handle_client):
        self.root = root
        self.admin_window = None
        self.__handle_client = handle_client

    def open_admin_interface(self):
        self.admin_window = tk.Toplevel(self.root)
        self.admin_window.title("管理员界面")
        self.admin_window.geometry("400x300")

        button_font = ("宋体", 15, "bold")

        btn_show_student_info = tk.Button(self.admin_window, text="显示学生信息", command=self.show_student_info,
                                          font=button_font)
        btn_show_student_info.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        btn_modify_student_info = tk.Button(self.admin_window, text="修改学生信息", command=self.modify_student_info,
                                            font=button_font)
        btn_modify_student_info.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        btn_enter_course = tk.Button(self.admin_window, text="录入课程信息", command=self.enter_course,
                                     font=button_font)
        btn_enter_course.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        btn_modify_score = tk.Button(self.admin_window, text="修改成绩", command=self.modify_score, font=button_font)
        btn_modify_score.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)

        btn_assign_course = tk.Button(self.admin_window, text="分配教师任教课程", command=self.assign_course,
                                      font=button_font)
        btn_assign_course.grid(row=4, column=0, sticky="nsew", padx=10, pady=10)

        btn_assign_account = tk.Button(self.admin_window, text="修改账号密码", command=self.modify_passwd,
                                      font=button_font)
        btn_assign_account.grid(row=5, column=0, sticky="nsew", padx=10, pady=10)

        self.admin_window.columnconfigure(0, weight=1)
        for i in range(5):
            self.admin_window.rowconfigure(i, weight=1)


    # 这里具体的传递参数还不清不楚。。。。。。。。。。。。。。。。。。。。。。
    def show_student_info(self):
        response = self.__handle_client.send_request({"action": "show_student_info"})
        status = response['status']
        if status == 'success':
            info_window = tk.Toplevel(self.admin_window)
            info_window.title("学生信息")

            tree = ttk.Treeview(info_window, columns=("学号", "姓名", "性别", "所在学院", "账号"), show="headings")
            tree.heading("学号", text="学号")
            tree.heading("姓名", text="姓名")
            tree.heading("性别", text="性别")
            tree.heading("所在学院", text="所在学院")
            tree.heading("账号", text="账号")

            students = response["students"]
            for student in students:
                tree.insert("", "end", values=(
                    student["学号"], student["姓名"], student["性别"], student["所在学院"], student["账号"]
                ))
            tree.pack()
        else:
            messagebox.showerror("错误", "获取学生信息失败")
            print("获取学生信息失败")

    # 这里的参数也不确定。。。。。。。。。。。。。。。。。。。。。。。。。
    def modify_student_info(self):
        response = self.__handle_client.send_request({"action": "show_student_info"})
        status = response['status']
        if status:
            students = response["datas"]
            modify_window = tk.Toplevel(self.admin_window)
            modify_window.title("修改学生信息")

            tree = ttk.Treeview(modify_window, columns=("学号", "姓名", "性别", "所在学院", "账号", "密码"),
                                show="headings")
            tree.heading("学号", text="学号")
            tree.heading("姓名", text="姓名")
            tree.heading("性别", text="性别")
            tree.heading("所在学院", text="所在学院")
            tree.heading("账号", text="账号")
            tree.heading("密码", text="密码")

            for student in students:
                tree.insert("", "end", values=(
                    student["学号"], student["姓名"], student["性别"], student["所在学院"], student["账号"],
                    student["密码"]))

            tree.pack()

            save_btn = tk.Button(modify_window, text="保存", command=lambda: self.save_student_changes(tree))
            save_btn.pack()
        else:
            messagebox.showerror("错误", "修改学生信息失败")
            print("修改学生信息失败")

    def save_student_changes(self, tree):
        updated_students = []
        for item in tree.get_children():
            values = tree.item(item)["values"]
            updated_students.append(
                {"学号": values[0], "姓名": values[1], "性别": values[2], "所在学院": values[3], "账号": values[4],
                 "密码": values[5]})
        response = self.__handle_client.send_request({"action": "update_students", "data": updated_students})
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

        add_course_btn = tk.Button(course_window, text="添加", command=lambda: self.add_course(tree))
        add_course_btn.pack()

    def add_course(self, tree):
        course_id = simpledialog.askstring("课程号", "请输入课程号")
        course_name = simpledialog.askstring("课程名", "请输入课程名")
        credit = simpledialog.askstring("学分", "请输入学分")

        if course_id and course_name and credit:
            response = self.__handle_client.send_request(
                {"action": "add_course", "data": {"课程号": course_id, "课程名": course_name, "学分": credit}})
            if response and response.get("status") == "success":
                tree.insert("", "end", values=(course_id, course_name, credit))
                messagebox.showinfo("提示", "学生信息已更新")
                print("课程添加成功")
            else:
                messagebox.showerror("错误", "添加课程失败")
                print("添加课程失败")
        else:
            messagebox.showwarning("警告", "请输入完整信息")
            print("请输入完整信息")

    def modify_score(self):
        response = self.__handle_client.send_request({"action": "show_student_scores"})
        status = response['status']
        if status == 'success':
            scores = response["scores"]
            modify_window = tk.Toplevel(self.admin_window)
            modify_window.title("修改成绩")

            tree = ttk.Treeview(modify_window, columns=("学号", "姓名", "课程名", "成绩"), show="headings")
            tree.heading("学号", text="学号")
            tree.heading("姓名", text="姓名")
            tree.heading("课程名", text="课程名")
            tree.heading("成绩", text="成绩")

            for score in scores:
                tree.insert("", "end", values=(
                    score["学号"], score["姓名"], score["课程名"], score["成绩"]
                ))

            tree.pack()

            save_btn = tk.Button(modify_window, text="保存", command=lambda: self.save_score_changes(tree))
            save_btn.pack()
        else:
            messagebox.showerror("错误", "获取学生成绩失败")
            print("获取学生成绩失败")

    def save_score_changes(self, tree):
        updated_scores = []
        for item in tree.get_children():
            values = tree.item(item)["values"]
            updated_scores.append(
                {"学号": values[0], "课程名": values[2], "成绩": values[3]}
            )

        response = self.__handle_client.send_request({"action": "update_scores", "data": updated_scores})
        if response and response.get("status") == "success":
            messagebox.showinfo("提示", "成绩已更新")
            print("成绩已更新")
        else:
            messagebox.showerror("错误", "更新成绩失败")
            print("更新成绩失败")

    def assign_course(self):
        response = self.__handle_client.send_request({"action": "show_courses_teachers"})
        status = response['status']
        if status == 'success':
            courses_teachers = response["courses_teachers"]
            assign_window = tk.Toplevel(self.admin_window)
            assign_window.title("分配教师任教课程")

            tree = ttk.Treeview(assign_window, columns=("课程号", "课程名", "教师工号", "教师姓名"), show="headings")
            tree.heading("课程号", text="课程号")
            tree.heading("课程名", text="课程名")
            tree.heading("教师工号", text="教师工号")
            tree.heading("教师姓名", text="教师姓名")

            for ct in courses_teachers:
                tree.insert("", "end", values=(
                    ct["课程号"], ct["课程名"], ct["教师工号"], ct["教师姓名"]
                ))

            tree.pack()

            assign_btn = tk.Button(assign_window, text="分配", command=lambda: self.assign_teacher_to_course(tree))
            assign_btn.pack()
        else:
            messagebox.showerror("错误", "获取课程与教师信息失败")
            print("获取课程与教师信息失败")

    def assign_teacher_to_course(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("警告", "请选择一项进行分配")
            return

        course_id = tree.item(selected_item[0])["values"][0]
        teacher_id = simpledialog.askstring("教师工号", "请输入要分配的教师工号")

        if teacher_id:
            response = self.__handle_client.send_request(
                {"action": "assign_teacher", "data": {"课程号": course_id, "教师工号": teacher_id}})
            if response and response.get("status") == "success":
                messagebox.showinfo("提示", "教师分配成功")
                print("教师分配成功")
            else:
                messagebox.showerror("错误", "教师分配失败")
                print("教师分配失败")
        else:
            messagebox.showwarning("警告", "请输入教师工号")
            print("教师工号为空")

    def modify_passwd(self):
        modify_window = tk.Toplevel(self.admin_window)
        modify_window.title("修改账号密码")

        tk.Label(modify_window, text="账号:").grid(row=0, column=0, padx=10, pady=10)
        account_entry = tk.Entry(modify_window)
        account_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(modify_window, text="新密码:").grid(row=1, column=0, padx=10, pady=10)
        password_entry = tk.Entry(modify_window, show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=10)

        def save_new_password():
            account = account_entry.get()
            new_password = password_entry.get()

            if account and new_password:
                response = self.__handle_client.send_request(
                    {"action": "modify_passwd", "data": {"账号": account, "新密码": new_password}})
                if response and response.get("status") == "success":
                    messagebox.showinfo("提示", "密码修改成功")
                    print("密码修改成功")
                else:
                    messagebox.showerror("错误", "密码修改失败")
                    print("密码修改失败")
            else:
                messagebox.showwarning("警告", "请输入完整信息")
                print("账号或密码为空")

        save_btn = tk.Button(modify_window, text="保存", command=save_new_password)
        save_btn.grid(row=2, column=0, columnspan=2, pady=10)


if __name__ == '__main__':
    root = tk.Tk()
    client = HandleClient()
    app = AdminView(root, client)
    app.open_admin_interface()
    root.mainloop()
