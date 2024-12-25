-- 插入些测试数据

-- 插入 account 表数据
INSERT INTO account (account, password, category) VALUES
('test_student', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'student'),    -- 对应密码：123
('test_teacher', 'b3a8e0e1f9ab1bfe3a36f231f676f78bb30a519d2b21e6c530c0eee8ebb4a5d0', 'teacher'),    -- 对应密码：456
('test_admin', '35a9e381b1a27567549b5f8a6f783c167ebf809f1c4d6a9e367240484d8ce281', 'admin'),        -- 对应密码：789
('这是一个学生', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'student'),        -- 对应密码：789
('这是一个老师', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'teacher');        -- 对应密码：789

-- 插入 class 表数据
INSERT INTO class (classname) VALUES
('ClassA'),
('ClassB'),
('ClassC');

-- 插入 admin 表数据
INSERT INTO admin (id, account_id, level) VALUES
('admin_1', 3, 'high'); -- 假设 account_id 为3的账号是 admin1

-- 插入 student 表数据
INSERT INTO student (id, account_id, name, sex, department, classname) VALUES
('stu_1', 1, 'Alice', 'female', 'Computer Science', 'ClassA'),
('stu_2', 4, 'Bob', 'male', 'Mathematics', 'ClassB');

-- 插入 course 表数据
INSERT INTO course (id, coursename, credit) VALUES
(1, 'Math 101', 3),
(2, 'Programming 101', 4),
(3, 'English 101', 2);

-- 插入 teacher 表数据
INSERT INTO teacher (id, account_id, name, sex, department) VALUES
('teacher_1', 2, 'Dr.Smith', 'male', 'Computer Science'),
('teacher_2', 5, 'Ms.Johnson', 'female', 'Mathematics');

-- 插入 student_course 表数据
INSERT INTO student_course (sid, cid, score) VALUES
('stu_1', 1, 85),
('stu_1', 2, 90),
('stu_2', 2, 78),
('stu_2', 3, 88);

-- 插入 teacher_course 表数据
INSERT INTO teacher_course (tid, cid, class) VALUES
('teacher_1', 2, 'ClassA'),
('teacher_2', 1, 'ClassB'),
('teacher_2', 3, 'ClassC');


-- 查看表
SELECT * FROM account;

SELECT * FROM class;

SELECT * FROM admin;

SELECT * FROM student;

SELECT * FROM course;

SELECT * FROM teacher;

SELECT * FROM student_course;

SELECT * FROM teacher_course;