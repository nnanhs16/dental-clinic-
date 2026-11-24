
# Dental Clinic Management System

Hệ thống quản lý phòng khám nha khoa được xây dựng theo mô hình Client-Server.

## 1. Technologies

### Client
- Python 3.12
- PySide6

### Server
- Python 3.12
- Django 5
- Django REST Framework
- JWT Authentication

### Database
- MariaDB
- XAMPP
- phpMyAdmin

### Communication
- HTTP REST API
- JSON

## 2. Project Structure

```text
dental-clinic/
├── client/
├── server/
│   ├── accounts/
│   ├── patients/
│   ├── appointments/
│   ├── reception/
│   ├── nursing/
│   ├── clinical/
│   ├── accounting/
│   ├── management/
│   ├── human_resources/
│   ├── system_admin/
│   ├── config/
│   └── manage.py
├── database/
├── requirements.txt
├── .gitignore
└── README.md
```

## 3. Setup

1. Install Python 3.12.
2. Install XAMPP and start MySQL.
3. Create database `dental_clinic`.
4. Create virtual environment:

```cmd
py -3.12 -m venv venv312
venv312\Scripts\activate
```

5. Install dependencies:

```cmd
pip install -r requirements.txt
```

6. Configure the `.env` file using the required database settings.
7. Run migrations:

```cmd
cd server
python manage.py migrate
```

8. Start the server:

```cmd
python manage.py runserver
```

## 4. API

- Admin: http://127.0.0.1:8000/admin/
- Authentication: http://127.0.0.1:8000/api/accounts/token/
- Current user: http://127.0.0.1:8000/api/accounts/me/

## 5. Architecture

PySide6 Client communicates with Django Server through HTTP REST API.
Django Server handles business logic and accesses MariaDB.
