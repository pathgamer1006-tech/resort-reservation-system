# Setup Guide for Resort Reservation System

## Complete Setup Instructions

This document provides step-by-step instructions for setting up and running the Resort Reservation System.

### System Requirements
- Python 3.8 or higher
- pip (Python package manager)
- Windows, macOS, or Linux OS

### Step 1: Environment Setup

1. **Navigate to project directory**
```bash
cd resort-reservation-system
```

2. **Create virtual environment** (if not already created)
```bash
python -m venv venv
```

3. **Activate virtual environment**
   - **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   - **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Database Setup

1. **Create migrations**
```bash
python manage.py makemigrations
```

2. **Apply migrations**
```bash
python manage.py migrate
```

3. **Create superuser**
```bash
python manage.py createsuperuser
```
   Follow the prompts to create your admin account.

4. **Load sample data** (optional)
```bash
python manage.py load_sample_data
```

### Step 4: Run Development Server

```bash
python manage.py runserver
```

The server will start at `http://localhost:8000/`

### Step 5: Access Admin Interface

1. Open your browser and go to: `http://localhost:8000/admin/`
2. Log in with your superuser credentials
3. Start managing resorts, rooms, guests, and reservations

## Available Commands

### Django Management Commands

```bash
# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data
python manage.py load_sample_data

# Run development server
python manage.py runserver

# Run server on specific port
python manage.py runserver 0.0.0.0:8080

# Interactive shell
python manage.py shell

# Database shell
python manage.py dbshell

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic
```

## Project Structure Overview

### Main Components

```
resort-reservation-system/
├── resort_system/              # Main Django project
│   ├── core/                   # Core application with all models
│   ├── reservations/           # Reserved for future reservation features
│   ├── guests/                 # Reserved for future guest features
│   ├── utils/                  # Utility functions and validators
│   ├── settings.py             # Django configuration
│   ├── urls.py                 # URL routing
│   └── wsgi.py                 # WSGI configuration
├── manage.py                   # Django management script
└── requirements.txt            # Python dependencies
```

## Key Features

### Admin Interface Features

1. **Amenities Management**
   - Create and manage resort amenities
   - Assign amenities to room types

2. **Room Types Management**
   - Define room categories with pricing
   - Set capacity and base price
   - Manage amenities per room type

3. **Room Management**
   - Register individual rooms
   - Track room status
   - View availability and reservations

4. **Resort Management**
   - Create and manage resort properties
   - Set policies and operational times
   - View revenue statistics

5. **Guest Management**
   - Maintain guest profiles
   - Track booking history
   - View guest statistics

6. **Reservation Management**
   - Create and confirm reservations
   - Automatic price calculation
   - Handle cancellations

7. **Payment Tracking**
   - Record transactions
   - Track payment status
   - Generate transaction reports

## Atomic Architecture Benefits

1. **Modularity**: Each component is independent and focused
2. **Maintainability**: Easy to understand and modify specific features
3. **Scalability**: Simple to add new apps or features
4. **Testability**: Each module can be tested separately
5. **Reusability**: Utilities and components can be reused

## Troubleshooting

### Issue: Port 8000 already in use
**Solution:** Run on a different port
```bash
python manage.py runserver 8001
```

### Issue: Module not found errors
**Solution:** Ensure virtual environment is activated and dependencies are installed
```bash
pip install -r requirements.txt
```

### Issue: Database errors
**Solution:** Reset the database
```bash
# Delete db.sqlite3 file
python manage.py migrate
python manage.py createsuperuser
python manage.py load_sample_data
```

### Issue: Admin interface not accessible
**Solution:** Create a superuser
```bash
python manage.py createsuperuser
```

## Security Recommendations

1. **Production Deployment**
   - Change `SECRET_KEY` in settings.py
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS` properly
   - Use environment variables for sensitive data

2. **Database**
   - Use PostgreSQL for production
   - Set up regular backups
   - Use strong passwords

3. **Access Control**
   - Keep admin credentials secure
   - Use strong passwords
   - Enable HTTPS in production

## Next Steps

1. **Explore Admin Interface**: Familiarize yourself with all models and features
2. **Load Sample Data**: Use `python manage.py load_sample_data` to populate test data
3. **Create Custom Views**: Extend functionality with custom admin actions
4. **API Development**: Future versions can include REST API endpoints
5. **Reporting**: Add advanced analytics and reporting features

## Support & Documentation

- Django Official Documentation: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- Project README: See README.md for comprehensive documentation

---

**Last Updated**: December 2025
**Version**: 1.0.0
