-- 插入些测试数据

-- 插入 account 表数据
INSERT INTO account (account, password, category) VALUES
('test_student', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'student'),    -- 密码：123
('test_teacher', 'b3a8e0e1f9ab1bfe3a36f231f676f78bb30a519d2b21e6c530c0eee8ebb4a5d0', 'teacher'),    -- 密码：456
('test_admin', '35a9e381b1a27567549b5f8a6f783c167ebf809f1c4d6a9e367240484d8ce281', 'admin'),        -- 密码：789
('test_student_2', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'student'),  -- 密码：123
('test_teacher_2', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'teacher'),  -- 密码：123
('student_3', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'student'),        -- 密码：123
('student_4', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'student'),        -- 密码：123
('teacher_3', 'b3a8e0e1f9ab1bfe3a36f231f676f78bb30a519d2b21e6c530c0eee8ebb4a5d0', 'teacher'),        -- 密码：456
('teacher_4', 'b3a8e0e1f9ab1bfe3a36f231f676f78bb30a519d2b21e6c530c0eee8ebb4a5d0', 'teacher');        -- 密码：456

-- 插入 class 表数据
INSERT INTO class (classname) VALUES
('ClassA'),
('ClassB'),
('ClassC'),
('ClassD'),
('ClassE'),
('ClassF');

-- 插入 admin 表数据
INSERT INTO admin (id, account_id, level) VALUES
('admin_1', 3, 'high'),
('admin_2', 6, 'medium');

-- 插入 student 表数据
INSERT INTO student (id, account_id, name, sex, department, classname) VALUES
('stu_1', 1, 'Alice', 'female', 'Computer Science', 'ClassA'),
('stu_2', 4, 'Bob', 'male', 'Mathematics', 'ClassB'),
('stu_3', 6, 'Charlie', 'male', 'Physics', 'ClassC'),
('stu_4', 7, 'Diana', 'female', 'Computer Science', 'ClassA'),
('stu_5', 8, 'Eva', 'female', 'Mathematics', 'ClassB'),
('stu_6', 9, 'Frank', 'male', 'Physics', 'ClassD');

-- 插入 course 表数据
INSERT INTO course (id, coursename, credit) VALUES
(1, 'Math 101', 3),
(2, 'Programming 101', 4),
(3, 'English 101', 2),
(4, 'Physics 101', 3),
(5, 'History 101', 2),
(6, 'Data Structures', 4),
(7, 'Machine Learning', 3),
(8, 'Database Systems', 4);

-- 插入 teacher 表数据
INSERT INTO teacher (id, account_id, name, sex, department) VALUES
('teacher_1', 2, 'Dr.Smith', 'male', 'Computer Science'),
('teacher_2', 5, 'Ms.Johnson', 'female', 'Mathematics'),
('teacher_3', 8, 'Dr.Adams', 'male', 'Physics'),
('teacher_4', 9, 'Dr.Brown', 'female', 'Computer Science');

-- 插入 student_course 表数据
INSERT INTO student_course (sid, cid, score) VALUES
('stu_1', 1, 85),
('stu_1', 2, 90),
('stu_1', 3, 92),
('stu_2', 2, 78),
('stu_2', 3, 88),
('stu_2', 1, 81),
('stu_3', 4, 89),
('stu_3', 5, 76),
('stu_4', 2, 95),
('stu_4', 6, 87),
('stu_5', 1, 88),
('stu_5', 7, 91),
('stu_6', 4, 72),
('stu_6', 8, 84);

-- 插入 teacher_course 表数据
INSERT INTO teacher_course (tid, cid, class) VALUES
('teacher_1', 2, 'ClassA'),
('teacher_2', 1, 'ClassB'),
('teacher_2', 3, 'ClassC'),
('teacher_1', 6, 'ClassA'),
('teacher_2', 7, 'ClassB'),
('teacher_3', 4, 'ClassC'),
('teacher_4', 8, 'ClassD'),
('teacher_4', 5, 'ClassE');


-- 查看表
SELECT * FROM account;

SELECT * FROM class;

SELECT * FROM admin;

SELECT * FROM student;

SELECT * FROM course;

SELECT * FROM teacher;

SELECT * FROM student_course;

SELECT * FROM teacher_course;