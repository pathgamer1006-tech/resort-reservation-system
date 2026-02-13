# Resort Reservation System - Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Django Admin Interface                        │
│                   (http://localhost:8000/admin)                 │
└────────────┬────────────────────────────────────────────────────┘
             │
             │ Admin Authentication
             │ (Sessions & Permissions)
             │
┌────────────▼────────────────────────────────────────────────────┐
│                    Django URL Routing                            │
│                    (urls.py)                                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ /admin/ → Admin Interface                               │   │
│  │ /api/    → REST Framework URLs (Future)                │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────────┬────────────────────────────────────────────────────┘
             │
┌────────────▼─────────────────────────────────────────────────────┐
│                   Core Application (core/)                        │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │                      Admin Interface                     │    │
│  │ ┌────────┬────────┬────────┬────────┬────────┬────────┐ │    │
│  │ │Amenity │RoomType│ Room   │Resort  │ Guest  │Payment │ │    │
│  │ │Admin   │Admin   │Admin   │Admin   │Admin   │Admin   │ │    │
│  │ └────────┴────────┴────────┴────────┴────────┴────────┘ │    │
│  │                   Custom Admin Classes                   │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │                    Models (Data Layer)                   │    │
│  │                                                           │    │
│  │  ┌─────────┐    ┌──────────┐    ┌─────────┐            │    │
│  │  │ Amenity │◄───┤ RoomType ├───►│  Room   │            │    │
│  │  └─────────┘    └──────────┘    └────┬────┘            │    │
│  │       ▲                             │   │                │    │
│  │       │                             │   │                │    │
│  │  ┌────┴──────┐             ┌───────┴─┐ │                │    │
│  │  │   Resort  │             │Reservation
│  │  └─────┬─────┘             └─────────┘ │                │    │
│  │        │                       │        │                │    │
│  │        └─────────┬─────────────┘        │                │    │
│  │                  │                      │                │    │
│  │          ┌───────▼────────┐     ┌──────▼──────┐         │    │
│  │          │     Guest      │─────┤  Payment    │         │    │
│  │          │                │     │ Transaction │         │    │
│  │          └────────────────┘     └─────────────┘         │    │
│  │                                                           │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │                  Utilities & Helpers                      │    │
│  │                                                           │    │
│  │  ┌──────────────────────────────────────────────────┐    │    │
│  │  │ validators.py                                   │    │    │
│  │  │ • validate_check_in_out_dates()                 │    │    │
│  │  │ • validate_guest_capacity()                     │    │    │
│  │  │ • calculate_total_nights()                      │    │    │
│  │  │ • calculate_reservation_price()                 │    │    │
│  │  │ • check_room_availability()                     │    │    │
│  │  │ • get_room_availability_status()                │    │    │
│  │  │ • generate_transaction_id()                     │    │    │
│  │  └──────────────────────────────────────────────────┘    │    │
│  │                                                           │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
                           │
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌───────▼─────┐   ┌────────▼────────┐   ┌───▼────────┐
│ Future Apps │   │   Utils Module   │   │ Middleware │
│             │   │                  │   │            │
│ ┌─────────┐ │   │ ┌──────────────┐ │   │ ┌────────┐ │
│ │Guests   │ │   │ │  validators  │ │   │ │CORS    │ │
│ │Portal   │ │   │ ├──────────────┤ │   │ ├────────┤ │
│ └─────────┘ │   │ │ serializers  │ │   │ │CSRF    │ │
│             │   │ │ (Ready for   │ │   │ ├────────┤ │
│ ┌─────────┐ │   │ │  REST API)   │ │   │ │Auth    │ │
│ │API      │ │   │ └──────────────┘ │   │ └────────┘ │
│ │Endpoints│ │   │                  │   │            │
│ └─────────┘ │   │                  │   │            │
│             │   │                  │   │            │
└─────────────┘   └──────────────────┘   └────────────┘
        │                                       │
        └───────────────────┬───────────────────┘
                            │
                ┌───────────▼───────────┐
                │  SQLite Database      │
                │  (db.sqlite3)         │
                │                       │
                │  Tables:              │
                │  • auth_user          │
                │  • core_amenity       │
                │  • core_roomtype      │
                │  • core_room          │
                │  • core_resort        │
                │  • core_guest         │
                │  • core_reservation   │
                │  • core_payment       │
                │  • auth_permission    │
                │  • auth_group         │
                │                       │
                └───────────────────────┘
```

## Data Model Relationships

```
┌──────────────┐
│   Amenity    │
│              │
│ • id (PK)    │
│ • name       │
│ • description│
│ • icon       │
└────────┬─────┘
         │ M:M (Many to Many)
         │
┌────────▼────────────┐
│   RoomType          │
│                     │
│ • id (PK)           │
│ • name              │
│ • description       │
│ • base_price        │
│ • capacity          │
│ • amenities (M:M)   │
└────────┬────────────┘
         │ 1:M (One to Many)
         │
┌────────▼──────────┐
│   Room            │
│                   │
│ • id (PK)         │
│ • room_type (FK)  │
│ • room_number     │
│ • floor           │
│ • status          │
│ • created_at      │
│ • updated_at      │
└──────┬──────┬─────┘
       │      │
       │      └─────────┐
       │ 1:M             │
       │                 │
┌──────▼─────────────┐  │
│   Resort          │  │
│                   │  │
│ • id (PK)         │  │
│ • name            │  │ 1:M
│ • description     │  │
│ • location        │  │
│ • city            │  │
│ • country         │  │
│ • check_in_time   │  │
│ • check_out_time  │  │
│ • policies        │  │
└──────┬────────────┘  │
       │                │
       │ 1:M            │
┌──────▼──────────────────────┐
│   Reservation              │
│                            │
│ • id (PK)                  │
│ • resort (FK) ◄────────────┘
│ • guest (FK)
│ • room (FK) ◄──────────────┐
│ • check_in_date            │
│ • check_out_date           │
│ • number_of_guests         │
│ • status                   │
│ • total_nights (Auto)      │
│ • price_per_night          │
│ • total_price (Auto)       │
│ • discount                 │
│ • final_price (Auto)       │
│ • special_requests         │
│ • notes                    │
│ • created_at               │
│ • updated_at               │
│ • confirmed_at             │
│ • cancelled_at             │
└──────┬──────────────────────┘
       │ 1:M
       │
       │      ┌─────────────────┐
       │      │      Guest      │
       │      │                 │
       │      │ • id (PK)       │
       │      │ • first_name    │
       │      │ • last_name     │
       │      │ • email         │
       │      │ • phone         │
       │      │ • country       │
       │      │ • address       │
       │      │ • guest_type    │
       │      │ • date_joined   │
       │      │ • is_active     │
       │      └─────────────────┘
       │
       │ 1:M
       │
┌──────▼──────────────────┐
│   PaymentTransaction    │
│                         │
│ • id (PK)               │
│ • reservation (FK)      │
│ • payment_method        │
│ • amount                │
│ • status                │
│ • transaction_id        │
│ • notes                 │
│ • created_at            │
│ • updated_at            │
└─────────────────────────┘
```

## Data Flow - Creating a Reservation

```
1. Admin Opens Admin Interface
   ↓
2. Admin Clicks "Add Reservation"
   ↓
3. Admin Selects:
   • Resort (from Resort table)
   • Guest (from Guest table)
   • Room (from available Room list)
   • Check-in Date
   • Check-out Date
   • Number of Guests
   ↓
4. System Validates:
   • check_in_date < check_out_date
   • number_of_guests ≤ room.room_type.capacity
   • room is available for selected dates
   ↓
5. System Auto-Calculates (on save):
   • total_nights = check_out_date - check_in_date
   • price_per_night = room.room_type.base_price
   • total_price = price_per_night × total_nights
   • final_price = total_price - discount
   ↓
6. Reservation Saved to Database
   ↓
7. Payment Transaction Created
   ↓
8. Room Status Updated (if needed)
   ↓
9. Admin Sees Confirmation with Details
```

## Technology Stack

```
┌────────────────────────────────────────────────┐
│         Frontend: Django Admin Interface       │
└────────────────────────────────────────────────┘
                          │
┌────────────────────────▼────────────────────────┐
│  Backend Framework: Django 4.2                 │
│  • URL Router                                  │
│  • ORM (Object-Relational Mapping)             │
│  • Admin Interface                             │
│  • Authentication & Authorization              │
│  • Middleware Stack                            │
└────────────────────────▼────────────────────────┘
                          │
┌────────────────────────▼────────────────────────┐
│  Database: SQLite (Development)                │
│            PostgreSQL (Production Ready)       │
└────────────────────────▼────────────────────────┘
                          │
┌────────────────────────▼────────────────────────┐
│  Supporting Libraries:                         │
│  • Django REST Framework (Future API)          │
│  • django-cors-headers (CORS support)          │
│  • django-filter (Advanced filtering)          │
│  • Pillow (Image handling)                     │
│  • python-dotenv (Environment variables)       │
└────────────────────────────────────────────────┘
```

## Atomic Design Principles Applied

```
┌─────────────────────────────────────────────────┐
│  Single Responsibility Principle                │
│ ┌────────────────────────────────────────────┐  │
│ │ Each model has ONE clear purpose:          │  │
│ │ • Amenity: Resort feature                  │  │
│ │ • RoomType: Room category with price       │  │
│ │ • Room: Physical room inventory            │  │
│ │ • Resort: Property management              │  │
│ │ • Guest: Customer profile                  │  │
│ │ • Reservation: Booking record              │  │
│ │ • PaymentTransaction: Payment tracking     │  │
│ └────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  Separation of Concerns                        │
│ ┌────────────────────────────────────────────┐  │
│ │ • core/: Main models and admin             │  │
│ │ • reservations/: Reservation logic (ready) │  │
│ │ • guests/: Guest features (ready)          │  │
│ │ • utils/: Shared utilities                 │  │
│ │ • templates/: HTML templates               │  │
│ │ • static/: CSS, JS, images                 │  │
│ └────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  DRY Principle (Don't Repeat Yourself)         │
│ ┌────────────────────────────────────────────┐  │
│ │ • Shared validators in utils/validators.py │  │
│ │ • Reusable admin classes                   │  │
│ │ • Common configuration in settings.py      │  │
│ │ • Shared utilities for calculations        │  │
│ └────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  Extensibility & Scalability                   │
│ ┌────────────────────────────────────────────┐  │
│ │ Easy to add:                               │  │
│ │ • New apps (just create new directory)    │  │
│ │ • New models (extend existing apps)       │  │
│ │ • REST API endpoints (ready with views.py)│  │
│ │ • Guest portal (use guests/ app)          │  │
│ │ • Email notifications (add signals)       │  │
│ │ • Payment processing (extend admin)       │  │
│ └────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

## Admin Interface Flow

```
Admin Login (auth/login)
         ↓
Django Admin Dashboard (/admin/)
    ├─ Amenities
    ├─ Room Types
    ├─ Rooms
    ├─ Resorts
    ├─ Guests
    ├─ Reservations
    │  ├─ View List (with color-coded status)
    │  ├─ Add New
    │  ├─ View Details
    │  │  ├─ Price Breakdown
    │  │  ├─ Reservation History
    │  │  └─ Payment Records
    │  ├─ Edit
    │  └─ Delete/Cancel
    └─ Payment Transactions
       ├─ View List (with status)
       ├─ Record New Payment
       └─ Track History
```

---

## System Statistics

- **Total Models**: 7
- **Total Admin Classes**: 7 (one per model)
- **Total Fields**: 80+ across all models
- **Total Relationships**: 6 (foreign keys & many-to-many)
- **Sample Data Records**: 70+ (resorts, rooms, guests, reservations, etc.)
- **Lines of Code (Models + Admin)**: 800+
- **Validators/Utilities**: 10+
- **Built-in Admin Features**: 50+ (filtering, searching, editing, etc.)

This architecture ensures a scalable, maintainable, and extensible system that follows industry best practices and Django conventions.
