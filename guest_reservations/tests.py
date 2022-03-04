import imp
from urllib import response
from django.test import TestCase
from django.urls import reverse

# Create your tests here.

class GuestReservationTests(TestCase):
    def test_all_reservtions_page(self):
        response = self.client.get(reverse('guest_reservations:all_reservations'))
        self.assertTemplateUsed(response, 'guest_reservation/reservations.html')
        self.assertContains(response, text="Your Reservations", status_code=200, html=True)