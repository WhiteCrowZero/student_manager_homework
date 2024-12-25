import tkinter as tk
from tkinter import ttk


class StudentAIHelper:
    def __init__(self, student_window, handle_client, id):
        self.student_window = student_window
        self.__handle_client = handle_client
        self.__id = id
        self.ai_window = None
        self.chat_display = None
        self.input_entry = None

    # 主函数：创建 AI 助手窗口
    def ai_for_student(self):
        self.ai_window = tk.Toplevel(self.student_window)
        self.ai_window.title("AI 助手")
        self.ai_window.geometry("600x500")
        self.ai_window.protocol("WM_DELETE_WINDOW", lambda: self.ai_window.destroy())

        # 窗口整体布局
        main_frame = ttk.Frame(self.ai_window, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 聊天显示区域
        self.chat_display = tk.Text(
            main_frame, wrap=tk.WORD, state=tk.DISABLED, bg="#f9f9f9", fg="#333", font=("Arial", 10)
        )
        self.chat_display.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        # 分隔线
        separator = ttk.Separator(main_frame, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, pady=5)

        # 输入框和发送按钮区域
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X)

        self.input_entry = ttk.Entry(input_frame)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        send_button = ttk.Button(input_frame, text="发送", command=self.get_student_input)
        send_button.pack(side=tk.RIGHT)

    # 获取学生输入的问题
    def get_student_input(self):
        question = self.input_entry.get().strip()
        if question:  # 确保输入不为空
            self.add_to_chat("学生", question, "#0078D7")  # 蓝色字体显示学生输入
            self.input_entry.delete(0, tk.END)  # 清空输入框
            courses, response = self.send_question_to_server(question)  # 发送问题到服务端
            self.display_ai_response(courses, response)  # 显示服务端返回的回答

    # 发送问题到服务端
    def send_question_to_server(self, question):
        request = {"action": "ai_for_student", "student_id": self.__id, "question": question}
        resp = self.__handle_client.send_request(request)
        status = resp.get("status")
        if status:
            return resp.get("courses"), resp.get("datas")
        else:
            return "AI 助手暂时无法回答您的问题，请稍后再试。"

    # 显示 AI 助手的回复
    def display_ai_response(self, courses, response):
        self.add_to_chat("你选择的课程及所修学分为：", courses, "#FF1500")  # 色字体显示学生课程
        self.add_to_chat("AI 助手", response, "#FF4500")  # 橙色字体显示 AI 回复

    # 通用方法：添加消息到聊天显示区
    def add_to_chat(self, sender, message, color="#333"):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: ", ("sender",))
        self.chat_display.insert(tk.END, f"{message}\n", ("message", color))
        self.chat_display.tag_configure("sender", font=("Arial", 10, "bold"))
        self.chat_display.tag_configure("message", foreground=color)
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)


if __name__ == '__main__':
    from C.handle_client import HandleClient

    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    client = HandleClient()
    app = StudentAIHelper(root, client, 1)
    app.ai_for_student()
    tk.mainloop()
