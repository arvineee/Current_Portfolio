"""Entry point. PythonAnywhere's WSGI file keeps working: `from app import app as application`."""
from arval import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=False)
