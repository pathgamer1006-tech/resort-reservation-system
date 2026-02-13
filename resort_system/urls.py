"""
URL configuration for resort_system project.
"""

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from resort_system.core.views import (
    index, 
    login_view, 
    logout_view, 
    user_signup,
    user_login,
    admin_dashboard,
    sales_list,
    reservation_detail,
    create_reservation_admin,
    delete_reservation,
    edit_reservation,
    book_reservation,
    amenities_view,
    about_view,
    contact_view,
    packages_view,
    guest_dashboard,
)

# Customize admin site
admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE
admin.site.index_title = settings.ADMIN_INDEX_TITLE

urlpatterns = [
    # Public pages
    path('', index, name='index'),  # Landing page
    path('packages/', packages_view, name='packages'),
    path('amenities/', amenities_view, name='amenities'),
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),
    
    # User authentication
    path('user-login/', user_login, name='user_login'),
    path('user-signup/', user_signup, name='user_signup'),
    path('logout/', logout_view, name='logout'),
    path('guest-dashboard/', guest_dashboard, name='guest_dashboard'),
    
    # Admin authentication
    path('admin-login/', login_view, name='login'),
    path('book/', book_reservation, name='book_reservation'),
    
    # Admin pages
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('sales/', sales_list, name='sales_list'),
    path('reservation/<int:reservation_id>/', reservation_detail, name='reservation_detail'),
    path('reservation/<int:reservation_id>/edit/', edit_reservation, name='edit_reservation'),
    path('reservation/<int:reservation_id>/delete/', delete_reservation, name='delete_reservation'),
    path('create-reservation/', create_reservation_admin, name='create_reservation'),
    
    # Django admin
    path('admin/', admin.site.urls),
    path('api/', include('rest_framework.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
