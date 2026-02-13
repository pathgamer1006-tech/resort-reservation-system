"""
Utility functions for validations and helper methods.
Atomic principle: Focused utility functions.
"""

from datetime import datetime, timedelta
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_check_in_out_dates(check_in_date, check_out_date):
    """
    Validate that check-out date is after check-in date.
    """
    if check_in_date >= check_out_date:
        raise ValidationError(
            "Check-out date must be after check-in date."
        )
    
    if check_in_date < timezone.now().date():
        raise ValidationError(
            "Check-in date cannot be in the past."
        )


def validate_guest_capacity(number_of_guests, room_capacity):
    """
    Validate that number of guests doesn't exceed room capacity.
    """
    if number_of_guests > room_capacity:
        raise ValidationError(
            f"Number of guests ({number_of_guests}) exceeds room capacity ({room_capacity})."
        )


def calculate_total_nights(check_in_date, check_out_date):
    """
    Calculate the total number of nights between two dates.
    """
    if isinstance(check_in_date, str):
        check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d').date()
    if isinstance(check_out_date, str):
        check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d').date()
    
    return (check_out_date - check_in_date).days


def calculate_reservation_price(price_per_night, total_nights, discount=Decimal('0')):
    """
    Calculate the final reservation price after discount.
    """
    if total_nights <= 0:
        raise ValueError("Total nights must be greater than 0")
    
    total_price = price_per_night * total_nights
    final_price = total_price - discount
    
    return {
        'total_price': total_price,
        'final_price': final_price,
        'discount': discount
    }


def check_room_availability(room, check_in_date, check_out_date, exclude_reservation_id=None):
    """
    Check if a room is available for the given dates.
    Returns True if available, False otherwise.
    """
    from .models import Reservation
    
    # Check room status
    if room.status not in ['available', 'reserved']:
        return False
    
    # Check for overlapping reservations
    overlapping = Reservation.objects.filter(
        room=room,
        status__in=['confirmed', 'checked_in'],
        check_in_date__lt=check_out_date,
        check_out_date__gt=check_in_date
    )
    
    if exclude_reservation_id:
        overlapping = overlapping.exclude(id=exclude_reservation_id)
    
    return not overlapping.exists()


def get_room_availability_status(room):
    """
    Get a detailed availability status for a room.
    """
    from .models import Reservation
    
    next_reservation = Reservation.objects.filter(
        room=room,
        status__in=['confirmed', 'checked_in']
    ).order_by('check_in_date').first()
    
    return {
        'room': room,
        'current_status': room.status,
        'next_available': next_reservation.check_out_date if next_reservation else None,
        'is_available': room.status in ['available', 'reserved']
    }


def format_price(amount):
    """
    Format price to currency format.
    """
    return f"${amount:,.2f}"


def generate_transaction_id():
    """
    Generate a unique transaction ID.
    """
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    import random
    random_suffix = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    return f"TRX{timestamp}{random_suffix}"
