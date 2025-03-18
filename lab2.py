from typing import List, Dict
from flask import Flask, request, jsonify

app = Flask(__name__)

class Enrollment:
    def __init__(self, id: int, student_id: int, course_id: int):
        self.id = id
        self.student_id = student_id
        self.course_id = course_id

    def to_dict(self):
        return {"id": self.id, "student_id": self.student_id, "course_id": self.course_id}

class Course:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.enrollments: List[Enrollment] = []

    def add_enrollment(self, enrollment: Enrollment):
        self.enrollments.append(enrollment)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "enrollments": [enrollment.to_dict() for enrollment in self.enrollments]
        }

class Student:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.enrollments: List[Enrollment] = []

    def add_enrollment(self, enrollment: Enrollment):
        self.enrollments.append(enrollment)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "enrollments": [enrollment.to_dict() for enrollment in self.enrollments]
        }

class InMemoryAPI:
    def __init__(self):
        self.students: Dict[int, Student] = {}
        self.courses: Dict[int, Course] = {}
        self.enrollments: Dict[int, Enrollment] = {}

    def create_student(self, id: int, name: str):
        if id in self.students:
            return {"error": "Student already exists"}
        student = Student(id, name)
        self.students[id] = student
        return student.to_dict()

    def create_course(self, id: int, name: str):
        if id in self.courses:
            return {"error": "Course already exists"}
        course = Course(id, name)
        self.courses[id] = course
        return course.to_dict()

    def enroll_student(self, id: int, student_id: int, course_id: int):
        if id in self.enrollments:
            return {"error": "Enrollment already exists"}
        if student_id not in self.students:
            return {"error": "Student not found"}
        if course_id not in self.courses:
            return {"error": "Course not found"}
        enrollment = Enrollment(id, student_id, course_id)
        self.students[student_id].add_enrollment(enrollment)
        self.courses[course_id].add_enrollment(enrollment)
        self.enrollments[id] = enrollment
        return enrollment.to_dict()

api = InMemoryAPI()
api.create_student(1, "Alice")
api.create_course(1, "Mathematics")
api.enroll_student(1, 1, 1)

@app.route('/students', methods=['GET'])
def get_students():
    return jsonify([student.to_dict() for student in api.students.values()])

@app.route('/courses', methods=['GET'])
def get_courses():
    return jsonify([course.to_dict() for course in api.courses.values()])

@app.route('/enrollments', methods=['GET'])
def get_enrollments():
    return jsonify([enrollment.to_dict() for enrollment in api.enrollments.values()])

if __name__ == '__main__':
    app.run(debug=True)
