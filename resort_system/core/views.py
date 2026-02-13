"""
Views file for the core app.
Includes authentication, booking, and admin sales management.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from datetime import datetime
import uuid
from .models import Resort, Reservation, Guest, Room, Amenity, RoomType, PaymentTransaction
from resort_system.utils.validators import validate_check_in_out_dates


def index(request):
    """
    Landing page view for the resort reservation system.
    Displays resort information and booking form.
    """
    context = {
        'total_resorts': Resort.objects.count(),
        'total_amenities': Amenity.objects.count(),
        'room_types': RoomType.objects.all(),
    }
    
    return render(request, 'index.html', context)


def login_view(request):
    """
    Login page for admin users.
    """
    # If already logged in as admin, redirect to dashboard
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if user is staff
            if user.is_staff:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                return render(request, 'login.html', {'error': 'This account is not an admin account. Please use guest login.'})
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')


def logout_view(request):
    """
    Logout user and redirect to home.
    """
    logout(request)
    return redirect('index')


def user_signup(request):
    """
    User registration/signup page.
    """
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        
        errors = []
        
        # Validation
        if not username or len(username) < 3:
            errors.append('Username must be at least 3 characters long')
        if User.objects.filter(username=username).exists():
            errors.append('Username already taken')
        if not email or '@' not in email:
            errors.append('Valid email is required')
        if User.objects.filter(email=email).exists():
            errors.append('Email already registered')
        if not password or len(password) < 6:
            errors.append('Password must be at least 6 characters long')
        if password != password_confirm:
            errors.append('Passwords do not match')
        
        if not errors:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            # Log them in
            login(request, user)
            return redirect('index')
        
        return render(request, 'user_signup.html', {'errors': errors})
    
    return render(request, 'user_signup.html')


def user_login(request):
    """
    Unified login page for both guests and admin users.
    """
    if request.user.is_authenticated:
        # If already logged in as admin, redirect to dashboard
        if request.user.is_staff:
            return redirect('admin_dashboard')
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirect to admin dashboard if staff, otherwise to home
            if user.is_staff:
                return redirect('admin_dashboard')
            else:
                return redirect('index')
        else:
            return render(request, 'user_login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'user_login.html')


def admin_dashboard(request):
    """
    Admin dashboard view with sales statistics.
    """
    # Redirect to login if not authenticated or not staff
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')
    
    resorts = Resort.objects.all()
    reservations = Reservation.objects.all().order_by('-created_at')
    total_sales = sum(r.final_price for r in Reservation.objects.filter(status='confirmed'))
    pending_count = Reservation.objects.filter(status='pending').count()
    confirmed_count = Reservation.objects.filter(status='confirmed').count()
    
    context = {
        'total_resorts': Resort.objects.count(),
        'total_reservations': Reservation.objects.count(),
        'total_guests': Guest.objects.count(),
        'pending_reservations': pending_count,
        'confirmed_reservations': confirmed_count,
        'total_sales': total_sales,
        'reservations': reservations[:20],  # Latest 20 reservations
        'resorts': resorts,
    }
    
    return render(request, 'admin/dashboard.html', context)


@login_required(login_url='login')
def sales_list(request):
    """
    List all reservations/sales with filters.
    """
    reservations = Reservation.objects.all().order_by('-created_at')
    status_filter = request.GET.get('status')
    
    if status_filter:
        reservations = reservations.filter(status=status_filter)
    
    total_sales = sum(r.final_price for r in Reservation.objects.filter(status='confirmed'))
    
    context = {
        'reservations': reservations,
        'total_sales': total_sales,
        'status_filter': status_filter,
    }
    
    return render(request, 'admin/sales_list.html', context)


@login_required(login_url='login')
def reservation_detail(request, reservation_id):
    """
    View and manage individual reservation details.
    """
    reservation = get_object_or_404(Reservation, id=reservation_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['pending', 'confirmed', 'checked_in', 'checked_out', 'cancelled']:
            reservation.status = new_status
            reservation.save()
            return redirect('sales_list')
    
    context = {
        'reservation': reservation,
    }
    
    return render(request, 'admin/reservation_detail.html', context)


@login_required(login_url='login')
def create_reservation_admin(request):
    """
    Admin form to create new reservations.
    """
    if request.method == 'POST':
        # Get form data
        guest_name = request.POST.get('guest_name')
        guest_email = request.POST.get('guest_email')
        guest_phone = request.POST.get('guest_phone')
        room_id = request.POST.get('room')
        check_in_str = request.POST.get('check_in')
        check_out_str = request.POST.get('check_out')
        num_guests = int(request.POST.get('num_guests', 1))
        status = request.POST.get('status', 'pending')
        
        # Parse dates
        check_in = datetime.strptime(check_in_str, '%Y-%m-%d').date()
        check_out = datetime.strptime(check_out_str, '%Y-%m-%d').date()
        
        # Validate dates
        try:
            validate_check_in_out_dates(check_in, check_out)
        except Exception as e:
            rooms = Room.objects.filter(status='available')
            return render(request, 'admin/create_reservation.html', {
                'rooms': rooms,
                'statuses': ['pending', 'confirmed', 'checked_in', 'checked_out', 'cancelled'],
                'error': str(e)
            })
        
        # Get or create guest
        guest, _ = Guest.objects.get_or_create(
            name=guest_name,
            defaults={'email': guest_email, 'phone': guest_phone, 'type': 'individual'}
        )
        
        # Check if guest has an active reservation
        active_reservation = Reservation.objects.filter(
            guest=guest,
            status__in=['pending', 'confirmed', 'checked_in']
        ).first()
        
        if active_reservation:
            rooms = Room.objects.filter(status='available')
            return render(request, 'admin/create_reservation.html', {
                'rooms': rooms,
                'statuses': ['pending', 'confirmed', 'checked_in', 'checked_out', 'cancelled'],
                'error': f'Guest already has an active reservation (ID: {active_reservation.id}). Please complete or cancel it before creating a new one.'
            })
        
        # Get room
        room = get_object_or_404(Room, id=room_id)
        resort = room.resort
        
        # Create reservation
        reservation = Reservation.objects.create(
            resort=resort,
            room=room,
            guest=guest,
            check_in_date=check_in,
            check_out_date=check_out,
            num_guests=num_guests,
            status=status,
        )
        
        return redirect('reservation_detail', reservation_id=reservation.id)
    
    rooms = Room.objects.filter(status='available')
    context = {
        'rooms': rooms,
        'statuses': ['pending', 'confirmed', 'checked_in', 'checked_out', 'cancelled'],
    }
    
    return render(request, 'admin/create_reservation.html', context)


@login_required(login_url='login')
def delete_reservation(request, reservation_id):
    """
    Delete a reservation.
    """
    reservation = get_object_or_404(Reservation, id=reservation_id)
    
    if request.method == 'POST':
        reservation.delete()
        return redirect('sales_list')
    
    context = {'reservation': reservation}
    return render(request, 'admin/delete_reservation.html', context)


@login_required(login_url='login')
def edit_reservation(request, reservation_id):
    """
    Edit reservation details.
    """
    reservation = get_object_or_404(Reservation, id=reservation_id)
    
    if request.method == 'POST':
        check_in_str = request.POST.get('check_in')
        check_out_str = request.POST.get('check_out')
        num_guests = request.POST.get('num_guests')
        status = request.POST.get('status')
        
        # Validate dates if provided
        if check_in_str and check_out_str:
            check_in = datetime.strptime(check_in_str, '%Y-%m-%d').date()
            check_out = datetime.strptime(check_out_str, '%Y-%m-%d').date()
            
            try:
                validate_check_in_out_dates(check_in, check_out)
                reservation.check_in_date = check_in
                reservation.check_out_date = check_out
            except Exception as e:
                return render(request, 'admin/edit_reservation.html', {
                    'reservation': reservation,
                    'statuses': ['pending', 'confirmed', 'checked_in', 'checked_out', 'cancelled'],
                    'error': str(e)
                })
        
        if num_guests:
            reservation.num_guests = int(num_guests)
        if status:
            reservation.status = status
        
        reservation.save()
        return redirect('reservation_detail', reservation_id=reservation.id)
    
    context = {
        'reservation': reservation,
        'statuses': ['pending', 'confirmed', 'checked_in', 'checked_out', 'cancelled'],
    }
    
    return render(request, 'admin/edit_reservation.html', context)


def book_reservation(request):
    """
    Simple public booking form submission.
    """
    if request.method == 'POST':
        guest_name = request.POST.get('guest_name')
        guest_email = request.POST.get('guest_email')
        guest_phone = request.POST.get('guest_phone')
        check_in_str = request.POST.get('check_in')
        check_out_str = request.POST.get('check_out')
        package_type = request.POST.get('package_type')
        num_guests = int(request.POST.get('num_guests', 1))
        
        try:
            # Parse dates
            check_in = datetime.strptime(check_in_str, '%Y-%m-%d').date()
            check_out = datetime.strptime(check_out_str, '%Y-%m-%d').date()
            
            # Validate dates using the validator function
            validate_check_in_out_dates(check_in, check_out)
            
            # Get or create guest
            guest, _ = Guest.objects.get_or_create(
                email=guest_email,
                defaults={
                    'first_name': guest_name.split()[0] if guest_name else 'Guest',
                    'last_name': ' '.join(guest_name.split()[1:]) if len(guest_name.split()) > 1 else '',
                    'phone': guest_phone
                }
            )
            
            # Check if guest has an active reservation
            active_reservation = Reservation.objects.filter(
                guest=guest,
                status__in=['pending', 'confirmed', 'checked_in']
            ).first()
            
            if active_reservation:
                return render(request, 'booking_confirmation.html', {
                    'error': f'You already have an active reservation (ID: {active_reservation.id}). Please complete or cancel it before booking again.'
                })
            
            # Get first resort and first room
            resort = Resort.objects.first()
            room = Room.objects.first()
            
            if not resort or not room:
                return render(request, 'booking_confirmation.html', 
                            {'error': 'System configuration incomplete. Please contact support.'})
            
            # Calculate nights
            nights = (check_out - check_in).days
            base_price = 5000  # Simple base price per night
            
            # Create reservation
            reservation = Reservation.objects.create(
                resort=resort,
                room=room,
                guest=guest,
                check_in_date=check_in,
                check_out_date=check_out,
                number_of_guests=num_guests,
                total_nights=nights,
                price_per_night=base_price,
                total_price=nights * base_price,
                final_price=nights * base_price,
                package_type=package_type,
                status='pending',
            )
            
            # Create payment transaction
            PaymentTransaction.objects.create(
                reservation=reservation,
                amount=reservation.final_price,
                status='pending',
                transaction_id=f"TXN-{uuid.uuid4().hex[:12].upper()}",
            )
            
            return render(request, 'booking_confirmation.html', {
                'reservation': reservation,
                'success': True,
            })
        
        except Exception as e:
            return render(request, 'booking_confirmation.html', 
                        {'error': str(e)})
    
    return redirect('index')


def amenities_view(request):
    """
    Amenities page showing all resort amenities.
    """
    amenities = Amenity.objects.all()
    
    context = {
        'amenities': amenities,
        'total_amenities': amenities.count(),
    }
    return render(request, 'amenities.html', context)


def about_view(request):
    """
    About page with resort information.
    """
    resorts = Resort.objects.all()
    
    context = {
        'resorts': resorts,
        'total_resorts': resorts.count(),
    }
    return render(request, 'about.html', context)


def contact_view(request):
    """
    Contact page with resort contact information.
    """
    resorts = Resort.objects.all()
    
    context = {
        'resorts': resorts,
    }
    return render(request, 'contact.html', context)


def packages_view(request):
    """
    Packages page displaying all KAELA resort offerings.
    """
    context = {
        'total_amenities': Amenity.objects.count(),
    }
    return render(request, 'packages.html', context)


@login_required(login_url='user_login')
def guest_dashboard(request):
    """
    Guest dashboard showing their reservations and booking status.
    """
    try:
        guest = Guest.objects.get(email=request.user.email)
        reservations = guest.reservations.all().order_by('-created_at')
    except Guest.DoesNotExist:
        reservations = []
    
    # Count pending and confirmed reservations
    pending_count = Reservation.objects.filter(
        guest__email=request.user.email, 
        status='pending'
    ).count()
    
    confirmed_count = Reservation.objects.filter(
        guest__email=request.user.email, 
        status='confirmed'
    ).count()
    
    context = {
        'reservations': reservations,
        'pending_count': pending_count,
        'confirmed_count': confirmed_count,
        'user': request.user,
    }
    
    return render(request, 'guest_dashboard.html', context)
