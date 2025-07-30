import streamlit as st
import mysql.connector
from fpdf import FPDF

# ---------- Function: Connect to MySQL ----------
def connect_db():
    return mysql.connector.connect(
        
        host="sql.freedb.tech",
        user="freedb_preeti_mishra",
        password="QUUFH#EGu2rb99#",
        database="freedb_user_db"
    )
def create_table():
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                age INT
            )
        """)
        db.commit()
        cursor.close()
        db.close()
    except Error as e:
        st.error(f"Error creating table: {e}")

# ---------- Function: Fetch student data ----------
def fetch_student_data(roll_no):
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT * FROM marksheet WHERE roll_no = %s"
    cursor.execute(query, (roll_no,))
    result = cursor.fetchone()
    conn.close()
    return result

# ---------- Function: Generate Marksheet PDF ----------
def generate_pdf(name, class_sec, marks, total, percentage):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Student Marksheet", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Class: {class_sec}", ln=True)
    for i, mark in enumerate(marks, 1):
        pdf.cell(200, 10, txt=f"Subject {i}: {mark}", ln=True)
    pdf.cell(200, 10, txt=f"Total: {total}", ln=True)
    pdf.cell(200, 10, txt=f"Percentage: {percentage:.2f}%", ln=True)

    file_path = "/mnt/data/marksheet.pdf"
    pdf.output(file_path)
    return file_path

# ---------- Function: Display student marks ----------
def display_marksheet(student):
    name, class_sec = student[1], student[2]
    marks = student[3:]
    total = sum(marks)
    percentage = total / 5

    st.subheader(f"Name: {name}")
    st.write(f"Class: {class_sec}")
    st.write("Marks:")
    for i, m in enumerate(marks, 1):
        st.write(f"Subject {i}: {m}")
    st.write(f"Total: {total}")
    st.write(f"Percentage: {percentage:.2f}%")

    if st.button("Download PDF"):
        path = generate_pdf(name, class_sec, marks, total, percentage)
        with open(path, "rb") as f:
            st.download_button("Download Marksheet PDF", f, file_name="marksheet.pdf")

# ---------- Streamlit App ----------
def main():
    st.title("Student Marksheet Viewer")
    roll_no = st.number_input("Enter Roll Number", min_value=1, step=1)

    if st.button("Show Marksheet"):
        student = fetch_student_data(roll_no)
        if student:
            display_marksheet(student)
        else:
            st.error("Roll number not found.")

if __name__ == "__main__":
    main()
