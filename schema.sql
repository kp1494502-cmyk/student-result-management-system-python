CREATE DATABASE IF NOT EXISTS student_result_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE student_result_db;

CREATE TABLE IF NOT EXISTS students (
    roll_no VARCHAR(30) PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    semester VARCHAR(30) NOT NULL,
    python INT NOT NULL,
    dbms INT NOT NULL,
    software_engineering INT NOT NULL,
    mathematics INT NOT NULL,
    computer_networks INT NOT NULL,
    total INT NOT NULL,
    percentage DECIMAL(5,2) NOT NULL,
    grade VARCHAR(2) NOT NULL,
    result VARCHAR(10) NOT NULL,
    CONSTRAINT chk_python CHECK (python BETWEEN 0 AND 100),
    CONSTRAINT chk_dbms CHECK (dbms BETWEEN 0 AND 100),
    CONSTRAINT chk_software_engineering CHECK (software_engineering BETWEEN 0 AND 100),
    CONSTRAINT chk_mathematics CHECK (mathematics BETWEEN 0 AND 100),
    CONSTRAINT chk_computer_networks CHECK (computer_networks BETWEEN 0 AND 100)
);
