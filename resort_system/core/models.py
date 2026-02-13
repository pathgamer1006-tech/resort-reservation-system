"""
Core models for the resort reservation system.
Atomic principle: Each model handles a single entity responsibility.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal


class Amenity(models.Model):
    """
    Amenity model - represents a single amenity offered by the resort.
    Examples: WiFi, Swimming Pool, Gym, Spa, etc.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # For icon representation
    
    class Meta:
        verbose_name_plural = "Amenities"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class RoomType(models.Model):
    """
    RoomType model - defines different types of rooms available.
    Examples: Single, Double, Suite, Presidential Suite, etc.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    base_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    capacity = models.IntegerField(validators=[MinValueValidator(1)])
    amenities = models.ManyToManyField(Amenity, related_name='room_types')
    
    class Meta:
        ordering = ['base_price']
    
    def __str__(self):
        return f"{self.name} (${self.base_price})"


class Room(models.Model):
    """
    Room model - represents a physical room in the resort.
    """
    room_type = models.ForeignKey(RoomType, on_delete=models.PROTECT, related_name='rooms')
    room_number = models.CharField(max_length=50, unique=True)
    floor = models.IntegerField(validators=[MinValueValidator(1)])
    
    ROOM_STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
        ('reserved', 'Reserved'),
    ]
    status = models.CharField(
        max_length=20, 
        choices=ROOM_STATUS_CHOICES, 
        default='available'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['floor', 'room_number']
    
    def __str__(self):
        return f"Room {self.room_number} ({self.room_type.name})"


class Resort(models.Model):
    """
    Resort model - represents the main resort entity.
    """
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    location = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True)
    
    # Operating information
    total_rooms = models.IntegerField(validators=[MinValueValidator(1)])
    check_in_time = models.TimeField(default='14:00')
    check_out_time = models.TimeField(default='11:00')
    
    # Policies
    cancellation_policy = models.TextField(blank=True)
    max_occupancy = models.IntegerField(validators=[MinValueValidator(1)])
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Guest(models.Model):
    """
    Guest model - represents a guest/customer.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    
    COUNTRY_CODES = [
        ('US', 'United States'),
        ('CA', 'Canada'),
        ('UK', 'United Kingdom'),
        ('AU', 'Australia'),
        ('IN', 'India'),
        ('DE', 'Germany'),
        ('FR', 'France'),
        ('JP', 'Japan'),
        ('CN', 'China'),
        ('BR', 'Brazil'),
    ]
    country = models.CharField(max_length=2, choices=COUNTRY_CODES, blank=True)
    
    address = models.TextField(blank=True)
    
    GUEST_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('corporate', 'Corporate'),
        ('group', 'Group'),
    ]
    guest_type = models.CharField(max_length=20, choices=GUEST_TYPE_CHOICES, default='individual')
    
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Reservation(models.Model):
    """
    Reservation model - represents a room reservation.
    Uses atomic principle with clear separation of concerns.
    """
    resort = models.ForeignKey(Resort, on_delete=models.CASCADE, related_name='reservations')
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='reservations')
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='reservations')
    
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_of_guests = models.IntegerField(validators=[MinValueValidator(1)])
    
    RESERVATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(
        max_length=20, 
        choices=RESERVATION_STATUS_CHOICES, 
        default='pending'
    )
    
    # Pricing
    total_nights = models.IntegerField(validators=[MinValueValidator(1)])
    price_per_night = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    total_price = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    discount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    final_price = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    # Special requests
    special_requests = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    package_type = models.CharField(max_length=100, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['resort', 'check_in_date']),
            models.Index(fields=['guest', 'status']),
            models.Index(fields=['room', 'check_in_date', 'check_out_date']),
        ]
    
    def __str__(self):
        return f"Reservation #{self.id} - {self.guest.full_name} at {self.resort.name}"
    
    def save(self, *args, **kwargs):
        """Override save to auto-calculate total nights and prices."""
        from datetime import timedelta
        
        if self.check_in_date and self.check_out_date:
            self.total_nights = (self.check_out_date - self.check_in_date).days
            
        if self.total_nights and self.price_per_night:
            self.total_price = self.price_per_night * self.total_nights
            self.final_price = self.total_price - self.discount
        
        super().save(*args, **kwargs)


class PaymentTransaction(models.Model):
    """
    PaymentTransaction model - handles payment records for reservations.
    Atomic principle: Isolated responsibility for payment tracking.
    """
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='payments')
    
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash'),
        ('wallet', 'Digital Wallet'),
    ]
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    transaction_id = models.CharField(max_length=100, unique=True, blank=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Payment #{self.id} - {self.reservation.id} - {self.amount}"
