"""
Management command to load sample data for testing.
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta
from resort_system.core.models import (
    Amenity, RoomType, Room, Resort, Guest, Reservation, PaymentTransaction
)


class Command(BaseCommand):
    help = 'Load sample data for the resort reservation system'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Create Amenities
        amenities = []
        amenity_data = [
            ('WiFi', 'High-speed internet access'),
            ('Swimming Pool', 'Outdoor heated swimming pool'),
            ('Gym', 'Fully equipped fitness center'),
            ('Spa', 'Professional spa services'),
            ('Restaurant', 'On-site dining facilities'),
            ('Parking', 'Free parking available'),
            ('Air Conditioning', 'Climate control'),
            ('Balcony', 'Private balcony/patio'),
        ]

        for name, desc in amenity_data:
            amenity, created = Amenity.objects.get_or_create(
                name=name,
                defaults={'description': desc}
            )
            amenities.append(amenity)
            if created:
                self.stdout.write(self.style.SUCCESS(f'  Created amenity: {name}'))

        # Create Room Types
        room_types = {}
        room_type_data = [
            ('Standard Room', 'Basic comfortable room', Decimal('100.00'), 2),
            ('Deluxe Room', 'Spacious room with premium amenities', Decimal('150.00'), 2),
            ('Suite', 'Large suite with separate living area', Decimal('250.00'), 4),
            ('Presidential Suite', 'Luxury suite with premium services', Decimal('500.00'), 4),
        ]

        for name, desc, price, capacity in room_type_data:
            room_type, created = RoomType.objects.get_or_create(
                name=name,
                defaults={
                    'description': desc,
                    'base_price': price,
                    'capacity': capacity
                }
            )
            room_types[name] = room_type
            if created:
                self.stdout.write(self.style.SUCCESS(f'  Created room type: {name}'))
                # Add amenities to room types
                room_type.amenities.add(amenities[0], amenities[2])  # WiFi, Gym

        # Create Resort
        resort, created = Resort.objects.get_or_create(
            name='KAELA Events Place and Private Resort',
            defaults={
                'description': 'A luxurious private resort offering world-class amenities and event spaces',
                'location': '0214 A. Mabini St, Purok 3, Mojon, Maloles, Philippines 3000',
                'city': 'Maloles',
                'country': 'Philippines',
                'phone': '0917 858 0963',
                'email': 'kaelaresor.ph@gmail.com',
                'website': 'https://www.kaela.com.ph',
                'total_rooms': 50,
                'max_occupancy': 200,
                'cancellation_policy': '48 hours notice required for free cancellation'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'  Created resort: {resort.name}'))

        # Create Rooms
        room_count = 0
        for floor in range(1, 6):  # 5 floors
            for room_num in range(1, 11):  # 10 rooms per floor
                room_number = f'{floor}{room_num:02d}'
                room_type = list(room_types.values())[room_count % len(room_types)]
                
                room, created = Room.objects.get_or_create(
                    room_number=room_number,
                    defaults={
                        'room_type': room_type,
                        'floor': floor,
                        'status': 'available'
                    }
                )
                if created:
                    room_count += 1

        self.stdout.write(self.style.SUCCESS(f'  Created {room_count} rooms'))

        # Create Guests
        guests = []
        guest_data = [
            ('Juan', 'Santos', 'juan.santos@email.com', '+63-917-123-4567', 'PH'),
            ('Maria', 'Cruz', 'maria.cruz@email.com', '+63-918-234-5678', 'PH'),
            ('Carlos', 'Rodriguez', 'carlos.rodriguez@email.com', '+63-919-345-6789', 'PH'),
            ('Emma', 'Reyes', 'emma.reyes@email.com', '+63-920-456-7890', 'PH'),
        ]

        for first_name, last_name, email, phone, country in guest_data:
            guest, created = Guest.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'phone': phone,
                    'country': country,
                    'guest_type': 'individual'
                }
            )
            guests.append(guest)
            if created:
                self.stdout.write(self.style.SUCCESS(f'  Created guest: {guest.full_name}'))

        # Create Reservations
        today = timezone.now().date()
        reservation_count = 0

        for i, guest in enumerate(guests):
            check_in = today + timedelta(days=i * 5)
            check_out = check_in + timedelta(days=3)
            room = Room.objects.filter(status='available').first()
            room_type = room.room_type if room else list(room_types.values())[0]
            price_per_night = room_type.base_price

            reservation, created = Reservation.objects.get_or_create(
                resort=resort,
                guest=guest,
                check_in_date=check_in,
                defaults={
                    'room': room,
                    'check_out_date': check_out,
                    'number_of_guests': 2,
                    'status': 'confirmed',
                    'total_nights': (check_out - check_in).days,
                    'price_per_night': price_per_night,
                    'total_price': price_per_night * (check_out - check_in).days,
                    'final_price': price_per_night * (check_out - check_in).days,
                    'special_requests': 'High floor preferred',
                    'confirmed_at': timezone.now()
                }
            )

            if created:
                reservation_count += 1
                # Create payment transaction
                PaymentTransaction.objects.create(
                    reservation=reservation,
                    payment_method='credit_card',
                    amount=reservation.final_price,
                    status='completed',
                    transaction_id=f'TRX{reservation.id:06d}'
                )

        self.stdout.write(self.style.SUCCESS(f'  Created {reservation_count} reservations'))
        self.stdout.write(self.style.SUCCESS('\nSample data loaded successfully!'))
