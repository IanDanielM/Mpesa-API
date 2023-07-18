"""
Main Script

This script is the entry point of the application.
It runs the Flask application in debug mode.

"""

from app import create_app

app = create_app()


if __name__ == '__main__':
    app.run(debug=True)
