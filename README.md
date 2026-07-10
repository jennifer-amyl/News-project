# News Website Capstone

## Overview

This project is a Django-based news website developed as part of the HyperionDev Software Engineering Bootcamp.

The application allows users to:

- Register and log in
- View approved news articles
- Create and manage articles (Journalists)
- Read articles and newsletters (Readers)
- Manage users through the Django admin panel

The project has been version controlled using Git, documented using Sphinx and containerised using Docker.

---

## Technologies Used

- Python 3
- Django
- SQLite
- Git
- Docker
- Sphinx

---

## Installation (Virtual Environment)

### 1. Clone the repository

```bash
git clone https://github.com/jennifer-amyl/News-project.git
cd news-project
```

### 2. Create a virtual environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the project

If your project requires any secret keys or environment variables, create them before running the application.

Do not commit passwords, secret keys or access tokens to GitHub.

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Create an administrator (optional)

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

Open your browser and visit:

```
http://127.0.0.1:8000
```

---

## MySQL configuration with Docker

The project uses MySQL. For normal local development, Django connects to the
database using `localhost`.

When the application runs inside Docker, `localhost` refers to the container
itself rather than the Windows host. Use `host.docker.internal` so the container
can connect to MySQL running on the host machine.

Build the image:

```bash
docker build -t news-project .
```

Run the container on Windows with PowerShell:

```powershell
docker run --rm -p 8000:8000 `
  -e DB_HOST=host.docker.internal `
  -e DB_NAME=news_project_db `
  -e DB_USER=root `
  -e DB_PASSWORD=password `
  -e DB_PORT=3306 `
  news-project
```

For normal local virtual-environment use, no database environment variables are
required because the default database host remains `localhost`.

## Documentation

Sphinx documentation is located in the `docs` directory.

To build the documentation:

```bash
cd docs
make html
```

The generated HTML files can be found in:

```
docs/build/html
```

---

## Repository Structure

```
NewsWebsite/
│
├── docs/
├── news/
├── users/
├── templates/
├── static/
├── manage.py
├── requirements.txt
├── Dockerfile
├── README.md
└── .gitignore
```

---

## Author

Jennifer Fernandes

HyperionDev Software Engineering Bootcamp