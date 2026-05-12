# University Course Registration System

## SE1201 - Foundations of Software Engineering Project
# https://github.com/rawanabdulaah/SE_Rawan_Al-Mahdawi/tree/main


## Project Description

A full-stack web application for university course registration Students can browse available courses, enroll with automatic validation, view their weekly schedule, and drop courses Administrators can manage the course catalog and student accounts

---

## Team Members

| Name | Student ID | Role |

| Rawan Abdullah Al-Mahdawi | 44610911 | Team Leader / Backend Developer |
| Dima Hashem Al-Saab | 44611454 | Frontend Developer |
| Dana Nayef Al-Mahabi | 44610881 | Database Designer / Tester |
| Lama Hassan Al-Mahdawi | 44610371 | Documentation / QA |

---

## Tech Stack

| Layer | Technology |

| Backend | Python 3.10+, Flask 3.0 |
| Database | SQLite + SQLAlchemy ORM |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Authentication | Flask-Login |
| Forms & CSRF | Flask-WTF |
| Password Security | Werkzeug (pbkdf2:sha256) |

---

## Features

### Student
- Login with university ID and password
- Browse all available courses with details
- Enroll in courses with automatic checks (duplicate, capacity, prerequisite, schedule conflict)
- View weekly schedule in calendar format
- Drop enrolled courses

### Admin
- Login with username and password
- Dashboard with statistics (students, courses, enrollments)
- Add, edit, and delete courses
- View all students and their enrolled courses
- Add and delete student accounts

### Security
- Passwords hashed with pbkdf2:sha256
- CSRF protection on all forms
- SQL injection prevention via ORM
- XSS prevention via Jinja2 auto-escaping
- Session management with Flask-Login
- Access control with custom decorators


---

## Setup Instructions

## Project Structure


course_registration_system/
├── app.py
├── config.py
├── models.py
├── forms.py
├── requirements.txt
├── README.md
└── app/
├── init.py
├── decorators.py
├── routes/
│   ├── init.py
│   ├── auth.py
│   ├── student.py
│   └── admin.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── student/
│   │   ├── dashboard.html
│   │   ├── courses.html
│   │   └── schedule.html
│   └── admin/
│       ├── dashboard.html
│       ├── courses.html
│       └── students.html
└── static/
├── css/
│   └── style.css
└── js/
└── main.js
### Prerequisites
- Python 3.10 or higher

### Steps

1. Clone the repository or extract the project folder
2. Open terminal in the project folder
3. Create virtual environment:


python -m venv venv

```
4. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
5. Install dependencies:


pip install -r requirements.txt


6. Run the application:


python app.py


7. Open browser: `http://127.0.0.1:5000/login`



## Default Credentials

| Role | Username/ID | Password |

| Admin | admin | Admin@123 |
| Student 1 | 441000111 | Student@123 |
| Student 2 | 441000222 | Student@123 |
| Student 3 | 441000333 | Student@123 |


## Testing

Four testing strategies were applied:

- Unit Testing: Individual functions tested (password hashing, conflict checks, prerequisite validation)
- Integration Testing: Full flow testing (login, enroll, drop, admin CRUD)
- Static Testing: Code review for PEP 8, SQL injection check, CSRF check
- Dynamic Testing: Running the system as real users on multiple screen sizes

