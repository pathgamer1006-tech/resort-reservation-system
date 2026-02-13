"""
Admin configuration for core models.
Atomic principle: Separate admin classes for each model.
Only admins can access and modify resort data.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count
from .models import (
    Amenity, RoomType, Room, Resort, Guest, Reservation, PaymentTransaction
)


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    """Admin interface for Amenities - simple atomic responsibility."""
    list_display = ['name', 'description_short', 'room_types_count']
    search_fields = ['name', 'description']
    list_filter = ['room_types']
    
    def description_short(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_short.short_description = 'Description'
    
    def room_types_count(self, obj):
        return obj.room_types.count()
    room_types_count.short_description = 'Used in Room Types'


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    """Admin interface for Room Types."""
    list_display = ['name', 'base_price', 'capacity', 'amenities_list', 'rooms_count']
    search_fields = ['name', 'description']
    list_filter = ['capacity', 'base_price']
    filter_horizontal = ['amenities']
    readonly_fields = ['rooms_count']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'capacity')
        }),
        ('Pricing', {
            'fields': ('base_price',)
        }),
        ('Amenities', {
            'fields': ('amenities',)
        }),
        ('Statistics', {
            'fields': ('rooms_count',),
            'classes': ('collapse',)
        }),
    )
    
    def amenities_list(self, obj):
        amenities = obj.amenities.all()
        if amenities:
            return ', '.join([a.name for a in amenities[:3]]) + \
                   (f' +{amenities.count() - 3}' if amenities.count() > 3 else '')
        return '—'
    amenities_list.short_description = 'Amenities'
    
    def rooms_count(self, obj):
        return obj.rooms.count()
    rooms_count.short_description = 'Total Rooms'


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Admin interface for Rooms."""
    list_display = ['room_number', 'room_type', 'floor', 'status_badge', 'created_at']
    search_fields = ['room_number', 'room_type__name']
    list_filter = ['status', 'room_type', 'floor']
    readonly_fields = ['created_at', 'updated_at', 'reservation_history']
    fieldsets = (
        ('Room Information', {
            'fields': ('room_type', 'room_number', 'floor')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Reservation History', {
            'fields': ('reservation_history',),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'available': '#28a745',
            'occupied': '#dc3545',
            'maintenance': '#ffc107',
            'reserved': '#17a2b8',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def reservation_history(self, obj):
        reservations = obj.reservations.all()[:5]
        if not reservations:
            return 'No reservations yet'
        html = '<ul>'
        for res in reservations:
            html += f'<li>{res.guest.full_name} - {res.check_in_date} to {res.check_out_date}</li>'
        html += '</ul>'
        return format_html(html)
    reservation_history.short_description = 'Recent Reservations'


@admin.register(Resort)
class ResortAdmin(admin.ModelAdmin):
    """Admin interface for Resorts."""
    list_display = ['name', 'city', 'country', 'total_rooms', 'active_status', 'updated_at']
    search_fields = ['name', 'city', 'country', 'email']
    list_filter = ['is_active', 'country', 'created_at']
    readonly_fields = ['created_at', 'updated_at', 'total_reservations', 'revenue_info']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'website')
        }),
        ('Location', {
            'fields': ('location', 'city', 'country')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone')
        }),
        ('Operating Information', {
            'fields': ('total_rooms', 'check_in_time', 'check_out_time', 'max_occupancy')
        }),
        ('Policies', {
            'fields': ('cancellation_policy',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Statistics & Dates', {
            'fields': ('total_reservations', 'revenue_info', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def active_status(self, obj):
        color = '#28a745' if obj.is_active else '#dc3545'
        status = 'Active' if obj.is_active else 'Inactive'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            status
        )
    active_status.short_description = 'Status'
    
    def total_reservations(self, obj):
        return obj.reservations.count()
    total_reservations.short_description = 'Total Reservations'
    
    def revenue_info(self, obj):
        from django.db.models import Sum
        total_revenue = obj.reservations.filter(
            status__in=['confirmed', 'checked_in', 'checked_out']
        ).aggregate(total=Sum('final_price'))['total'] or 0
        return format_html(f'<strong>${total_revenue:,.2f}</strong>')
    revenue_info.short_description = 'Total Revenue'


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    """Admin interface for Guests."""
    list_display = ['full_name', 'email', 'phone', 'guest_type', 'active_status', 'reservation_count', 'date_joined']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    list_filter = ['guest_type', 'is_active', 'country', 'date_joined']
    readonly_fields = ['date_joined', 'reservation_history', 'total_spent']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Address & Country', {
            'fields': ('address', 'country')
        }),
        ('Guest Type', {
            'fields': ('guest_type',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Statistics', {
            'fields': ('date_joined', 'reservation_history', 'total_spent'),
            'classes': ('collapse',)
        }),
    )
    
    def active_status(self, obj):
        color = '#28a745' if obj.is_active else '#dc3545'
        status = 'Active' if obj.is_active else 'Inactive'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            status
        )
    active_status.short_description = 'Status'
    
    def reservation_count(self, obj):
        return obj.reservations.count()
    reservation_count.short_description = 'Reservations'
    
    def reservation_history(self, obj):
        reservations = obj.reservations.all()[:10]
        if not reservations:
            return 'No reservations'
        html = '<ol>'
        for res in reservations:
            html += f'<li>{res.resort.name} - {res.check_in_date} to {res.check_out_date} ({res.get_status_display()})</li>'
        html += '</ol>'
        return format_html(html)
    reservation_history.short_description = 'Recent Reservations'
    
    def total_spent(self, obj):
        from django.db.models import Sum
        total = obj.reservations.filter(
            status__in=['confirmed', 'checked_in', 'checked_out']
        ).aggregate(total=Sum('final_price'))['total'] or 0
        return format_html(f'<strong>${total:,.2f}</strong>')
    total_spent.short_description = 'Total Spent'


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """Admin interface for Reservations."""
    list_display = ['reservation_id', 'guest_name', 'resort_name', 'room_number', 
                    'check_in_date', 'check_out_date', 'status_badge', 'final_price']
    search_fields = ['id', 'guest__first_name', 'guest__last_name', 'resort__name', 'room__room_number']
    list_filter = ['status', 'resort', 'check_in_date', 'created_at']
    readonly_fields = ['created_at', 'updated_at', 'confirmed_at', 'cancelled_at', 'price_breakdown']
    
    fieldsets = (
        ('Reservation Details', {
            'fields': ('resort', 'guest', 'room')
        }),
        ('Dates', {
            'fields': ('check_in_date', 'check_out_date', 'total_nights')
        }),
        ('Guest Information', {
            'fields': ('number_of_guests', 'special_requests')
        }),
        ('Pricing', {
            'fields': ('price_per_night', 'total_price', 'discount', 'final_price', 'price_breakdown'),
            'classes': ('wide',)
        }),
        ('Status', {
            'fields': ('status', 'confirmed_at', 'cancelled_at', 'cancellation_reason')
        }),
        ('Additional Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def reservation_id(self, obj):
        return f"#{obj.id}"
    reservation_id.short_description = 'ID'
    
    def guest_name(self, obj):
        return obj.guest.full_name
    guest_name.short_description = 'Guest'
    
    def resort_name(self, obj):
        return obj.resort.name
    resort_name.short_description = 'Resort'
    
    def room_number(self, obj):
        return obj.room.room_number
    room_number.short_description = 'Room'
    
    def status_badge(self, obj):
        colors = {
            'pending': '#ffc107',
            'confirmed': '#28a745',
            'checked_in': '#17a2b8',
            'checked_out': '#6c757d',
            'cancelled': '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def price_breakdown(self, obj):
        html = f'''
        <table style="border-collapse: collapse; width: 300px;">
            <tr style="border-bottom: 1px solid #ddd;">
                <td style="padding: 5px;">Price per Night:</td>
                <td style="padding: 5px; text-align: right;"><strong>${obj.price_per_night}</strong></td>
            </tr>
            <tr style="border-bottom: 1px solid #ddd;">
                <td style="padding: 5px;">Total Nights:</td>
                <td style="padding: 5px; text-align: right;"><strong>{obj.total_nights}</strong></td>
            </tr>
            <tr style="border-bottom: 1px solid #ddd;">
                <td style="padding: 5px;">Subtotal:</td>
                <td style="padding: 5px; text-align: right;"><strong>${obj.total_price}</strong></td>
            </tr>
            <tr style="border-bottom: 2px solid #ddd;">
                <td style="padding: 5px;">Discount:</td>
                <td style="padding: 5px; text-align: right;"><strong>-${obj.discount}</strong></td>
            </tr>
            <tr>
                <td style="padding: 5px;"><strong>TOTAL:</strong></td>
                <td style="padding: 5px; text-align: right;"><strong style="color: green;">${obj.final_price}</strong></td>
            </tr>
        </table>
        '''
        return format_html(html)
    price_breakdown.short_description = 'Price Breakdown'


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    """Admin interface for Payment Transactions."""
    list_display = ['transaction_id', 'reservation_id', 'guest_name', 'amount', 
                    'payment_method', 'status_badge', 'created_at']
    search_fields = ['transaction_id', 'reservation__id', 'reservation__guest__first_name',
                     'reservation__guest__last_name']
    list_filter = ['status', 'payment_method', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Transaction Information', {
            'fields': ('reservation', 'transaction_id')
        }),
        ('Payment Details', {
            'fields': ('payment_method', 'amount', 'status')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def reservation_id(self, obj):
        return f"#{obj.reservation.id}"
    reservation_id.short_description = 'Reservation'
    
    def guest_name(self, obj):
        return obj.reservation.guest.full_name
    guest_name.short_description = 'Guest'
    
    def status_badge(self, obj):
        colors = {
            'pending': '#ffc107',
            'completed': '#28a745',
            'failed': '#dc3545',
            'refunded': '#6c757d',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
