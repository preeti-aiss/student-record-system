CREATE DATABASE IF NOT EXISTS school;
USE school;

-- students table
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    class VARCHAR(10)
);

-- marks table
CREATE TABLE marks (
    student_id INT,
    subject VARCHAR(50),
    marks INT,
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- Sample Data
INSERT INTO students (name, class) VALUES
('Reyaansh', '6A'),
('Saanvi', '6A');

INSERT INTO marks (student_id, subject, marks) VALUES
(1, 'Math', 90),
(1, 'Science', 88),
(1, 'English', 85),
(2, 'Math', 70),
(2, 'Science', 75),
(2, 'English', 80);
