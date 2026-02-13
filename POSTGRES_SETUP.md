# PostgreSQL Database Setup on Render

## Step 1: Create PostgreSQL Database on Render

1. **Go to Render Dashboard**: https://dashboard.render.com
2. **Click "New +"** and select **"PostgreSQL"**
3. **Fill in the details:**
   - **Name**: `resort-reservation-db`
   - **Database**: `resort_system`
   - **User**: `resort_user`
   - **Region**: Same as your web service
   - **Plan**: Free tier (PostgreSQL 15)

4. **Click "Create Database"**
5. **Copy the connection string** (it will look like):
   ```
   postgresql://resort_user:password@host:5432/resort_system
   ```

## Step 2: Update Your Web Service on Render

1. **Go to your Resort Reservation System web service**
2. **Click "Environment"**
3. **Add the DATABASE_URL:**
   - **Key**: `DATABASE_URL`
   - **Value**: Paste the connection string from Step 1

4. **Save** and your service will redeploy automatically

## Step 3: Run Migrations on Render

Once deployed with PostgreSQL:

1. **Click "Shell"** in your web service dashboard
2. **Run these commands:**

```bash
python manage.py migrate
python manage.py load_sample_data
python manage.py createsuperuser
```

3. **Create your admin account when prompted**

## What This Does

- ✅ Migrates all Django tables to PostgreSQL
- ✅ Loads sample resort, rooms, and amenities data
- ✅ Creates an admin user for managing the system

## Important Notes

- PostgreSQL databases on free tier have limits (90 days, then deleted if inactive)
- Use PostgreSQL for better scalability than SQLite
- Database URL is automatically managed by Render
- Migrations run automatically on deploy (via build.sh)

## Verify Database Connection

After migrations, you can verify in the Shell:

```bash
python manage.py dbshell
```

This opens a PostgreSQL shell where you can check tables:

```sql
\dt  -- List all tables
\q   -- Quit
```

---

That's it! Your Render deployment will now use a persistent PostgreSQL database. 🎉
