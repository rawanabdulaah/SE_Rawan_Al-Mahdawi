"""
app.py
======
Main entry point for the University Course Registration System.
Initializes the Flask application, registers all blueprints,
sets up the database, and inserts seed data on first run.

How to run:
    python app.py
    Then open: http://127.0.0.1:5000
"""

from flask import Flask
from flask_login import LoginManager
from models import db, Student, Admin, Course
from config import Config
# =============================================================================
# Application Factory
# =============================================================================
def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask app instance ready to run.
    """
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

    # Load configuration from Config class
    app.config.from_object(Config)

    # Initialize extensions with the app
    db.init_app(app)

    # =========================================================================
    # Flask-Login Setup
    # =========================================================================
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'error'

    @login_manager.user_loader
    def load_user(user_id):
        """
        Flask-Login user loader callback.
        This function is called by Flask-Login to load the current user
        from the session. Since we have two user types (Student and Admin),
        we first try to load as each type.

        Args:
            user_id (str): The user ID stored in the session (formatted as 'S_1' or 'A_1').

        Returns:
            User object (Student or Admin) if found, otherwise None.
        """
        # The user_id contains a prefix to indicate user type: 'S_' for Student, 'A_' for Admin
        if user_id.startswith('S_'):
            return db.session.get(Student, int(user_id[2:]))
        elif user_id.startswith('A_'):
            return db.session.get(Admin, int(user_id[2:]))
        return None

    # =========================================================================
    # Register Blueprints
    # =========================================================================
    from app.routes.auth import auth
    from app.routes.student import student
    from app.routes.admin import admin

    app.register_blueprint(auth)
    app.register_blueprint(student)
    app.register_blueprint(admin)

    # =========================================================================
    # Database Initialization and Seed Data
    # =========================================================================
    with app.app_context():
        # Create all tables if they don't exist
        db.create_all()

        # Insert seed data only if the database is empty
        if Student.query.count() == 0 and Admin.query.count() == 0:
            seed_database()

    return app


# =============================================================================
# Seed Data
# =============================================================================
def seed_database():
    """
    Insert initial sample data into the database.
    This runs automatically on first launch when the database is empty.

    Creates:
        - 8 courses (some with prerequisites)
        - 3 students
        - 1 admin
    """
    print("Seeding database with initial data...")

    # -------------------------------------------------------------------------
    # Create Courses
    # -------------------------------------------------------------------------
    course1 = Course(
        course_code='CS101',
        course_name='Introduction to Programming',
        credit_hours=3,
        max_capacity=30,
        available_seats=30,
        schedule_day='Sunday',
        schedule_time='08:00 AM - 10:00 AM',
        prerequisite_id=None
    )
    db.session.add(course1)

    course2 = Course(
        course_code='CS201',
        course_name='Data Structures',
        credit_hours=3,
        max_capacity=25,
        available_seats=25,
        schedule_day='Monday',
        schedule_time='10:00 AM - 12:00 PM',
        prerequisite_id=None  # Will set after CS101 is committed
    )
    db.session.add(course2)

    course3 = Course(
        course_code='MATH101',
        course_name='Calculus I',
        credit_hours=4,
        max_capacity=35,
        available_seats=35,
        schedule_day='Sunday',
        schedule_time='10:00 AM - 12:00 PM',
        prerequisite_id=None
    )
    db.session.add(course3)

    course4 = Course(
        course_code='MATH201',
        course_name='Calculus II',
        credit_hours=4,
        max_capacity=30,
        available_seats=30,
        schedule_day='Tuesday',
        schedule_time='08:00 AM - 10:00 AM',
        prerequisite_id=None  # Will set after MATH101 is committed
    )
    db.session.add(course4)

    course5 = Course(
        course_code='PHYS101',
        course_name='Physics I',
        credit_hours=3,
        max_capacity=25,
        available_seats=25,
        schedule_day='Wednesday',
        schedule_time='08:00 AM - 10:00 AM',
        prerequisite_id=None
    )
    db.session.add(course5)

    course6 = Course(
        course_code='ENGL101',
        course_name='English Composition',
        credit_hours=2,
        max_capacity=40,
        available_seats=40,
        schedule_day='Monday',
        schedule_time='08:00 AM - 10:00 AM',
        prerequisite_id=None
    )
    db.session.add(course6)

    course7 = Course(
        course_code='CS301',
        course_name='Database Systems',
        credit_hours=3,
        max_capacity=20,
        available_seats=20,
        schedule_day='Thursday',
        schedule_time='10:00 AM - 12:00 PM',
        prerequisite_id=None  # Will set after CS201 is committed
    )
    db.session.add(course7)

    course8 = Course(
        course_code='STAT101',
        course_name='Introduction to Statistics',
        credit_hours=3,
        max_capacity=35,
        available_seats=35,
        schedule_day='Wednesday',
        schedule_time='10:00 AM - 12:00 PM',
        prerequisite_id=None
    )
    db.session.add(course8)

    # Commit to get course IDs assigned
    db.session.commit()

    # Now set the prerequisites (need course IDs from the database)
    # CS201 requires CS101
    course2.prerequisite_id = course1.id
    # MATH201 requires MATH101
    course4.prerequisite_id = course3.id
    # CS301 requires CS201
    course7.prerequisite_id = course2.id

    db.session.commit()
    print("  -> 8 courses created successfully.")

    # -------------------------------------------------------------------------
    # Create Students
    # -------------------------------------------------------------------------
    student1 = Student(
        university_id='441000111',
        full_name='Ahmed Alghamdi',
        email='ahmed@university.edu',
        major='Computer Science'
    )
    student1.set_password('Student@123')
    db.session.add(student1)

    student2 = Student(
        university_id='441000222',
        full_name='Sara Alqahtani',
        email='sara@university.edu',
        major='Computer Science'
    )
    student2.set_password('Student@123')
    db.session.add(student2)

    student3 = Student(
        university_id='441000333',
        full_name='Noura Alshahrani',
        email='noura@university.edu',
        major='Mathematics'
    )
    student3.set_password('Student@123')
    db.session.add(student3)

    db.session.commit()
    print("  -> 3 students created successfully.")

    # -------------------------------------------------------------------------
    # Create Admin
    # -------------------------------------------------------------------------
    admin = Admin(
        username='admin'
    )
    admin.set_password('Admin@123')
    db.session.add(admin)

    db.session.commit()
    print("  -> 1 admin created successfully.")

    print("Database seeding complete!")
    print("-" * 50)
    print("Default Credentials:")
    print("  Admin: username='admin', password='Admin@123'")
    print("  Students: university_id='441000111' (or 222, 333), password='Student@123'")
    print("-" * 50)


# =============================================================================
# Application Entry Point
# =============================================================================
if __name__ == '__main__':
    # Create the app and run the development server
    app = create_app()
    print("=" * 60)
    print(" University Course Registration System (SE1201 Project)")
    print(" Server running at: http://127.0.0.1:5000")
    print(" Press CTRL+C to stop the server")
    print("=" * 60)
    app.run(debug=True, host='127.0.0.1', port=5000)