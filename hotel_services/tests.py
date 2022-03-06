from ast import arg
import re
from urllib import response
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Service, Subscription, GuestCreatedSubscription, OneTimeService, GuestOneTimeServicePayment
from django.urls import reverse
from django.test.utils import setup_test_environment,teardown_test_environment

User = get_user_model()



# Create your tests here.

class HotelServiceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """setting up test data for the test class"""
        cls.user = User.objects.create_user(
            # username='testuser',  # username is commented because CustomUser model is used instead of the default django user model for authentication
            password='testpass123',
            first_name='Test',
            last_name='User',
            email='testuser@gmail.com'
        )
        cls.user.save()

        cls.service = Service.objects.create(
            name = 'Spa',
            image = 'media/hotel_services/spa.jpeg',
            description = 'Leisure Inn spa service'
        )

        cls.subscription = Subscription.objects.create(
            service = cls.service,
            image = 'media/hotel_services/spa_1_R14xXDH.jpeg',
            plan = 'Standard',
            days = '5',
            price = '10000',
            description = 'A standard spa subscription service'
        )

        cls.guestCreatedSubscription = GuestCreatedSubscription.objects.create(
            subscription = cls.subscription,
            guest = cls.user,
            cancelled = False,
            date_created = '2022-12-24',
            date_cancelled = '2022-12-29',
            payment_id = '0'
        )

        cls.oneTimeService = OneTimeService.objects.create(
            service = cls.service,
            price = 11000
        )

        cls.guestOneTimeServicePayment = GuestOneTimeServicePayment.objects.create(
            service = cls.oneTimeService,
            guest = cls.user,
            paid = True,
            paid_date = '2022-12-29'
        )
        teardown_test_environment()
        setup_test_environment()
    
    
    def test_database_models(self):
        """testing created data models"""
        users = User.objects.all()
        services = Service.objects.all()
        subscriptions = Subscription.objects.all()
        guestCreatedSubscriptions = GuestCreatedSubscription.objects.all()
        oneTimeServices = OneTimeService.objects.all()
        guestOneTimeServicePayments = GuestOneTimeServicePayment.objects.all()

        self.assertEqual(users.count(), 1)
        self.assertEqual(services.count(), 1)
        self.assertEqual(subscriptions.count(), 1)
        self.assertEqual(guestCreatedSubscriptions.count(), 1)
        self.assertEqual(oneTimeServices.count(), 1)
        self.assertEqual(guestOneTimeServicePayments.count(), 1)

    def test_all_services_page(self):
        """testing the all_service_page view function"""
        response = self.client.get(reverse('hotel_services:all_services'), data={'name': 'spa', 'image':'media/hotel_services/spa.jpeg'}) # reversing url with query parameters
        self.assertTemplateUsed( response, 'hotel_services/hotel_services.html')

    def test_service_subscriptions(self):
        service = Service.objects.get(id=1, name='Spa')
        response = self.client.get(reverse('hotel_services:service_subscriptions', args=[str(service.name), int(service.id)])) # reversing url with parameters
        self.assertContains(response, text='Standard') # checking if "Standard" is in the template
        self.assertTemplateUsed(response, 'hotel_services/hotel_services_detail.html')


    def test_fetch_guest_subscriptions(self):
        self.client.login(username='testuser@gmail.com', password='testpass123')
        user = User.objects.get(email='testuser@gmail.com')
        guestCreatedSubscriptions = GuestCreatedSubscription.objects.filter(guest__email=user.email)
        response = self.client.get(reverse('hotel_services:fetch_guest_subscriptions'))
        self.assertTemplateUsed(response, template_name='hotel_services/guest_created_subscriptions.html')
        self.assertQuerysetEqual(response.context['guestCreatedSubscriptions'], guestCreatedSubscriptions, transform=lambda x: x) # testing the context of response

    def test_one_time_services(self):
        response = self.client.get(reverse('hotel_services:one_time_services'))
        services = Service.objects.all()
        self.assertTemplateUsed(response, template_name='hotel_services/one_time_services.html')
        self.assertQuerysetEqual(response.context['services'],  services, transform=lambda x: x) # testing the context of response

    def test_one_time_service_payment_process(self):
        self.client.login(username='testuser@gmail.com', password='testpass123')
        service = Service.objects.get(id=1)
        response = self.client.get(reverse('hotel_services:one_time_service_payment_process', args=[ int(service.id) ] ))
        self.assertTemplateUsed(response, template_name='hotel_services/one_time_service_payment_process.html')

    def test_one_time_service_payment_failed(self):
        response = self.client.get(reverse('hotel_services:one_time_service_payment_failed'))
        self.assertTemplateUsed(response, template_name='hotel_services/one_time_service_payment_failed.html')