import streamlit as st
import sqlite3
import pandas as pd

# Database connection
conn = sqlite3.connect("students.db", check_same_thread=False)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    roll_no INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    course TEXT,
    marks REAL
)
""")
conn.commit()

st.title("🎓 Student Record Management System")
st.write("Manage Student Records using CRUD Operations")

# Menu
menu = st.sidebar.selectbox(
    "Select Operation",
    ["Add Student", "View Students",
     "Update Student", "Delete Student"]
)

# CREATE
if menu == "Add Student":
    st.header("Add New Student")

    roll = st.number_input("Roll Number", min_value=1, step=1)
    name = st.text_input("Student Name")
    age = st.number_input("Age", min_value=1, max_value=100)
    course = st.text_input("Course")
    marks = st.number_input("Marks", min_value=0.0, max_value=100.0)

    if st.button("Add Student"):
        try:
            cursor.execute(
                "INSERT INTO students VALUES (?, ?, ?, ?, ?)",
                (roll, name, age, course, marks)
            )
            conn.commit()
            st.success("Student added successfully!")
        except sqlite3.IntegrityError:
            st.error("Roll Number already exists!")

# READ
elif menu == "View Students":
    st.header("All Student Records")

    df = pd.read_sql_query("SELECT * FROM students", conn)
    st.dataframe(df, use_container_width=True)

# UPDATE
elif menu == "Update Student":
    st.header("Update Student Details")

    roll = st.number_input("Enter Roll Number", min_value=1, step=1)

    if st.button("Search Student"):
        result = cursor.execute(
            "SELECT * FROM students WHERE roll_no=?",
            (roll,)
        ).fetchone()

        if result:
            st.session_state.student = result
        else:
            st.error("Student not found!")

    if "student" in st.session_state:
        result = st.session_state.student

        name = st.text_input("Name", value=result[1])
        age = st.number_input("Age", value=result[2])
        course = st.text_input("Course", value=result[3])
        marks = st.number_input("Marks", value=float(result[4]))

        if st.button("Update Record"):
            cursor.execute("""
                UPDATE students
                SET name=?, age=?, course=?, marks=?
                WHERE roll_no=?
            """, (name, age, course, marks, result[0]))

            conn.commit()
            st.success("Student record updated!")
            del st.session_state.student

# DELETE
elif menu == "Delete Student":
    st.header("Delete Student Record")

    roll = st.number_input("Enter Roll Number", min_value=1, step=1)

    if st.button("Delete Student"):
        cursor.execute(
            "DELETE FROM students WHERE roll_no=?",
            (roll,)
        )
        conn.commit()

        if cursor.rowcount > 0:
            st.success("Student deleted successfully!")
        else:
            st.error("Student not found!")

conn.close()