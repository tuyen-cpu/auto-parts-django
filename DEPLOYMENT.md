# Deployment: Docker + Cloudflare R2

Project has a production-oriented Docker setup:

```text
web  Django + Gunicorn
db   PostgreSQL 16
```

## 1. Create production env

```powershell
copy .env.production.example .env.production
```

Update these values:

```env
DEBUG=False
SECRET_KEY=your-long-random-secret
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=https://your-domain.com,https://www.your-domain.com

POSTGRES_DB=autoparts
POSTGRES_USER=autoparts
POSTGRES_PASSWORD=change-this-password

USE_R2_STORAGE=True
R2_ACCOUNT_ID=your-cloudflare-account-id
R2_BUCKET_NAME=your-r2-bucket
R2_ACCESS_KEY_ID=your-r2-access-key-id
R2_SECRET_ACCESS_KEY=your-r2-secret-access-key
R2_REGION_NAME=auto
R2_LOCATION=media
R2_CUSTOM_DOMAIN=images.your-domain.com
R2_QUERYSTRING_AUTH=False
```

Cloudflare R2 uses an S3-compatible API. The default endpoint is:

```text
https://<ACCOUNT_ID>.r2.cloudflarestorage.com
```

Use `R2_CUSTOM_DOMAIN` when the bucket is exposed through a public custom domain. Uploaded images from Django Admin will then be stored in R2 instead of local `media/`.

## 2. Run with Docker Compose

```powershell
docker compose up --build -d
```

View logs:

```powershell
docker compose logs -f web
```

Create an admin user:

```powershell
docker compose exec web python manage.py createsuperuser
```

## 3. Startup commands

The container entrypoint runs these by default:

```bash
python manage.py migrate --noinput
python manage.py collectstatic --noinput
```

Control them with:

```env
RUN_MIGRATIONS=1
RUN_COLLECTSTATIC=1
```

## 4. Production notes

- Static files are served by WhiteNoise.
- Uploaded media files use Cloudflare R2 when `USE_R2_STORAGE=True`.
- PostgreSQL is required for production; do not use SQLite for business deployment.
- Back up PostgreSQL regularly.
- Keep `.env.production` private and never commit real secrets.
