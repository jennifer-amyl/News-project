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
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
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

## Running with Docker

### Build the Docker image

```bash
docker build -t news-capstone .
```

### Run the container

```bash
docker run -p 8000:8000 news-capstone
```

Visit:

```
http://localhost:8000
```

---

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