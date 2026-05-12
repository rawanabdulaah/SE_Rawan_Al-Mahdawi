"""
config.py
=========
Main application configuration for the University Course Registration System.
Contains secret key, database settings, and security configurations.
"""

import os


class Config:
    """
    Main configuration class for the Flask application.
    Stores all configuration variables in one place.
    """

    # --- Secret Key ---
    # Used for session signing and CSRF protection.
    # In production, this should be set as an environment variable.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-for-se1201-project-2026'

    # --- Database Configuration ---
    # Get the absolute path of the project root directory.
    basedir = os.path.abspath(os.path.dirname(__file__))

    # SQLite database file will be stored inside the instance/ folder.
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'registration.db')
    # Disable tracking modifications to save memory (not needed for SQLite).
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Security Settings ---
    # Enable CSRF (Cross-Site Request Forgery) protection for all forms.
    WTF_CSRF_ENABLED = True