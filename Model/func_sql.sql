-- 1. 验证用户身份
SELECT account_id, category
FROM account
WHERE account = ? AND password = ?;

-- 2. 显示单个学生信息
SELECT id, name, sex, department, classname
FROM student
WHERE account_id = ?;

-- 3. 显示学生课程
SELECT course.id, coursename, credit, name
FROM course
LEFT JOIN teacher_course ON course.id = teacher_course.cid
LEFT JOIN teacher ON teacher_course.tid = teacher.id
WHERE class = (SELECT classname FROM student WHERE account_id = ?);

-- 4. 显示学生课程成绩
SELECT student_course.cid, course.coursename, student_course.score
FROM student_course
LEFT JOIN course ON student_course.cid = course.id
WHERE student_course.sid = (SELECT id FROM student WHERE account_id = ?);

-- 5. 学生选课
INSERT INTO student_course (sid, cid, score)
VALUES ((SELECT id FROM student WHERE account_id = ?), ?, NULL);

-- 6. 获取教师课程
SELECT c.id, c.coursename, c.credit
FROM course c
LEFT JOIN teacher_course ON teacher_course.cid = c.id
WHERE teacher_course.tid = (SELECT id FROM teacher WHERE account_id = ?);

-- 7. 更新成绩
UPDATE student_course
SET score = ?
WHERE sid = ? AND cid = ?;

-- 8. 获取学生成绩
SELECT s.id, s.name, s.classname, c.coursename, sc.score
FROM student s
LEFT JOIN student_course sc ON s.id = sc.sid
LEFT JOIN course c ON sc.cid = c.id
WHERE sc.cid = ?;

-- 9. 显示所有学生信息
SELECT *
FROM student;

-- 10. 更新学生信息
UPDATE student
SET account_id = ?, name = ?, sex = ?, department = ?, classname = ?
WHERE id = ?;

-- 11. 添加课程
INSERT INTO course (id, coursename, credit)
VALUES (?, ?, ?);

-- 12. 分配教师课程
INSERT INTO teacher_course (tid, cid, assignment_date)
VALUES (?, ?, ?);

-- 13. 更新学生成绩（通过账户ID）
UPDATE student_course
SET score = ?
WHERE sid = (SELECT id FROM student WHERE account_id = ?) AND cid = ?;

-- 14. 修改密码
UPDATE account
SET password = ?
WHERE account_id = ?;

-- 15. 显示课程信息
SELECT *
FROM course;
