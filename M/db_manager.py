"""
学生选课系统 SQL
包含
    CourseSQL 负责与数据库交互处理
"""
import pymysql


class DatabaseManager:
    def __init__(self, host='localhost', port=3306, user='root', password='123456', database='dict_online',
                 charset='utf8mb4'):
        self.kwargs = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': database,
            'charset': charset
        }
        self.db = pymysql.connect(**self.kwargs)
        self.cursor = self.db.cursor()
        print('连接数据库成功')

    # 处理关闭
    def close(self):
        self.cursor.close()
        self.db.close()

    """
    登录部分
    """

    # 验证用户身份
    def authenticate(self, name, password):
        sql = "SELECT id, role FROM users WHERE username = %s AND password = SHA2(%s, 256)"
        try:
            self.cursor.execute(sql, (name, password))
            self.db.commit()
            return self.cursor.fetchone()[0]
        except Exception as e:
            self.db.rollback()
            print(e)
            return False

    """
    学生部分
    """

    def show_student_info_single(self, id):
        sql = "select * from students where id = %s"
        try:
            self.cursor.execute(sql, (id,))
            self.db.commit()
            return self.cursor.fetchone()[0]
        except Exception as e:
            self.db.rollback()
            print(e)
            return False

    def show_course(self):
        sql = "select * from courses"
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return self.cursor.fetchall()
        except Exception as e:
            self.db.rollback()
            print(e)
            return False

    def show_student_course_score(self, id):
        sql = "select course_name, score from student_course where student_id = %s"
        try:
            self.cursor.execute(sql, (id,))
            self.db.commit()
            return self.cursor.fetchall()
        except Exception as e:
            self.db.rollback()
            print(e)
            return False

    def select_course(self, id, course_name):
        sql = "insert into student_course values (%s, %s)"
        try:
            self.cursor.execute(sql, (id, course_name))
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(e)
            return False

    """
    教师部分
    """

    def get_teacher_courses(self, teacher_id):
        sql = "select courese_id, course_name from teacher_course where teacher_id = %s"
        try:
            self.cursor.execute(sql, (id,))
            self.db.commit()
            return self.cursor.fetchall()
        except Exception as e:
            self.db.rollback()
            print(e)
            return False

    """
    管理员部分
    """

    def update_students(self, students):
        for student in students:
            sql = "update students set name = %s, gender = %s, college = %s, account = %s, password = %s where id = %s"
            try:
                self.cursor.execute(sql, (
                student["姓名"], student["性别"], student["所在学院"], student["账号"], student["密码"],
                student["学号"]))
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                print(e)
                return False
        return True

    def add_course(self, course):
        sql = "insert into courses values (%s, %s, %s)"
        try:
            self.cursor.execute(sql, (course["课程号"], course["课程名"], course["学分"]))
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(e)
            return False

    def assign_teacher(self, course_id, teacher_id):
        sql = "insert into course_teacher values (%s, %s)"
        try:
            self.cursor.execute(sql, (course_id, teacher_id))
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(e)
            return False

    def show_course_students(self, course_id):
        sql = "select * from course_students where course_id = %s"
        try:
            self.cursor.execute(sql, (course_id,))
            self.db.commit()
            return self.cursor.fetchall()
        except Exception as e:
            self.db.rollback()
            print(e)

    def update_scores(self, scores):
        for score in scores:
            sql = "update course_students set score = %s where student_id = %s and course_id = %s"
            try:
                self.cursor.execute(sql, (score["成绩"], score["学号"], score["课程号"]))
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                print(e)
                return False
        return True

    def modify_passwd(self, id, password):
        sql = "update students set password = %s where id = %s"
        try:
            self.cursor.execute(sql, (password, id))
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(e)
            return False

    def show_student_info(self):
        sql = "select * from students"
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return self.cursor.fetchall()
        except Exception as e:
            self.db.rollback()
            print(e)
            return False


if __name__ == '__main__':
    sql = DatabaseManager()
    sql.close()
