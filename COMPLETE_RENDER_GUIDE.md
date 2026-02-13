# Complete Render Deployment Guide with PostgreSQL

This guide covers deploying your Resort Reservation System on Render with a PostgreSQL database.

## Part 1: Create PostgreSQL Database on Render

### Step 1: Create the Database

1. Go to https://dashboard.render.com
2. Click **"New +"** → Select **"PostgreSQL"**
3. Fill in the form:
   - **Name**: `resort-reservation-db`
   - **Database**: `resort_system`
   - **User**: `resort_user`
   - **Region**: Choose your region
   - **Plan**: Free
4. Click **"Create Database"**

### Step 2: Copy Connection Details

Once created, you'll see a connection string like:
```
postgresql://resort_user:xxxxxxxx@dpg-xxxxx.xxx.render.com:5432/resort_system
```

**Save this - you'll need it in the next step!**

## Part 2: Deploy Web Service on Render

### Step 1: Create Web Service

1. Click **"New +"** → Select **"Web Service"**
2. Connect your GitHub account
3. Select: `resort-reservation-system` repository
4. Click **"Create Web Service"**

### Step 2: Configure Build & Start Commands

```
Build Command: pip install -r requirements.txt
Start Command: gunicorn resort_system.wsgi --log-file -
```

### Step 3: Add Environment Variables

Click **"Environment"** and add these variables:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | Generate one using: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `your-app-name.onrender.com` |
| `CORS_ALLOWED_ORIGINS` | `https://your-app-name.onrender.com` |
| `DATABASE_URL` | Paste the PostgreSQL connection string from Part 1 |

### Step 4: Deploy

Click **"Create Web Service"** and wait for deployment (usually 2-3 minutes).

## Part 3: Initialize Database

Once deployed, initialize the database:

### Step 1: Open Shell

In your Render dashboard:
1. Go to your web service
2. Click **"Shell"** tab

### Step 2: Run Setup Commands

```bash
# Run migrations
python manage.py migrate

# Load sample data
python manage.py load_sample_data

# Create admin user
python manage.py createsuperuser
```

When creating the superuser, follow the prompts:
```
Username: admin
Email: your-email@example.com
Password: (enter a secure password)
```

## Part 4: Access Your Application

Once everything is deployed:

- **Main Website**: `https://your-app-name.onrender.com`
- **Admin Panel**: `https://your-app-name.onrender.com/admin`
  - Login with the admin credentials you created

## Database Features

✅ **PostgreSQL on Render provides:**
- Persistent database (survives redeploys)
- Automatic backups
- 90-day free tier (then deleted if inactive)
- Upgradable to paid plans for production

## Verify Database Connection

To check if PostgreSQL is connected properly:

1. Open Shell in Render dashboard
2. Run: `python manage.py dbshell`
3. You should see a PostgreSQL prompt: `resort_system=#`
4. Type `\dt` to list all tables
5. Type `\q` to exit

## Auto-Redeploy on Push

Your Render service is configured to auto-redeploy when you push to the `main` branch:

```bash
git add .
git commit -m "Your changes"
git push origin main
```

Render will automatically rebuild and redeploy! 🎉

## Troubleshooting

### Database Connection Fails
- Check that DATABASE_URL is correctly set in Environment variables
- Make sure PostgreSQL database was created first
- Verify the connection string is correct

### Migrations Fail
- Open Shell and run manually: `python manage.py migrate`
- Check logs for specific error messages

### Admin Login Fails
- Run: `python manage.py createsuperuser` in Shell
- Make sure you created a superuser account

## Useful Render Commands

**View Logs:**
```bash
# In Render Shell
tail -f logs/debug.log
```

**Run Django Shell:**
```bash
python manage.py shell
```

**Check Database Size:**
```bash
python manage.py dbshell
# Then: SELECT pg_size_pretty(pg_database_size('resort_system'));
```

## Production Checklist

Before going live:
- [ ] Generate a strong SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS with your domain
- [ ] Set up email notifications
- [ ] Enable HTTPS (automatic on Render)
- [ ] Set up database backups
- [ ] Create admin account
- [ ] Test booking flow

## Support

- Render Docs: https://render.com/docs
- Django Docs: https://docs.djangoproject.com
- PostgreSQL Docs: https://www.postgresql.org/docs/

---

**You're all set! Your Resort Reservation System is now live on Render! 🏨🚀**
