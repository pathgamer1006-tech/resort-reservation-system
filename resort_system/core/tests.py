"""
Test file structure for the resort reservation system.
This demonstrates how to test models and admin functionality.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone

from .models import Amenity, RoomType, Room, Resort, Guest, Reservation, PaymentTransaction


class AmenityModelTest(TestCase):
    """Tests for Amenity model."""
    
    def setUp(self):
        self.amenity = Amenity.objects.create(
            name='WiFi',
            description='High-speed internet'
        )
    
    def test_amenity_creation(self):
        self.assertEqual(self.amenity.name, 'WiFi')
        self.assertEqual(str(self.amenity), 'WiFi')


class RoomTypeModelTest(TestCase):
    """Tests for RoomType model."""
    
    def setUp(self):
        self.amenity = Amenity.objects.create(name='WiFi')
        self.room_type = RoomType.objects.create(
            name='Standard Room',
            description='Basic room',
            base_price=Decimal('100.00'),
            capacity=2
        )
        self.room_type.amenities.add(self.amenity)
    
    def test_room_type_creation(self):
        self.assertEqual(self.room_type.name, 'Standard Room')
        self.assertEqual(self.room_type.base_price, Decimal('100.00'))
        self.assertEqual(self.room_type.capacity, 2)


class RoomModelTest(TestCase):
    """Tests for Room model."""
    
    def setUp(self):
        self.room_type = RoomType.objects.create(
            name='Standard Room',
            description='Basic room',
            base_price=Decimal('100.00'),
            capacity=2
        )
        self.room = Room.objects.create(
            room_type=self.room_type,
            room_number='101',
            floor=1,
            status='available'
        )
    
    def test_room_creation(self):
        self.assertEqual(self.room.room_number, '101')
        self.assertEqual(self.room.floor, 1)
        self.assertEqual(self.room.status, 'available')


class ResortModelTest(TestCase):
    """Tests for Resort model."""
    
    def setUp(self):
        self.resort = Resort.objects.create(
            name='Test Resort',
            description='A test resort',
            location='123 Beach Road',
            city='Miami',
            country='United States',
            phone='+1-305-555-0100',
            email='test@resort.com',
            total_rooms=50,
            max_occupancy=200
        )
    
    def test_resort_creation(self):
        self.assertEqual(self.resort.name, 'Test Resort')
        self.assertEqual(self.resort.city, 'Miami')


class GuestModelTest(TestCase):
    """Tests for Guest model."""
    
    def setUp(self):
        self.guest = Guest.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='+1-305-555-0100'
        )
    
    def test_guest_creation(self):
        self.assertEqual(self.guest.full_name, 'John Doe')
        self.assertEqual(str(self.guest), 'John Doe')


class ReservationModelTest(TestCase):
    """Tests for Reservation model."""
    
    def setUp(self):
        self.room_type = RoomType.objects.create(
            name='Standard Room',
            description='Basic room',
            base_price=Decimal('100.00'),
            capacity=2
        )
        self.room = Room.objects.create(
            room_type=self.room_type,
            room_number='101',
            floor=1
        )
        self.resort = Resort.objects.create(
            name='Test Resort',
            description='A test resort',
            location='123 Beach Road',
            city='Miami',
            country='United States',
            phone='+1-305-555-0100',
            email='test@resort.com',
            total_rooms=50,
            max_occupancy=200
        )
        self.guest = Guest.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='+1-305-555-0100'
        )
        
        self.check_in = timezone.now().date() + timedelta(days=1)
        self.check_out = self.check_in + timedelta(days=3)
        
        self.reservation = Reservation.objects.create(
            resort=self.resort,
            guest=self.guest,
            room=self.room,
            check_in_date=self.check_in,
            check_out_date=self.check_out,
            number_of_guests=2,
            total_nights=3,
            price_per_night=Decimal('100.00'),
            total_price=Decimal('300.00'),
            final_price=Decimal('300.00')
        )
    
    def test_reservation_creation(self):
        self.assertEqual(self.reservation.total_nights, 3)
        self.assertEqual(self.reservation.final_price, Decimal('300.00'))
    
    def test_reservation_auto_calculation(self):
        # Test that save() automatically calculates nights and prices
        reservation = Reservation(
            resort=self.resort,
            guest=self.guest,
            room=self.room,
            check_in_date=self.check_in,
            check_out_date=self.check_out,
            number_of_guests=2,
            price_per_night=Decimal('100.00')
        )
        reservation.save()
        self.assertEqual(reservation.total_nights, 3)
        self.assertEqual(reservation.total_price, Decimal('300.00'))


class PaymentTransactionModelTest(TestCase):
    """Tests for PaymentTransaction model."""
    
    def setUp(self):
        # Create necessary objects
        self.room_type = RoomType.objects.create(
            name='Standard Room',
            description='Basic room',
            base_price=Decimal('100.00'),
            capacity=2
        )
        self.room = Room.objects.create(
            room_type=self.room_type,
            room_number='101',
            floor=1
        )
        self.resort = Resort.objects.create(
            name='Test Resort',
            description='A test resort',
            location='123 Beach Road',
            city='Miami',
            country='United States',
            phone='+1-305-555-0100',
            email='test@resort.com',
            total_rooms=50,
            max_occupancy=200
        )
        self.guest = Guest.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='+1-305-555-0100'
        )
        
        self.check_in = timezone.now().date() + timedelta(days=1)
        self.check_out = self.check_in + timedelta(days=3)
        
        self.reservation = Reservation.objects.create(
            resort=self.resort,
            guest=self.guest,
            room=self.room,
            check_in_date=self.check_in,
            check_out_date=self.check_out,
            number_of_guests=2,
            total_nights=3,
            price_per_night=Decimal('100.00'),
            total_price=Decimal('300.00'),
            final_price=Decimal('300.00')
        )
        
        self.payment = PaymentTransaction.objects.create(
            reservation=self.reservation,
            payment_method='credit_card',
            amount=Decimal('300.00'),
            status='completed',
            transaction_id='TRX000001'
        )
    
    def test_payment_creation(self):
        self.assertEqual(self.payment.amount, Decimal('300.00'))
        self.assertEqual(self.payment.status, 'completed')
