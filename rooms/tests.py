from urllib import response
from django.test import TestCase
from .models import Amenities, Room
from django.contrib.auth import get_user_model

# Create your tests here.

User = get_user_model()
class RoomsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
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
    
    def test_home_featured_rooms(self):
        response = self.client.get('rooms:home')
        if response == self.client.get('rooms:home'):
            self.assertTemplateUsed(response, template_name='home.html')
        elif response == self.client.post('rooms:home'):
            self.assertRedirects(response, expected_url='rooms:check_room_availability', status_code=302, target_status_code=202, fetch_redirect_response=True)
