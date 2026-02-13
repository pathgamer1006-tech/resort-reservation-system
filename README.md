# Resort Reservation System

A comprehensive Django-based resort reservation management system designed for administrators to manage resort operations, room inventory, guest information, and reservations.

## Features

### Core Features
- **Resort Management**: Create and manage multiple resort properties with detailed information
- **Room Management**: Organize rooms by type, floor, and capacity with real-time status tracking
- **Guest Management**: Maintain comprehensive guest profiles with contact information and history
- **Reservation System**: Handle room bookings with automatic price calculations and discounts
- **Payment Tracking**: Record and track payment transactions for reservations
- **Admin Dashboard**: Intuitive Django admin interface for all operations

### Technical Features
- **Atomic Architecture**: Clean separation of concerns with focused, atomic modules
- **Database Relationships**: Proper foreign keys and many-to-many relationships
- **Price Calculations**: Automatic calculation of reservation prices based on duration
- **Room Availability**: Real-time room availability checking
- **Transaction History**: Comprehensive logging and tracking of all transactions
- **Admin-Only Access**: Secure access control through Django admin authentication

## Project Structure

```
resort-reservation-system/
├── resort_system/                 # Main Django project
│   ├── core/                      # Core models and admin configuration
│   │   ├── models.py              # All data models
│   │   ├── admin.py               # Admin interface configuration
│   │   ├── apps.py                # App configuration
│   │   └── __init__.py
│   ├── reservations/              # Reservations app (atomic separation)
│   ├── guests/                    # Guests app (atomic separation)
│   ├── utils/                     # Utility functions
│   │   ├── validators.py          # Validation and helper functions
│   │   └── __init__.py
│   ├── static/                    # Static files (CSS, JS)
│   ├── templates/                 # HTML templates
│   ├── settings.py                # Django settings
│   ├── urls.py                    # URL routing
│   ├── wsgi.py                    # WSGI configuration
│   └── __init__.py
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Models

### Core Models (Atomic Design)

1. **Amenity**: Represents resort amenities (WiFi, Pool, Gym, etc.)
2. **RoomType**: Defines room categories with base pricing and capacity
3. **Room**: Individual room instances with status tracking
4. **Resort**: Main resort property information
5. **Guest**: Guest/customer profiles
6. **Reservation**: Booking records with pricing and status
7. **PaymentTransaction**: Payment tracking for reservations

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
```bash
cd resort-reservation-system
```

2. **Create a virtual environment**
```bash
python -m venv venv
```

3. **Activate the virtual environment**
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Apply migrations**
```bash
python manage.py migrate
```

6. **Create a superuser (admin account)**
```bash
python manage.py createsuperuser
```

7. **Load sample data (optional)**
```bash
python manage.py loaddata sample_data
```

## Running the Application

### Start the development server
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000/`

### Access the Admin Interface
Navigate to `http://localhost:8000/admin/` and log in with your superuser credentials.

## Admin Interface Guide

### Amenities Management
- Add, edit, and delete resort amenities
- View which room types have specific amenities

### Room Types Management
- Create room type categories (Single, Double, Suite, etc.)
- Set base pricing and capacity
- Assign amenities to room types

### Rooms Management
- Register individual rooms
- Assign room types and floor numbers
- Track room status (Available, Occupied, Maintenance, Reserved)
- View reservation history for each room

### Resort Management
- Create and manage multiple resorts
- Set check-in/check-out times
- Define cancellation policies
- View revenue statistics

### Guests Management
- Register guest profiles
- Track guest booking history
- View total spending and reservation count
- Manage guest types (Individual, Corporate, Group)

### Reservations Management
- Create new reservations
- Track reservation status (Pending, Confirmed, Checked In, Checked Out, Cancelled)
- View detailed price breakdown
- Manage special requests and notes

### Payment Transactions
- Record payment information
- Track payment status
- Manage transaction IDs
- View payment history

## Admin-Only Features

All modifications to the system are restricted to authenticated admin users:
- Only admins can create/edit resorts, rooms, and room types
- Only admins can confirm reservations
- Payment processing is admin-controlled
- Guest records can only be modified by admins

## Database

The system uses SQLite by default for development. For production, consider using PostgreSQL or MySQL.

To use PostgreSQL:

1. Install the psycopg2 adapter:
```bash
pip install psycopg2-binary
```

2. Update `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'resort_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## API Endpoints (Future)

Future versions will include REST API endpoints for:
- Guest registration and profile management
- Reservation booking
- Payment processing
- Room availability queries

## Atomic Architecture Principles

The project follows atomic design principles:

1. **Single Responsibility**: Each model handles one entity
2. **Clear Separation**: Apps separated by domain (core, reservations, guests)
3. **Focused Utilities**: Helper functions in dedicated utils module
4. **Reusable Components**: Admin classes follow DRY principle
5. **Database Integrity**: Proper relationships and constraints

## Security Considerations

- Change `SECRET_KEY` in `settings.py` for production
- Set `DEBUG = False` in production
- Configure `ALLOWED_HOSTS` properly
- Use environment variables for sensitive data
- Enable HTTPS in production
- Configure database backups

## Contributing

Guidelines for extending the system:

1. Create new apps following the atomic principle
2. Add models to the appropriate app
3. Register models in admin.py
4. Add validators for data integrity
5. Create unit tests for new features

## Support

For issues, questions, or contributions, please contact the development team.

## License

This project is provided as-is for educational and commercial use.

---

**Last Updated**: December 2025
**Django Version**: 4.2.0
