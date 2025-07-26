import streamlit as st
import mysql.connector

# Connect to database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="school"
)
cursor = conn.cursor()

# Streamlit UI
st.title("Student Record Viewer")

if st.button("Show Students"):
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    for row in rows:
        st.write(row)

name = st.text_input("Name")
age = st.number_input("Age", 1, 100)

if st.button("Add Student"):
    cursor.execute("INSERT INTO students (name, age) VALUES (%s, %s)", (name, age))
    conn.commit()
    st.success("Student added!")
