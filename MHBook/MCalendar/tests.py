from django.test import TestCase
from django.urls import reverse
from .models import *
from django.utils import timezone, dateformat

class MyBookingsTests(TestCase):
    def setUp(self):
        # Create User
        self.user = Users.objects.create_user(
            first_name='test', 
            last_name='user', 
            email='TestUser@icloud.com', 
            password='testPass', 
        )
        # Create superuser
        self.superuser = Users.objects.create_superuser(
            first_name='super', 
            last_name='user', 
            email='AdminUser@icloud.com', 
            password='testPass', 
            telephone=''
        )
        # Create events for user
        self.event1 = Event.objects.create(
            bookingName=f'{self.user.first_name} {self.user.last_name}', 
            supervisorName='John Pork', 
            email=self.user.email, 
            bookingDate=timezone.now().date() + timezone.timedelta(days=1), 
            startTime='10:00', 
            finishTime='12:00', 
            notes='Test note', 
            equipment='Projector', 
            hourlyRate=20.00, 
        )
        self.event2 = Event.objects.create(
            bookingName=f'{self.user.first_name} {self.user.last_name}', 
            supervisorName='Kai Cenat', 
            email=self.user.email, 
            bookingDate=timezone.now().date() + timezone.timedelta(days=3), 
            startTime='14:00', 
            finishTime='17:00', 
            notes='Test note 2', 
            equipment='Cryostat', 
            hourlyRate=14.00, 
        )
        # Create event for other user
        self.event1 = Event.objects.create(
            bookingName='Fanum Tax', 
            supervisorName='Lionel Messi', 
            email='otheruser@email.com', 
            bookingDate=timezone.now().date() + timezone.timedelta(days=2), 
            startTime='10:00', 
            finishTime='15:00', 
            notes='Test note 3', 
            equipment='Haggis', 
            hourlyRate=9.00, 
        )
    
    # Tests
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('myBookings'))
        # 302 code is used when unauthenticated users try to access a page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('loginPage'))
    
    def test_regular_users_see_own_bookings(self):
        self.client.login(email='TestUser@icloud.com', password='testPass')
        response = self.client.get(reverse('myBookings'))
        # 200 code is used to check if the page was loaded correctly
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myBookings.html')
        self.assertContains(response, f'{self.user.first_name} {self.user.last_name}')
        self.assertNotContains(response, 'Fanum Tax')

    def test_superuser_sees_all_bookings(self):
        self.client.login(email='AdminUser@icloud.com', password='testPass')
        response = self.client.get(reverse('myBookings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myBookings.html')
        self.assertContains(response, f'{self.user.first_name} {self.user.last_name}')
        self.assertContains(response, 'Fanum Tax')

    def test_no_past_bookings_shown(self):
        past_booking = Event.objects.create(
            bookingName='Past Booking', 
            supervisorName='Kylian Mbappe', 
            email=self.user.email, 
            bookingDate=timezone.now().date() - timezone.timedelta(days=1), 
            startTime='10:00', 
            finishTime='15:00', 
            notes='We be yesterday', 
            equipment='Haggis', 
            hourlyRate=4.00, 
        )

        self.client.login(email='TestUser@icloud.com', password='testPass')
        response = self.client.get(reverse('myBookings'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Past Booking')
        self.assertContains(response, f'{self.user.first_name} {self.user.last_name}')

    def test_no_bookings_message_displayed(self):
        self.client.login(email='TestUser@icloud.com', password='testPass')
        Event.objects.filter(email='TestUser@icloud.com').delete()
        response = self.client.get(reverse('myBookings'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You have no current bookings.")

    def test_pagination(self):
        for i in range(13):
            Event.objects.create(
                bookingName=f'Booking No {i}', 
                supervisorName=f'Supervisor {i}', 
                email=self.user.email,
                bookingDate=timezone.now().date() + timezone.timedelta(days=i), 
                startTime='15:00', 
                finishTime='16:00', 
                notes=f'Test note {3+i}', 
                equipment='Projector', 
                hourlyRate=20.00, 
            )
        self.client.login(email='TestUser@icloud.com', password='testPass')
        response = self.client.get(reverse('myBookings'))
        # Paginator is set to 10 items per page
        self.assertEqual(len(response.context['pageObj']), 10)
        self.assertContains(response, 'Booking No 1')
        self.assertNotContains(response, 'Booking No 11')
