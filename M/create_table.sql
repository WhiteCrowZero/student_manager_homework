-- 创建数据库
CREATE DATABASE student_course;
USE student_course;

-- 删除旧表
DROP TABLE IF EXISTS teacher_course;
DROP TABLE IF EXISTS student_course;
DROP TABLE IF EXISTS teacher;
DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS admin;
DROP TABLE IF EXISTS class;
DROP TABLE IF EXISTS account;

-- 创建 account 表（登录账户信息表）
CREATE TABLE account (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    account VARCHAR(20) NOT NULL,
    password VARCHAR(64) NOT NULL,
    category ENUM('student', 'teacher', 'admin') NOT NULL,
    UNIQUE(account, category)
);

-- 创建 class 表
CREATE TABLE class (
    classname VARCHAR(20) PRIMARY KEY
);

-- 创建 admin 表
CREATE TABLE admin (
    id VARCHAR(20) PRIMARY KEY, -- 管理员编号，例如 "A0001"
    account_id INT NOT NULL,
    level ENUM('low', 'medium', 'high') NOT NULL,
    FOREIGN KEY (account_id) REFERENCES account(account_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 创建 student 表
CREATE TABLE student (
    id VARCHAR(20) PRIMARY KEY, -- 学号，例如 "2024010001"
    account_id INT NOT NULL,
    name VARCHAR(20) NOT NULL,
    sex ENUM('male', 'female') NOT NULL,
    department VARCHAR(50) NOT NULL,
    classname VARCHAR(20),
    FOREIGN KEY (account_id) REFERENCES account(account_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (classname) REFERENCES class(classname) ON DELETE SET NULL ON UPDATE CASCADE
);

-- 创建 course 表
CREATE TABLE course (
    id INT AUTO_INCREMENT PRIMARY KEY,
    coursename VARCHAR(30) NOT NULL,
    credit INT NOT NULL CHECK (credit > 0)
);

-- 创建 teacher 表
CREATE TABLE teacher (
    id VARCHAR(20) PRIMARY KEY, -- 工号，例如 "T20230101"
    account_id INT NOT NULL,
    name VARCHAR(20) NOT NULL,
    sex ENUM('male', 'female') NOT NULL,
    department VARCHAR(50) NOT NULL,
    FOREIGN KEY (account_id) REFERENCES account(account_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 创建 student_course 表（学生选课信息）
CREATE TABLE student_course (
    sid VARCHAR(20) NOT NULL, -- 学号
    cid INT NOT NULL,         -- 课程 ID
    score INT CHECK (score BETWEEN 0 AND 100),
    PRIMARY KEY (sid, cid),
    FOREIGN KEY (sid) REFERENCES student(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (cid) REFERENCES course(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 创建 teacher_course 表（教师授课信息）
CREATE TABLE teacher_course (
    tid VARCHAR(20) NOT NULL, -- 工号
    cid INT NOT NULL,         -- 课程 ID
    class VARCHAR(20) NOT NULL,
    PRIMARY KEY (tid, cid, class),
    FOREIGN KEY (tid) REFERENCES teacher(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (cid) REFERENCES course(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (class) REFERENCES class(classname) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 创建索引
CREATE INDEX idx_student_department ON student(department);
CREATE INDEX idx_teacher_department ON teacher(department);
CREATE INDEX idx_student_course_sid ON student_course(sid);
CREATE INDEX idx_student_course_cid ON student_course(cid);
CREATE INDEX idx_teacher_course_tid ON teacher_course(tid);
CREATE INDEX idx_teacher_course_cid ON teacher_course(cid);
