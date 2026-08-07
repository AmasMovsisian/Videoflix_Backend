# Videoflix Backend

A Netflix-inspired streaming backend built with **Django** and **Django REST Framework**. The application provides a complete REST API for authentication, video management, HLS streaming, and secure user management.

The backend uses **FFmpeg** for video transcoding, **PostgreSQL** for persistent storage, **Redis** for caching, **JWT authentication with HTTP-only cookies** for security, and is fully containerized with **Docker**.

---

# Table of Contents

- [Frontend](#frontend)
- [About the Project](#about-the-project)
- [Prerequisites](#prerequisites)
- [Installation & Configuration](#installation--configuration)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Project Structure](#project-structure)
- [Authentication Flow](#authentication-flow)
- [Video Streaming](#video-streaming)
- [API Endpoints](#api-endpoints)
- [Author](#author)

---

# Frontend

Frontend repository:
https://github.com/AmasMovsisian/Videoflix_Frontend

---

# About the Project

Videoflix Backend is a Netflix-inspired streaming backend built with Django and Django REST Framework.

It provides authentication, video processing, HLS streaming and secure API access for the Videoflix platform.

---

# Prerequisites

Before installing the project make sure you have installed:

- Docker
- Docker Compose
- Git

---

# Installation & Configuration

## 1. Clone the Repository

```bash
git clone <repository-url>
cd Videoflix_Backend
```

---

## 2. Create the Environment File

Sensitive configuration values are stored inside a local `.env` file.

Create it by copying the template:

```bash
cp .env.template .env
```

---

## 3. Generate a Django Secret Key

Run:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the generated key into your `.env` file.

---

## 4. Configure Environment Variables

Example:

```env
SECRET_KEY=your_secret_key
DEBUG=True

DB_NAME=videoflix
DB_USER=postgres
DB_PASSWORD=postgres

EMAIL_HOST=smtp.example.com
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
```

> **Important**
>
> `DEBUG=True` should only be used during development.
>
> For production:
>
> - Set `DEBUG=False`
> - Configure `ALLOWED_HOSTS`
> - Configure `CORS_ALLOWED_ORIGINS`
> - Configure `CSRF_TRUSTED_ORIGINS`
> - Use secure production credentials

---

## 5. Make the Entrypoint Script Executable (Linux/macOS)

On Linux and macOS, make the entrypoint script executable before starting the containers:

```bash
chmod +x backend.entrypoint.sh
```

This step only needs to be done once after cloning the repository.

---

## 6. Build and Start the Containers

```bash
docker compose up --build
```

During the first startup the entrypoint script automatically:

- waits until PostgreSQL is ready
- runs all database migrations
- collects static files (if configured)
- creates the Django superuser
- starts the Django application

---

## 7. Access the API

Once the containers are running, the backend is available at:

```
http://127.0.0.1:8000/
```

---

# Tech Stack

### Backend

- Django
- Django REST Framework

### Database

- PostgreSQL

### Caching

- Redis

### Authentication

- JWT (Access & Refresh Tokens)
- HTTP-only Cookies

### Video Processing

- FFmpeg
- HLS (HTTP Live Streaming)

### Infrastructure

- Docker
- Docker Compose

---

# Features

## Authentication

- User Registration
- User Login
- Secure Logout
- JWT Authentication
- HTTP-only Cookies
- Refresh Tokens
- Protected Endpoints

---

## Email Verification

After registration, users receive an activation email containing a secure token.

Only activated accounts are allowed to log in.

---

## Password Reset

Includes the complete password reset workflow:

- Request password reset
- Receive reset email
- Verify token
- Set new password

---

## Video Processing

Uploaded videos are automatically processed using **FFmpeg**.

Generated outputs include:

- HLS playlists (.m3u8)
- Video segments (.ts)
- Multiple resolutions

---

## Adaptive Streaming

The backend serves HLS streams that allow the client to automatically switch between different resolutions depending on network quality.

---

## Redis Cache

Frequently requested data is cached using Redis to reduce database load and improve response times.

---

## Dockerized

The application runs fully containerized with Docker and Docker Compose.

---

# Project Structure

```
Videoflix_Backend/
│
├── accounts/
│   ├── authentication
│   ├── registration
│   ├── activation
│   └── password reset
│
├── videos/
│   ├── upload
│   ├── ffmpeg conversion
│   ├── streaming
│   └── serializers
│
├── core/
│   ├── settings
│   ├── urls
│   ├── middleware
│   └── configuration
│
├── media/
│   ├── uploaded videos
│   └── generated HLS files
│
├── static/
│
├── backend.Dockerfile
│
├── backend.entrypoint.sh
│
├── docker-compose.yml
│
├── manage.py
│
├── requirements.txt
│
└── .env.template
```

---

# Authentication Flow

JWT authentication uses secure HTTP-only cookies.

Flow:

1. Register and activate account.
2. Login and receive tokens.
3. Access protected endpoints.
4. Refresh tokens when needed.
5. Logout invalidates tokens.

HTTP-only cookies prevent client-side JavaScript access to tokens.

---

# Video Streaming

HLS adaptive streaming allows the client to switch between multiple resolutions depending on network conditions.

---

# API Endpoints

## Authentication

| Method | Endpoint                               | Description            |
| ------ | -------------------------------------- | ---------------------- |
| POST   | `/api/register/`                       | Register a new user    |
| GET    | `/api/activate/<uid>/<token>/`         | Activate user account  |
| POST   | `/api/login/`                          | Login user             |
| POST   | `/api/logout/`                         | Logout user            |
| POST   | `/api/token/refresh/`                  | Refresh access token   |
| POST   | `/api/password_reset/`                 | Request password reset |
| POST   | `/api/password_confirm/<uid>/<token>/` | Confirm password reset |

---

## Videos

| Method | Endpoint                                  | Description                |
| ------ | ----------------------------------------- | -------------------------- |
| GET    | `/api/video/`                             | Retrieve all videos        |
| GET    | `/api/video/<id>/<resolution>/index.m3u8` | Retrieve HLS playlist      |
| GET    | `/api/video/<id>/<resolution>/<segment>/` | Retrieve HLS video segment |

---

# Author

**Amas Movsisian**

Backend Developer

---
