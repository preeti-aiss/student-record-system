import streamlit as st
import mysql.connector
import pdfkit
import tempfile
import os

# Connect to DB
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",  # replace your MySQL password
    database="school"
    
)
cursor = conn.cursor()

st.title("📄 Student Report Card Generator with PDF Download")

# Get student list
cursor.execute("SELECT id, name FROM students")
students = cursor.fetchall()
student_dict = {name: sid for sid, name in students}

student_name = st.selectbox("Select a student", list(student_dict.keys()))

if student_name:
    sid = student_dict[student_name]

    # Fetch student class
    cursor.execute("SELECT class FROM students WHERE id=%s", (sid,))
    student_class = cursor.fetchone()[0]

    # Fetch marks
    cursor.execute("SELECT subject, marks FROM marks WHERE student_id=%s", (sid,))
    results = cursor.fetchall()

    if results:
        total = sum([m for s, m in results])
        num_subjects = len(results)
        percentage = total / num_subjects
        grade = "A" if percentage >= 85 else "B" if percentage >= 70 else "C" if percentage >= 50 else "Fail"

        st.subheader(f"Name: {student_name} | Class: {student_class}")
        st.write("### Subject-wise Marks")
        for subject, marks in results:
            st.write(f"{subject}: {marks}")

        st.write(f"**Total Marks:** {total}")
        st.write(f"**Percentage:** {percentage:.2f}%")
        st.write(f"**Grade:** {grade}")

        # HTML content for PDF
        html = f"""
        <h2>Report Card</h2>
        <p><strong>Name:</strong> {student_name}</p>
        <p><strong>Class:</strong> {student_class}</p>
        <table border="1" cellspacing="0" cellpadding="5">
            <tr><th>Subject</th><th>Marks</th></tr>
        """
        for subject, marks in results:
            html += f"<tr><td>{subject}</td><td>{marks}</td></tr>"
        html += f"""
        </table>
        <p><strong>Total:</strong> {total}</p>
        <p><strong>Percentage:</strong> {percentage:.2f}%</p>
        <p><strong>Grade:</strong> {grade}</p>
        """

        # Create temporary PDF
        if st.button("Download Report Card as PDF"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                pdfkit.from_string(html, tmp_pdf.name)
                with open(tmp_pdf.name, "rb") as f:
                    st.download_button(
                        label="📥 Click to Download PDF",
                        data=f,
                        file_name=f"{student_name}_report_card.pdf",
                        mime="application/pdf"
                    )
                os.unlink(tmp_pdf.name)
    else:
        st.warning("No marks found.")
