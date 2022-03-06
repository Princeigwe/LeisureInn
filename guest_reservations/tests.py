from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import GuestReservationList, ReservationItem
from bookings.models import Booking
from rooms.models import Amenities, Room
from .views import delete_reservation

User = get_user_model()

# Create your tests here.

class GuestReservationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """setting test database for the Test class"""
        cls.user = User.objects.create_user(
            # username='testuser',  # username is commented because CustomUser model is used instead of the default django user model for authentication
            password='testpass123',
            first_name='Test',
            last_name='User',
            email='testuser@gmail.com'
        )
        cls.user.save()
        cls.amenities = Amenities.objects.create(first_item="Television")
        cls.amenities.save()
        cls.room = Room.objects.create(
            room_number = '11A',
            room_picture = 'media/room_pictures/download_1_8M8nsPj.jpeg',
            is_available = True,
            is_booked = False,
            room_price = 20000,
            amenities_type = cls.amenities,
        )
        cls.booking = Booking.objects.create(
            room=cls.room,
            guest_firstname=cls.user.first_name,
            guest_lastname=cls.user.last_name,
            guest_email=cls.user.email,
            guest_telephone='000000000001',
            checked_in=False,
            check_in='2022-12-24',
            check_out='2022-12-25',
            checked_out=False,
            amount=20000,
            paid=True,
        )
        
        
        GuestReservationList.objects.get_or_create(guest=cls.user)
        guest_reservation_list = GuestReservationList.objects.get(guest=cls.user)
        ReservationItem.objects.create(reservation_list=guest_reservation_list, booking = cls.booking)
    
    def test_reservation_item_count(self):
        reservation_items = ReservationItem.objects.all()
        self.assertEquals(reservation_items.count(), 1)
    
    def test_all_reservations_page(self):
        self.client.login(username='testuser@gmail.com', password='testpass123')
        response = self.client.get(reverse('guest_reservations:all_reservations'))
        self.assertTemplateUsed(response, 'guest_reservation/reservations.html')
        self.assertContains(response, text="Your Reservations", status_code=200, html=True)
    
    def test_delete_reservation_page(self):
        self.client.login(username='testuser@gmail.com', password='testpass123')
        response = self.client.get(reverse('guest_reservations:delete_reservation', args=[1]))
        expected_url = reverse('guest_reservations:all_reservations')
        self.assertEquals(response.resolver_match.func, delete_reservation)
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200, fetch_redirect_response=True)
