# Render PostgreSQL Setup - Quick Checklist

## ✅ What's Been Updated

Your code now supports both SQLite (local development) and PostgreSQL (Render production).

### Files Updated:
- ✅ `settings.py` - Added PostgreSQL support via dj-database-url
- ✅ `requirements.txt` - Added psycopg2-binary & dj-database-url
- ✅ `build.sh` - Includes automatic data loading
- ✅ Created `COMPLETE_RENDER_GUIDE.md` - Step-by-step deployment instructions
- ✅ Created `POSTGRES_SETUP.md` - Database setup guide

---

## 🚀 Step-by-Step: Deploy with PostgreSQL

### Step 1: Create PostgreSQL Database (5 minutes)

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Fill in:
   - **Name**: `resort-reservation-db`
   - **Database**: `resort_system`
   - **User**: `resort_user`
   - **Region**: Your region
   - **Plan**: Free
4. Click **"Create Database"**
5. **Copy the connection string** (you'll need this!)

### Step 2: Create Web Service (5 minutes)

1. Click **"New +"** → **"Web Service"**
2. Connect GitHub → Select your repository
3. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn resort_system.wsgi --log-file -`
4. Click **"Create Web Service"**

### Step 3: Add Environment Variables (2 minutes)

In the Render dashboard, go to your web service → **Environment** → Add:

```
SECRET_KEY=<generate one with Python>
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
CORS_ALLOWED_ORIGINS=https://your-app-name.onrender.com
DATABASE_URL=<paste PostgreSQL connection string from Step 1>
```

### Step 4: Deploy (2-3 minutes)

Wait for the deployment to finish. You can watch the logs.

### Step 5: Initialize Database (2 minutes)

Once deployed:
1. Click **"Shell"** in your Render dashboard
2. Run these commands:

```bash
python manage.py migrate
python manage.py load_sample_data
python manage.py createsuperuser
```

3. Create your admin account when prompted

---

## ✨ You're Done!

Your app is now live at: `https://your-app-name.onrender.com`

**Admin Panel**: `https://your-app-name.onrender.com/admin`

---

## 🔑 Key Features Enabled

✅ **Persistent Database** - PostgreSQL survives redeploys  
✅ **Auto-Scaling** - Works with Render's infrastructure  
✅ **Auto-Redeploy** - Push to `main` branch, auto-deploys  
✅ **Sample Data** - Loads automatically on build  
✅ **Admin Interface** - Full Django admin panel  
✅ **Static Files** - WhiteNoise serves CSS, images, etc.  

---

## 📖 Full Guides

- **Complete Deployment**: See `COMPLETE_RENDER_GUIDE.md`
- **Database Setup**: See `POSTGRES_SETUP.md`
- **Render Docs**: https://render.com/docs

---

## ⚡ Free Tier Limits

- PostgreSQL: 90 days free (then deleted if inactive)
- Web service: Spins down after 15 min inactivity
- Upgradable to paid plans for production use

**Ready to deploy? Follow the 5 steps above! 🎉**
