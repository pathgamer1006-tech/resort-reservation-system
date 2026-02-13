# Deployment Guide for Render

This guide will help you deploy the Resort Reservation System on Render's free tier.

## Prerequisites

1. **GitHub Account** - Your code must be on GitHub
2. **Render Account** - Sign up at https://render.com
3. **GitHub Repository** - https://github.com/pathgamer1006-tech/resort-reservation-system

## Step-by-Step Deployment

### 1. Connect GitHub to Render

1. Go to https://render.com and sign in
2. Click "New +" button and select "Web Service"
3. Click "Connect account" next to GitHub
4. Authorize Render to access your GitHub account
5. Select the `resort-reservation-system` repository

### 2. Configure the Web Service

**Basic Settings:**
- **Name**: `resort-reservation-system`
- **Environment**: `Python 3`
- **Region**: Choose your closest region
- **Branch**: `main`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn resort_system.wsgi --log-file -`

### 3. Add Environment Variables

In the Render dashboard, add the following environment variables:

```
SECRET_KEY=your-secure-random-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
CORS_ALLOWED_ORIGINS=https://your-app-name.onrender.com
```

**To generate a secure SECRET_KEY:**
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### 4. Database Setup (Optional but Recommended)

For free tier, SQLite will work, but for production consider:

1. Create a PostgreSQL database on Render
2. Add `DATABASE_URL` environment variable
3. Update requirements.txt with `psycopg2-binary`

### 5. Enable Auto-Deploy

- Check "Auto-deploy" checkbox
- Select branch: `main`
- This will automatically redeploy when you push to main

### 6. Deploy

1. Click "Create Web Service"
2. Render will start the build process
3. Check the logs for any errors
4. Once deployed, you'll get a URL like: `https://resort-reservation-system.onrender.com`

## Post-Deployment

### Create Admin User

Once deployed, you can create a superuser via the Render shell:

1. Go to your Render service dashboard
2. Click "Shell" tab
3. Run: `python manage.py createsuperuser`
4. Follow the prompts to create an admin account

### Accessing the Application

- **Main Site**: `https://your-app-name.onrender.com`
- **Admin Panel**: `https://your-app-name.onrender.com/admin`
- **API**: `https://your-app-name.onrender.com/api`

## Important Notes

### Free Tier Limitations

- Web services are spun down after 15 minutes of inactivity
- SQLite database (db.sqlite3) gets reset on redeploy
- Limited to 0.5 GB RAM

### Before Going to Production

1. Generate a strong `SECRET_KEY`
2. Set `DEBUG=False`
3. Use a persistent database (PostgreSQL recommended)
4. Set up proper ALLOWED_HOSTS
5. Configure email for notifications
6. Set up backups for the database

## Troubleshooting

### Service keeps crashing

Check logs for errors:
1. Click "Logs" tab in Render dashboard
2. Look for migration or import errors
3. Verify all environment variables are set

### Static files not loading

The project uses WhiteNoise to serve static files. This is already configured in `settings.py`.

### Database migrations fail

Run migrations manually in the Render shell:
```bash
python manage.py migrate
```

## Pushing Updates

After making changes locally:

```bash
git add .
git commit -m "Your commit message"
git push origin main
```

Render will automatically detect the push and redeploy!

## Need Help?

- Render Docs: https://render.com/docs
- Django Docs: https://docs.djangoproject.com
- Check the Render service logs for detailed error messages

Happy deploying! 🚀
