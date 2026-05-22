-- Таблица подразделений
CREATE TABLE department (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL CHECK (name <> ''),
    parent_id INT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_department_parent FOREIGN KEY (parent_id)
        REFERENCES department(id) ON DELETE SET NULL
);

-- Таблица сотрудников
CREATE TABLE employee (
    id SERIAL PRIMARY KEY,
    department_id INT NOT NULL,
    full_name VARCHAR(255) NOT NULL CHECK (full_name <> ''),
    position VARCHAR(255) NOT NULL CHECK (position <> ''),
    hired_at DATE NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_employee_department FOREIGN KEY (department_id)
        REFERENCES department(id) ON DELETE CASCADE
);

CREATE INDEX idx_department_parent ON department(parent_id);

CREATE INDEX idx_employee_department ON employee(department_id);