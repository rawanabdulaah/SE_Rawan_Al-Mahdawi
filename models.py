"""
models.py
=========
Database models for the University Course Registration System.
Defines all tables and their relationships using SQLAlchemy ORM.

Tables:
    - Admin: System administrators who manage courses and view students.
    - Student: Students who can register for courses.
    - Course: Courses available for registration.
    - Registration: Junction table linking students to courses.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone


# Initialize SQLAlchemy instance (will be linked to the Flask app in app.py)
db = SQLAlchemy()


# =============================================================================
# Admin Model
# =============================================================================
class Admin(UserMixin, db.Model):
    """
    Admin model for system administrators.
    Inherits from UserMixin to provide Flask-Login required methods.
    """

    __tablename__ = 'admins'

    # --- Columns ---
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # --- Password Management ---
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # --- Flask-Login Identifier ---
    def get_id(self):
        """
        Return a unique identifier for Flask-Login.
        Prefix with 'A_' to distinguish from Student users.
        """
        return f'A_{self.id}'

    # --- String Representation ---
    def __repr__(self):
        return f'<Admin {self.username}>'


# =============================================================================
# Student Model
# =============================================================================
class Student(UserMixin, db.Model):
    """
    Student model representing university students.
    Students login using their university_id and password.
    Inherits from UserMixin for Flask-Login compatibility.
    """

    __tablename__ = 'students'

    # --- Columns ---
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    university_id = db.Column(db.String(20), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    major = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # --- Relationships ---
    registrations = db.relationship(
        'Registration',
        backref='student',
        lazy=True,
        cascade='all, delete-orphan'
    )

    # --- Password Management ---
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # --- Flask-Login Identifier ---
    def get_id(self):
        """
        Return a unique identifier for Flask-Login.
        Prefix with 'S_' to distinguish from Admin users.
        """
        return f'S_{self.id}'

    # --- String Representation ---
    def __repr__(self):
        return f'<Student {self.university_id} - {self.full_name}>'


# =============================================================================
# Course Model
# =============================================================================
class Course(db.Model):
    """
    Course model representing university courses available for registration.
    Includes prerequisite logic and seat capacity tracking.
    """

    __tablename__ = 'courses'

    # --- Columns ---
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_code = db.Column(db.String(10), unique=True, nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    credit_hours = db.Column(db.Integer, nullable=False)
    max_capacity = db.Column(db.Integer, nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)
    schedule_day = db.Column(db.String(20), nullable=False)
    schedule_time = db.Column(db.String(30), nullable=False)

    # Self-referential foreign key for prerequisite course
    prerequisite_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=True)

    # --- Relationships ---
    # A course can have many registrations. Cascade deletes registrations.
    registrations = db.relationship(
        'Registration',
        backref='course',
        lazy=True,
        cascade='all, delete-orphan'
    )

    # Self-referential relationship for prerequisite
    prerequisite = db.relationship(
        'Course',
        remote_side=[id],
        backref=db.backref('required_by', lazy=True)
    )

    # --- Helper Methods ---
    def is_full(self):
        """
        Check if the course has reached maximum capacity.
        Returns True if no seats are available.
        """
        return self.available_seats <= 0

    def has_prerequisite(self):
        """
        Check if the course has a prerequisite.
        Returns True if a prerequisite course is set.
        """
        return self.prerequisite_id is not None

    # --- String Representation ---
    def __repr__(self):
        return f'<Course {self.course_code} - {self.course_name}>'


# =============================================================================
# Registration Model
# =============================================================================
class Registration(db.Model):
    """
    Registration model (Junction Table).
    Links students to courses they have registered for.
    """

    __tablename__ = 'registrations'

    # --- Columns ---
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    registration_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # --- Constraints ---
    # Prevent duplicate registration: a student cannot register for the same course twice.
    __table_args__ = (
        db.UniqueConstraint('student_id', 'course_id', name='unique_student_course'),
    )

    # --- String Representation ---
    def __repr__(self):
        return f'<Registration: Student {self.student_id} -> Course {self.course_id}>'