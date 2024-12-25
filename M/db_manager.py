"""
学生选课系统 SQL
包含
    DatabaseManager 负责与数据库交互处理
"""
import pymysql


class DatabaseManager:
    def __init__(self, host='localhost', port=3306, user='root', password='123456', database='student_course',
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
    def authenticate(self, account, password):
        sql = "SELECT account_id,category FROM account WHERE account = %s AND password = %s"
        try:
            self.cursor.execute(sql, (account, password))
            self.db.commit()
            return self.cursor.fetchone()
        except Exception as e:
            self.db.rollback()
            print(e)
            return False

    """
    学生部分
    """

    def show_student_info_single(self, id):
        sql = "SELECT id, name, sex, department, classname FROM student WHERE account_id = %s"
        try:
            self.cursor.execute(sql, (id,))
            self.db.commit()
            return self.cursor.fetchone()
        except Exception as e:
            self.db.rollback()
            print(e)
            return False

    def show_course(self, account_id):
        sql = ("select course.id, coursename, credit, name  from course left join teacher_course "
               "on course.id = teacher_course.cid "
               "left join teacher on teacher_course.tid = teacher.id "
               "where class = (select classname from student where account_id = %s)")
        try:
            self.cursor.execute(sql, (account_id,))
            self.db.commit()
            return self.cursor.fetchall()
        except Exception as e:
            self.db.rollback()
            print(e)
            return False

    def show_student_course_score(self, id):
        sql = ("SELECT student_course.cid,course.coursename,student_course.score FROM student_course "
               "LEFT JOIN course ON student_course.cid = course.id "
               "WHERE student_course.sid = (select id from student where account_id = %s)")
        try:
            self.cursor.execute(sql, (id,))
            self.db.commit()
            return self.cursor.fetchall()
        except Exception as e:
            self.db.rollback()
            print(e)
            return False

    def select_course(self, id, course_id):
        sql = "insert into student_course values (%s, %s, NULL)"
        try:
            self.cursor.execute(sql, (id, course_id))
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
        sql = "update account set password = %s where account_id = %s"
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
    # a = sql.authenticate('test_student', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3')
    # print(a)
    # a = sql.show_student_info_single(1)
    # print(a)
    # a = sql.show_course(1)
    # print(a)
    sql.close()
