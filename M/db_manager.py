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

    # 处理登录
    def login(self, name, password):
        sql = "select 1 from users where name = BINARY %s and password = %s"
        try:
            self.cursor.execute(sql, (name, password))
            self.db.commit()
            if self.cursor.fetchone():
                return True
            else:
                return False
        except Exception as e:
            self.db.rollback()
            print(e)
            return False

    # 验证用户身份
    def authenticate(self, name, password):
        sql = "SELECT id, username, role FROM users WHERE username = %s AND password = SHA2(%s, 256)"
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

    def view_student_info(self, id):
        sql = "select * from students where id = %s"
        try:
            self.cursor.execute(sql, (id,))
            self.db.commit()
            return self.cursor.fetchone()[0]
        except Exception as e:
            self.db.rollback()
            print(e)
            return False

    def view_course(self, id):
        sql = "select * from courses where id = %s"
        try:
            self.cursor.execute(sql, (id,))
            self.db.commit()
            return self.cursor.fetchone()[0]
        except Exception as e:
            self.db.rollback()
            print(e)
            return False

    def view_score(self, id):
        sql = "select * from scores where id = %s"
        try:
            self.cursor.execute(sql, (id,))
            self.db.commit()
            return self.cursor.fetchone()[0]
        except Exception as e:
            self.db.rollback()
            print(e)
            return False

    """
    教师部分
    """

    def view_class_course(self, id):
        sql = "select * from class_course where id = %s"
        try:
            self.cursor.execute(sql, (id,))
            self.db.commit()
            return self.cursor.fetchone()[0]
        except Exception as e:
            self.db.rollback()
            print(e)
            return False

    def insert_class_course(self, id, course):
        sql = "insert into class_course values (%s, %s)"
        try:
            self.cursor.execute(sql, (id, course))
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(e)
            return False

    """
    管理员部分
    """

    def modify_pwd(self, id, password):
        sql = "update students set password = %s where id = %s"
        try:
            self.cursor.execute(sql, (password, id))
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(e)
            return False

    def create_teacher(self, id, name, password):
        sql = "insert into teachers values (%s, %s)"
        try:
            self.cursor.execute(sql, (id, name, password))
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(e)
            return False


if __name__ == '__main__':
    sql = DatabaseManager()
    sql.close()
