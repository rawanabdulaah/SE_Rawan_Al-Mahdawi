"""
add_student.py
==============
Script to add a new student to the database manually.
"""

from models import db, Student
from app import create_app

app = create_app()

with app.app_context():
    # بيانات الطالب الجديد - غيّرها كما تريد
    new_student = Student(
        university_id='441000444',          # الرقم الجامعي
        full_name='Khalid Alharbi',         # الاسم الكامل
        email='khalid@university.edu',      # الإيميل
        major='Information Technology'      # التخصص
    )
    new_student.set_password('Student@123')  # كلمة المرور

    db.session.add(new_student)
    db.session.commit()

    print(f'Student added successfully!')
    print(f'  University ID: {new_student.university_id}')
    print(f'  Name: {new_student.full_name}')
    print(f'  Password: Student@123')