# Ecommerce Django Application

A simple, showcase-ready ecommerce web app built with Django 5.2.2. It demonstrates authentication, product catalog, cart, checkout simulation, and a clean URL/middleware setup.

## Features

- User auth: login, logout, registration, password reset
- Product categories, details pages
- Cart with add/increase/decrease/remove and totals
- Checkout and simulated payment + receipt page
- Middleware to require login for protected pages while allowing a public homepage
- Static and media handling (Pillow, Whitenoise)

## Tech Stack

- Python 3.11+
- Django 5.2.2
- SQLite (dev) / Postgres via `DATABASE_URL` (prod ready)
- Whitenoise for static files in production
- Gunicorn for production serving

## Local Development

1) Clone the repository and enter the project folder

2) Create and activate a virtual environment (recommended)

3) Install dependencies

```
pip install -r requirements.txt
```

4) Environment variables (optional in dev):
Copy `.env.example` to `.env` and adjust values when needed.

5) Apply migrations, create a superuser (optional), and run the server

```
cd Ecommerce
python manage.py migrate
# optional
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

## Project Structure

```
Ecommerce-Django/
├─ Ecommerce/                # Django project root
│  ├─ Ecommerce/             # Settings, urls, wsgi
│  ├─ app/                   # App with models, views, forms, urls, templates
│  ├─ media/                 # Uploaded images (dev)
│  └─ manage.py
├─ requirements.txt          # Python dependencies
├─ Procfile                  # Gunicorn entrypoint (for Render/Heroku-like platforms)
├─ render.yaml               # Render deploy blueprint
├─ .env.example              # Example environment variables
└─ .github/workflows/        # CI pipeline
```

## Production Settings

Settings are environment-driven in `Ecommerce/Ecommerce/settings.py`:

- `DJANGO_SECRET_KEY`: required in prod
- `DJANGO_DEBUG`: set to `False` in prod
- `ALLOWED_HOSTS`: comma-separated domains (e.g., `example.com,.onrender.com`)
- `CSRF_TRUSTED_ORIGINS`: comma-separated trusted origins (e.g., `https://*.onrender.com`)
- `DATABASE_URL`: Postgres URL if using a managed database
- Email settings via `EMAIL_*` variables

Static files are served with Whitenoise and collected into `staticfiles/` via `python manage.py collectstatic`.

## Deploy to Render (one-click style)

This repo includes `render.yaml` for a streamlined deploy:

1) Push this repository to GitHub
2) Create a new Web Service on Render, selecting this repo
3) Render will detect `render.yaml` and configure the service
4) Set environment variables as needed; `DJANGO_SECRET_KEY` is auto-generated
5) Render will build, collect static, and start Gunicorn

## GitHub Actions CI

The workflow `.github/workflows/django-ci.yml` runs on push/PR:
- Installs dependencies
- Runs migrations and `collectstatic`
- Executes Django tests

## License


This project is for educational and portfolio purposes. Use freely and adapt to your needs.
<img width="1920" height="926" alt="1" src="https://github.com/user-attachments/assets/1ca95f30-6b07-4613-86d9-ad8d7dcb4559" />


<img width="1920" height="924" alt="2" src="https://github.com/user-attachments/assets/7093b5b5-23b7-4975-b823-a9484cc49347" />


<img width="1920" height="939" alt="3" src="https://github.com/user-attachments/assets/0002732c-7d35-4cbb-851b-5a6222ad9f16" />



