from django.http import response
from django.test import TestCase
from .models import Booking
from rooms.models import Room, Amenities
import datetime
from .views import booking_failed, booking_successful
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your tests here.

class BookingTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """creating dummy data"""
        cls.user = User.objects.create_user(
            # username='testuser',  # username is commented because CustomUser model is used instead of the default django user model for authentication
            password='testpass123',
            first_name='Test',
            last_name='User',
            email='testuser@gmail.com'
        )
        cls.user.save()
        cls.amenities = Amenities.objects.create(item_type= 'SINGLE ROOM')
        cls.room = Room.objects.create(
            room_number = '11A',
            room_picture = 'media/room_pictures/download_1_5DAVHfj.jpeg',
            room_type = 'SINGLE ROOM',
            is_available = True,
            is_booked = False,
            room_price = 1000.00,
            amenities_type = cls.amenities
        )
        cls.booking = Booking.objects.create(
            
            room = cls.room,
            guest_firstname = 'John Smith',
            guest_lastname = 'Smith',
            guest_email = 'john@gmail.com',
            guest_telephone = '0909090909',
            checked_in = False,
            check_in = datetime.date(2022, 2, 16),
            check_out = datetime.date(2022, 2, 17),
            amount = 10000,
            paid = True,
        )
        return cls.booking
    
    
    def test_booking_form_page(self):
        """ testing the response of 'bookings/booking_process/1/', based on HTTP method (POST/GET) """
        self.client.login(username='testuser@gmail.com', password='testpass123')
        if response == self.client.get('bookings/booking_process/1/'):
            self.assertTemplateUsed(response, 'booking/booking_form.html')
        elif response == self.client.post('bookings/booking_process/1/', data={'guest_telephone': '0909090909', 'amount':10000}):
            self.assertRedirects(response, 'payments/1/', status_code=302, target_status_code=200, fetch_redirect_response=True)
    

    ## to test views that have authentication required, comment the @login_required decorator
    
    def test_booking_failed_view(self):
        self.client.login(username='testuser@gmail.com', password='testpass123')
        response = self.client.get(reverse('bookings:booking_failed'))
        self.assertEqual(response.resolver_match.func, booking_failed)
        self.assertTemplateUsed(response, 'booking/booking_failed.html')
    
    
    def test_booking_successful_page(self):
        self.client.login(username='testuser@gmail.com', password='testpass123')
        response = self.client.get(reverse('bookings:booking_successful'))
        self.assertEqual(response.resolver_match.func, booking_successful)
        self.assertTemplateUsed(response, 'booking/booking_successful.html')
