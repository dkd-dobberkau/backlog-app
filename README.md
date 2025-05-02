# Backlog Application

A simple web application for managing product and sprint backlogs for agile development teams.

## Features

- Manage product backlog items with title, description, status, priority, and story points
- Create and organize sprints with start and end dates
- Move items between product backlog and sprint backlogs
- Track sprint status (Planned, Active, Completed)
- Responsive web interface

## Technology Stack

- Python 3.8-3.9
- Flask 2.0.1
- SQLAlchemy 1.4.23
- Werkzeug 2.0.1
- SQLite database
- Bootstrap (frontend)

## Installation

### Standard Installation

1. Clone this repository
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the application:
   ```
   python run.py
   ```
5. Access the application at http://127.0.0.1:5001

### Docker Installation

1. Clone this repository
2. Build the Docker image:
   ```
   docker build -t backlog-app .
   ```
3. Run the container:
   ```
   docker run -p 5001:5000 backlog-app
   ```
4. Access the application at http://127.0.0.1:5001

## Project Structure

- `app/` - Main application package
  - `__init__.py` - Application factory and database initialization
  - `models.py` - Database models (BacklogItem, Sprint)
  - `forms.py` - WTForms form definitions
  - `routes.py` - Route handlers and business logic
  - `templates/` - Jinja2 HTML templates
  - `static/` - CSS, JavaScript and static assets
- `config.py` - Application configuration
- `run.py` - Application entry point

## Development

- The application uses SQLite as the database, with the file stored as `app.db`
- Changes to models will be automatically applied to the database schema via `db.create_all()`
- For adding new models, ensure they're imported in `app/__init__.py` before `db.create_all()` is called

## Version Compatibility

- Requires Python 3.8-3.9 with Flask 2.0.1, Werkzeug 2.0.1, SQLAlchemy 1.4.23
- Newer versions of Werkzeug and SQLAlchemy may cause errors