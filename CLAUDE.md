# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build/Run Commands
- Start app: `python run.py`
- Database setup: Use SQLAlchemy's `db.create_all()` (already in the create_app function)
- Install dependencies: `pip install -r requirements.txt`
- Create virtual env: `python -m venv venv && source venv/bin/activate`
- Environment compatibility: Requires Python 3.8-3.9 with Flask 2.0.1, Werkzeug 2.0.1, SQLAlchemy 1.4.23

## Important Notes
- The app uses SQLAlchemy's built-in migration support through `db.create_all()` rather than Flask-Migrate
- Version compatibility is critical - newer versions of Werkzeug and SQLAlchemy will cause errors
- When adding new models, ensure they're imported in app/__init__.py before db.create_all() is called

## Code Style Guidelines
- Follow PEP 8 for Python style (snake_case for variables/functions)
- Use CamelCase for class names
- Models include __repr__ and to_dict methods
- Organize routes by feature with clear comments
- Form validation with appropriate validators from WTForms
- Blueprint-based structure for modular organization
- SQLAlchemy for database models with relationship definitions
- Handle errors with appropriate Flask error pages and flash messages
- Document functions with docstrings describing purpose and parameters