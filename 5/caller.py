import os
import django
from datetime import date, datetime

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Student

# Run and print your queries


def add_students():
    student_data = [
        {"student_id": "FC5204", "first_name": "John", "last_name": "Doe", "birth_date": "1995-05-15", "email": "john.doe@university.com"},
        {"student_id": "FE0054", "first_name": "Jane", "last_name": "Smith", "birth_date": None, "email": "jane.smith@university.com"},
        {"student_id": "FH2014", "first_name": "Alice", "last_name": "Johnson", "birth_date": "1998-02-10", "email": "alice.johnson@university.com"},
        {"student_id": "FH2015", "first_name": "Bob", "last_name": "Wilson", "birth_date": "1996-11-25", "email": "bob.wilson@university.com"},
    ]

    student_instances = []
    for student in student_data:
        birth_date = datetime.strptime(student["birth_date"], "%Y-%m-%d").date() if student["birth_date"] else None
        student_instance = Student(
            student_id=student["student_id"],
            first_name=student["first_name"],
            last_name=student["last_name"],
            birth_date=birth_date,
            email=student["email"]
        )
        student_instances.append(student_instance)
    Student.objects.bulk_create(student_instances)

# add_students()
# print(Student.objects.all())


def get_students_info():
    all = Student.objects.all()
    result = ''
    for a in all:
        result += f"\nStudent №{a.student_id}: {a.first_name} {a.last_name}; Email: {a.email}"
    return result
# print(get_students_info())

def update_students_emails():
    all = Student.objects.all()
    for a in all:
        a.email = a.email.split("@")[0] + '@uni-students.com'
        a.save()

# update_students_emails()
# for student in Student.objects.all():
#     print(student.email)

def truncate_students():
    Student.objects.all().delete()

# truncate_students()
# print(Student.objects.all())
# print(f"Number of students: {Student.objects.count()}")