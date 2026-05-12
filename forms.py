"""
forms.py
========
Flask-WTF form definitions for the University Course Registration System.
Each form handles data input, validation, and CSRF protection automatically.

Forms:
    - LoginForm: Handles both student and admin login.
    - CourseForm: Used by admin to add and edit courses.
    - DropForm: Simple form with CSRF protection for course drop action.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Email, Optional
from models import Course


def get_prerequisite_choices():
    """
    Helper function to fetch all courses as choices for the prerequisite dropdown.
    Returns a list of tuples (course_id, course_code_and_name).
    The first option is always 'None' with value ''.
    """
    # We wrap in a function to dynamically fetch courses at call time,
    # rather than at module load time (when DB may not exist yet).
    choices = [('', 'None')]
    try:
        courses = Course.query.order_by(Course.course_code).all()
        for course in courses:
            label = f'{course.course_code} - {course.course_name}'
            choices.append((str(course.id), label))
    except Exception:
        # If the database is not yet initialized, return just the "None" option
        pass
    return choices


class LoginForm(FlaskForm):
    """
    Form for both student and admin login.
    The user selects their role (Student/Admin) and provides credentials.
    """
    # Dropdown to select user type
    user_type = SelectField(
        'Login As',
        choices=[('student', 'Student'), ('admin', 'Admin')],
        validators=[DataRequired(message='Please select a user type.')]
    )

    # Field for student university ID (shown only when "Student" is selected)
    university_id = StringField(
        'University ID',
        validators=[Optional(), Length(min=3, max=20)]
    )

    # Field for admin username (shown only when "Admin" is selected)
    username = StringField(
        'Username',
        validators=[Optional(), Length(min=3, max=50)]
    )

    # Password field (required for both)
    password = PasswordField(
        'Password',
        validators=[DataRequired(message='Password is required.')]
    )

    # Submit button
    submit = SubmitField('Login')


class CourseForm(FlaskForm):
    """
    Form for admin to add a new course or edit an existing one.
    All fields except prerequisite are required.
    """
    # Course code (e.g., "CS101")
    course_code = StringField(
        'Course Code',
        validators=[
            DataRequired(message='Course code is required.'),
            Length(min=2, max=10, message='Course code must be 2-10 characters.')
        ]
    )

    # Full course name (e.g., "Introduction to Programming")
    course_name = StringField(
        'Course Name',
        validators=[
            DataRequired(message='Course name is required.'),
            Length(min=3, max=100, message='Course name must be 3-100 characters.')
        ]
    )

    # Number of credit hours (1 to 6)
    credit_hours = IntegerField(
        'Credit Hours',
        validators=[
            DataRequired(message='Credit hours are required.'),
            NumberRange(min=1, max=6, message='Credit hours must be between 1 and 6.')
        ]
    )

    # Maximum number of students that can enroll
    max_capacity = IntegerField(
        'Maximum Capacity',
        validators=[
            DataRequired(message='Maximum capacity is required.'),
            NumberRange(min=1, max=500, message='Capacity must be between 1 and 500.')
        ]
    )

    # Day the course is held (Sunday through Thursday)
    schedule_day = SelectField(
        'Schedule Day',
        choices=[
            ('Sunday', 'Sunday'),
            ('Monday', 'Monday'),
            ('Tuesday', 'Tuesday'),
            ('Wednesday', 'Wednesday'),
            ('Thursday', 'Thursday')
        ],
        validators=[DataRequired(message='Schedule day is required.')]
    )

    # Time slot for the course (e.g., "08:00 AM - 10:00 AM")
    schedule_time = StringField(
        'Schedule Time',
        validators=[
            DataRequired(message='Schedule time is required.'),
            Length(min=5, max=30, message='Enter a valid time range (e.g., 08:00 AM - 10:00 AM).')
        ]
    )

    # Optional prerequisite course selection
    prerequisite_id = SelectField(
        'Prerequisite Course',
        choices=[],  # Choices will be set dynamically in the route
        validators=[Optional()]
    )

    # Submit button
    submit = SubmitField('Save Course')

    def __init__(self, *args, **kwargs):
        """
        Override __init__ to dynamically populate prerequisite choices
        from the database at instantiation time.
        """
        super(CourseForm, self).__init__(*args, **kwargs)
        self.prerequisite_id.choices = get_prerequisite_choices()


class DropForm(FlaskForm):
    """
    Simple form used to wrap the "Drop Course" button.
    Provides CSRF protection without any visible fields.
    """
    submit = SubmitField('Drop Course')