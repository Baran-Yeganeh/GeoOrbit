# GeoOrbit

GeoOrbit is a Django web application for managing **GNSS surveying missions**, including projects, receivers, satellite systems, and processing reports.

## Features

- Create, view, update, and delete surveying missions.
- Associate missions with receivers and satellite systems.
- Store images for missions, receivers, and satellite systems.
- Manage processing reports.
- Search missions dynamically using AJAX.
- Provide a REST API built with Django REST Framework.
- Authenticate API requests using token authentication.
- Apply group-based API permissions for `Employees` and `Managers`.
- Manage application data through Django Admin.
- Run automated tests for application views, forms, search, and API permissions.

## Tech stack

- Python
- Django
- Django REST Framework
- MySQL
- HTML, CSS, Bootstrap, JavaScript, and jQuery

## Requirements

- Python compatible with the installed Django version
- MySQL Server
- Git

## Setup on Windows

Clone the repository:

```cmd
git clone https://github.com/Baran-Yeganeh/GeoOrbit.git
cd GeoOrbit
```

Create and activate a virtual environment:

```cmd
python -m venv venv
venv\Scripts\activate
```

Install the dependencies:

```cmd
python -m pip install -r requirements.txt
```

Create a local environment file:

```cmd
copy .env.example .env
```

Edit `.env` and enter your own settings, including your MySQL password and a suitable Django secret key. Do not commit `.env` or share its secrets.

Create the MySQL database before running migrations:

```sql
CREATE DATABASE gnss_lab_db CHARACTER SET utf8mb4;
```

Make sure the database name, username, password, host, and port in `.env` match your MySQL configuration.

Apply migrations and create an administrator account:

```cmd
python manage.py migrate
python manage.py createsuperuser
```

Start the development server:

```cmd
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser. The login page is available at `/accounts/login/`.

## Environment variables

The `.env.example` file lists the environment variables used by the project. Configure the database credentials, Django secret key, allowed hosts, debug setting, and email credentials as needed.

Use `DEBUG=False`, a secure secret key, and appropriate allowed hosts when configuring a production deployment. Do not use development defaults in production.

## Tests

Run the automated Django test suite:

```cmd
python manage.py test
```

## REST API

All API endpoints below are prefixed with `/gnss/`.

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/gnss/api/token/` | Obtain an authentication token |
| `GET` | `/gnss/api/missions/` | List missions |
| `POST` | `/gnss/api/mission/create/` | Create a mission |
| `GET`, `PUT`, `PATCH`, `DELETE` | `/gnss/api/mission/<id>/` | Retrieve, update, or delete a mission |
| `GET`, `POST` | `/gnss/api/receivers/` | List or create receivers |
| `GET`, `PUT`, `PATCH`, `DELETE` | `/gnss/api/receiver/<id>/` | Retrieve, update, or delete a receiver |
| `GET`, `POST` | `/gnss/api/satellite-systems/` | List or create satellite systems |
| `GET`, `PUT`, `PATCH`, `DELETE` | `/gnss/api/satellite-system/<id>/` | Retrieve, update, or delete a satellite system |
| `GET`, `POST` | `/gnss/api/processing-reports/` | List or create processing reports |
| `GET`, `PUT`, `PATCH`, `DELETE` | `/gnss/api/processing-report/<id>/` | Retrieve, update, or delete a processing report |

### API permissions

- Read-only requests (`GET`, `HEAD`, and `OPTIONS`) are allowed without authentication.
- Creating records (`POST`) requires an authenticated user in the `Employees` or `Managers` group.
- Updating or deleting records requires membership in the `Managers` group.
- Superusers are granted access by the custom permission class.
- For authenticated API requests, send the token in the request header:

```text
Authorization: Token YOUR_TOKEN
```

## Project structure

```text
config/          Django settings and root URLs
apps/main/       Main application views and URLs
apps/gnss/       GNSS models, forms, API, permissions, and tests
templates/       Django HTML templates
static/          CSS, JavaScript, and static images