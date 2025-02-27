import mysql.connector

class Employee:
    def __init__(self, emp_id, name, department, salary):
        self.emp_id = emp_id
        self.name = name
        self.department = department
        self.salary = salary
        self.performance_reviews = []

    def promote(self, increment):
        self.salary += increment

    def add_performance_review(self, review):
        self.performance_reviews.append(review)

class Department:
    def __init__(self, name):
        self.name = name
        self.employees = []

    def add_employee(self, employee):
        self.employees.append(employee)

    def get_employees(self):
        return self.employees

class PerformanceReview:
    def __init__(self, emp_id, review):
        self.emp_id = emp_id
        self.review = review

class EmployeeManagementSystem:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    # Method to connect to the database
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print("Connection successful!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    
    # Method to close the database connection
    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Connection closed.")

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                                emp_id INTEGER PRIMARY KEY,
                                name TEXT,
                                department TEXT,
                                salary REAL)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS performance_reviews (
                                emp_id INTEGER,
                                review TEXT,
                                FOREIGN KEY(emp_id) REFERENCES employees(emp_id))''')
        self.connection.commit()

    def add_employee(self, emp_id, name, department, salary):
        self.cursor.execute("INSERT INTO employees VALUES (%s, %s, %s, %s)", (emp_id, name, department, salary))
        self.connection.commit()

    def search_employee(self, keyword):
        self.cursor.execute("SELECT * FROM employees WHERE name LIKE %s OR department LIKE %s OR emp_id = %s", 
                            (f"%{keyword}%", f"%{keyword}%", keyword))
        return self.cursor.fetchall()

    def update_salary(self, emp_id, new_salary):
        self.cursor.execute("UPDATE employees SET salary = %s WHERE emp_id = %s", (new_salary, emp_id))
        self.connection.commit()

    def add_performance_review(self, emp_id, review):
        self.cursor.execute("INSERT INTO performance_reviews VALUES (%s, %s)", (emp_id, review))
        self.connection.commit()

    def get_department_summary(self):
        self.cursor.execute("SELECT department, name, review FROM employees JOIN performance_reviews ON employees.emp_id = performance_reviews.emp_id")
        return self.cursor.fetchall()

# Example Usage
if __name__ == "__main__":
    ems = EmployeeManagementSystem("localhost", "appuser", "Aryaman21$", "ems")
    ems.connect()
    ems.create_tables()
    ems.add_employee(1, "Alice", "IT", 70000)
    ems.add_employee(2, "Bob", "HR", 60000)
    ems.add_performance_review(1, "Excellent performance in Q1.")
    print(ems.search_employee("Alice"))
    print(ems.get_department_summary())






