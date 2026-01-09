# Videoflix Backend

Django REST API for the Videoflix streaming platform with JWT authentication and HLS video streaming.

---

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Technologies](#technologies)
- [Configuration](#configuration)
- [Docker Commands](#docker-commands)

---

## Requirements

- Docker Desktop installed and running
- Git installed

---

## Installation

1. **Clone repository and navigate to directory**

2. **Create environment file**
   ```bash
   cp .env.template .env
   ```

3. **Start Docker containers**
   ```bash
   docker-compose up --build
   ```

4. **Access application**
   - Backend: http://localhost:8000
   - Admin: http://localhost:8000/admin
   - Login: `admin` / `adminpassword`

---

## Project Structure

```
videoflix/
├── core/                   # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/                  # Authentication
│   ├── authentication.py   # JWT Cookie Auth
│   ├── serializers.py      # Request/Response validation
│   ├── urls.py             # Auth routes
│   ├── utils.py            # Helper functions
│   └── views.py            # Auth views
├── videos/                 # Video streaming
│   ├── models.py           # Video model
│   ├── serializers.py      # Video serializer
│   ├── tasks.py            # HLS conversion (background)
│   ├── urls.py             # Video routes
│   ├── utils.py            # Streaming helpers
│   └── views.py            # Video views
├── media/                  # Uploads & HLS files
├── static/                 # Static files
├── .env                    # Environment variables
├── docker-compose.yml      # Docker configuration
├── backend.Dockerfile      # Docker image
├── backend.entrypoint.sh   # Container startup
├── requirements.txt        # Python dependencies
└── manage.py               # Django CLI
```

---

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/register/` | Register new user |
| GET | `/api/activate/<uid>/<token>/` | Activate account |
| POST | `/api/login/` | Login (sets HTTP-Only cookies) |
| POST | `/api/logout/` | Logout |
| POST | `/api/token/refresh/` | Refresh access token |
| POST | `/api/password_reset/` | Request password reset |
| POST | `/api/password_confirm/<uid>/<token>/` | Set new password |

### Video Streaming

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/video/` | List all videos |
| GET | `/api/video/<id>/<resolution>/index.m3u8` | HLS manifest |
| GET | `/api/video/<id>/<resolution>/<segment>/` | HLS segment |

**Available resolutions:** 480p, 720p, 1080p

---

## Technologies

- **Python 3.14.0**
- **Django 6.0.1** - Web framework
- **Django REST Framework 3.16.1** - REST API
- **PostgreSQL** - Database
- **Redis 7.1.0** - Caching layer
- **Django RQ 3.2.2** - Background task queue
- **FFMPEG** - Video conversion to HLS
- **Simple JWT 5.5.1** - Authentication with HTTP-Only cookies
- **Docker 29.0.1** - Containerization
- **Gunicorn 23.0.0** - WSGI server
- **Whitenoise 6.11.0** - Static file serving

---

## Configuration

Environment variables in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | - |
| `DEBUG` | Debug mode | `True` |
| `ALLOWED_HOSTS` | Allowed hostnames | `localhost` |
| `DB_NAME` | Database name | `videoflix_db` |
| `DB_USER` | Database user | `videoflix_user` |
| `DB_PASSWORD` | Database password | `videoflix_password` |
| `EMAIL_HOST` | SMTP server | `smtp.gmail.com` |
| `EMAIL_HOST_USER` | SMTP username | - |
| `EMAIL_HOST_PASSWORD` | SMTP password | - |

### Email Configuration

**Development Mode (default):**
If `EMAIL_HOST_USER` is empty, emails are printed to Docker console logs.
After registration, find the activation link in the logs:
```bash
docker-compose logs -f web
```

**Production Mode:**
Configure real SMTP credentials in `.env`:
```
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your.email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833).

---

## Docker Commands

**Start containers:**
```bash
docker-compose up --build
```

**Stop containers:**
```bash
docker-compose down
```

**Run migrations:**
```bash
docker-compose exec web python manage.py migrate
```

**Create superuser:**
```bash
docker-compose exec web python manage.py createsuperuser
```

**View logs:**
```bash
docker-compose logs -f
```

---

## Video Upload

1. Login to Admin: http://localhost:8000/admin
2. Navigate to Videos → Add Video
3. Upload video file and thumbnail
4. HLS conversion runs automatically in background
5. Videos available at `/api/video/` after conversion

---

## Testing with Postman

Import the included Postman files:
- `Videoflix_API.postman_collection.json`
- `Videoflix_Environment.postman_environment.json`

---

## License

This project is part of the Developer Akademie curriculum.