import pgxpool
import pymysql

def createRelations():

    # creates all of my relations
    with connection.cursor() as cursor:
        # create the tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Students (
                student_id INT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                age INT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Courses (
                course_id INT PRIMARY KEY,
                course_name VARCHAR(255) NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Enrollments (
                enrollment_id INT PRIMARY KEY,
                student_id INT,
                course_id INT,
                FOREIGN KEY (student_id) REFERENCES Students(student_id),
                FOREIGN KEY (course_id) REFERENCES Courses(course_id)
            )
        """)
# insert and parse the data from the provided CSV file into your relations
def insertParse( csv ):
    with connection.cursor() as cursor:
        # insert data into the tables
        cursor.execute("""
            INSERT INTO Students (student_id, name, age) VALUES
            (1, 'Alice', 20),
            (2, 'Bob', 22),
            (3, 'Charlie', 21)
        """)
        cursor.execute("""
            INSERT INTO Courses (course_id, course_name) VALUES
            (1, 'Math'),
            (2, 'Science'),
            (3, 'History')
        """)
        cursor.execute("""
            INSERT INTO Enrollments (enrollment_id, student_id, course_id) VALUES
            (1, 1, 1),
            (2, 1, 2),
            (3, 2, 1),
            (4, 3, 3)
        """)

if __name__ == "__main__":
    # database should be called HW5
    # create the database if it doesn't exist
    
    # interface allowing me to specify the CSV from the command line
    # When run as the primary entry point, your code
    # should connect to the database and properly create everything from scratch.
    
    
   
    createRelations()
    insertParse("data.csv")

    with connection.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS HW5")
        cursor.execute("USE HW5")

    # Connect to the MySQL database
    connection = pymysql.connect(
        host='localhost',
        user='your_username',
        password='your_password',
        database='HW5'
    )