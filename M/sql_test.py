
def select_course(self, id, course_name):
    # 假设student_course表列顺序是(sid, cid)，先查询课程id
    sql_course_id = "SELECT id FROM course WHERE coursename = %s"
    conn = mysql.connector.connect(user='your_user', password='your_password', host='your_host',
                                   database='your_database')
    cursor = conn.cursor()
    cursor.execute(sql_course_id, (course_name,))
    course_id = cursor.fetchone()[0]
    sql = "INSERT INTO student_course (sid, cid) VALUES (%s, %s)"
    cursor.execute(sql, (id, course_id))
    conn.commit()
    cursor.close()
    conn.close()

       #"教师部分"#

def get_teacher_courses(self, teacher_id, course=None):
    sql = ("SELECT teacher_course.tid, c.coursename, teacher_course.cid FROM teacher_course "
           "JOIN course c ON teacher_course.cid = c.id "
           "WHERE teacher_course.tid = %s")

    #管理员部分#

def update_students(self, students):
    for student in students:
        sql = "UPDATE student SET name=%s,sex=%s,department=%s,classname=%s,account_id=%s WHERE id=%s"
        values = (student['name'], student['sex'], student['department'], student['classname'], student['account_id'],
                  student['id'])

def add_course(self, course):
    sql = "INSERT INTO course (id, coursename, credit) VALUES (%s, %s, %s)"

def assign_teacher(self, cid, tid, class_):
    sql = "INSERT INTO teacher_course (tid, cid, class) VALUES (%s, %s, %s)"

def show_course_students(self, cid):
    sql = "SELECT * FROM student_course WHERE cid = %s "

def update_scores(self, scores):
    for score in scores:
        sql = "UPDATE student_course SET score = %s WHERE sid = %s AND cid = %s"
        values = (score['score'], score['sid'], score['cid'])


def show_student_info(self):
    sql = "SELECT * FROM student"