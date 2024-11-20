from django.test import TestCase
from django.urls import reverse
from .models import *
from django.utils import timezone, dateformat
from django.core.paginator import Paginator

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
        response = self.client.get(reverse('myBookings'), {'page': 1})
        self.assertEqual(response.status_code, 200)
        # Paginator is set to 10 items per page
        self.assertEqual(len(response.context['pageObj']), 10)
        self.assertContains(response, 'Booking No 1')
        self.assertNotContains(response, 'Booking No 11')

        events = Event.objects.all()
        paginator = Paginator(events, 10)
        self.assertEqual(len(response.context['pageObj']), len(paginator.page(1)))

class EditBookingTests(TestCase):
    def setUp(self):
        # Create User
        self.user = Users.objects.create_user(
            first_name='test', 
            last_name='user', 
            email='TestUser@icloud.com', 
            password='testPass', 
        )
        # Create supervisor
        self.supervisor = Supervisor.objects.create(
            first_name='Jane', 
            last_name='Doe', 
            email='JaneDoe@gmail.com', 
        )
        # Create equipment
        self.equipment = Equipment.objects.create(
            equipmentName='Projector', 
            hourlyRate=10.00, 
        )
        # Create event
        self.event1 = Event.objects.create(
            bookingName=f'{self.user.first_name} {self.user.last_name}', 
            supervisorName=f'{self.supervisor.first_name} {self.supervisor.last_name}', 
            email=self.user.email, 
            bookingDate=timezone.now().date() + timezone.timedelta(days=1), 
            startTime='10:00', 
            finishTime='12:00', 
            notes='Test note', 
            equipment=self.equipment.equipmentName, 
            hourlyRate=self.equipment.hourlyRate, 
        )

        self.url = reverse('editBooking', kwargs={'id': self.event1.id})
        self.cancelurl = reverse('cancelBooking', kwargs={'id': self.event1.id})

    # Tests
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('loginPage'))
    
    def test_edit_booking_loads(self):
        self.client.login(email='TestUser@icloud.com', password='testPass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'editBooking.html')
        self.assertIn('Edit Booking', response.content.decode())
    
    def test_edit_booking_update(self):
        self.client.login(email='TestUser@icloud.com', password='testPass')
        update = {
            'supervisorName': self.supervisor.id, 
            'bookingDate': timezone.now().date() + timezone.timedelta(days=2), # Changed
            'startTime': '10:00',
            'finishTime': '13:00', # Changed
            'notes': 'Test note',
            'equipment': self.equipment.equipmentName, 
        }
        self.client.post(self.url, update)
        self.event1.refresh_from_db()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.event1.bookingDate, timezone.now().date() + timezone.timedelta(days=2))
        self.assertEqual(self.event1.finishTime.strftime('%H:%M'), '13:00')
        self.assertEqual(self.event1.equipment, self.equipment.equipmentName) # Makes sure other fields remain the same
    
    def test_booking_overlap_error(self):
        self.client.login(email='TestUser@icloud.com', password='testPass')
        Event.objects.create(
            bookingName=f'John Pork', 
            supervisorName=f'{self.supervisor.first_name} {self.supervisor.last_name}', 
            email='JohnPork@gmail.com', 
            bookingDate=timezone.now().date() + timezone.timedelta(days=2), 
            startTime='14:00', 
            finishTime='15:00', 
            notes='Test note', 
            equipment=self.equipment.equipmentName, 
            hourlyRate=self.equipment.hourlyRate, 
        )
        update = {
            'supervisorName': self.supervisor.id, 
            'bookingDate': timezone.now().date() + timezone.timedelta(days=2),
            'startTime': '10:00',
            'finishTime': '15:00', # Changed
            'notes': 'Test note',
            'equipment': self.equipment.equipmentName, 
        }
        response = self.client.post(self.url, update)
        self.assertEqual(response.status_code, 200)
        self.assertIn('This time slot is already booked for this equipment.', response.content.decode())

    def test_cancel_bookings(self):
        self.client.login(email='TestUser@icloud.com', password='testPass')
        response = self.client.get(self.cancelurl)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('myBookings'))
        with self.assertRaises(Event.DoesNotExist):
            Event.objects.get(id=self.event1.id)

class RequestsTests(TestCase):
    def setUp(self):
        # Create User
        self.user = Users.objects.create_user(
            first_name='test', 
            last_name='user', 
            email='TestUser@icloud.com', 
            password='testPass', 
            verified=True, 
        )
        # Create superuser
        self.superuser = Users.objects.create_superuser(
            first_name='super', 
            last_name='user', 
            email='AdminUser@icloud.com', 
            password='testPass', 
            telephone=''
        )
        # Create unverified accounts
        self.not1 = Users.objects.create_user(
            first_name='not1', 
            last_name='user', 
            email='Not1User@icloud.com', 
            password='testPass', 
            verified=False, 
        )
        self.not2 = Users.objects.create_user(
            first_name='not2', 
            last_name='user', 
            email='Not2User@icloud.com', 
            password='testPass', 
            verified=False, 
        )
        # Tests
    def test_redirect_if_not_superuser(self):
        self.client.login(email='TestUser@icloud.com', password='testPass')
        response = self.client.get(reverse('requests'))
        self.assertEqual(response.status_code, 302)

        self.assertRedirects(response, reverse('loginPage'))
    
    def test_access_if_superuser(self):
        self.client.login(email='AdminUser@icloud.com', password='testPass')
        response = self.client.get(reverse('requests'))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'requests.html')
        self.assertIn('Requests', response.content.decode())

    def test_pending_requests_show(self):
        self.client.login(email='AdminUser@icloud.com', password='testPass')
        response = self.client.get(reverse('requests'))
        self.assertEqual(response.status_code, 200)

        self.assertIn(f'{self.not1.first_name} {self.not1.last_name}', response.content.decode())
        self.assertIn(f'{self.not2.first_name} {self.not2.last_name}', response.content.decode())
        self.assertNotIn(f'{self.user.first_name} {self.user.last_name}', response.content.decode()) # Checks verified user isn't here

    def test_pagination(self):
        for i in range(15):
            self.user = Users.objects.create_user(
                first_name=f'test{i}', 
                last_name=f'user{i}', 
                email=f'Test{i}User@icloud.com', 
                password='testPass', 
                verified=False, 
            )
        self.client.login(email='AdminUser@icloud.com', password='testPass')
        response = self.client.get(reverse('requests'), {'page': 1})
        self.assertEqual(response.status_code, 200)

        # Paginator is set to 12 items per page
        users = Users.objects.filter(verified=False)
        paginator = Paginator(users, 12)
        self.assertEqual(len(response.context['pageObj']), len(paginator.page(1)))

    def test_accept_request(self):
        self.client.login(email='AdminUser@icloud.com', password='testPass')
        accept_url = reverse('confirmAccept', kwargs={'id': self.not1.id})

        response = self.client.get(accept_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('requests'))

        self.not1.refresh_from_db()
        self.assertTrue(self.not1.verified)
    
    def test_reject_requests(self):
        self.client.login(email='AdminUser@icloud.com', password='testPass')
        reject_url = reverse('confirmReject', kwargs={'id': self.not2.id})

        response = self.client.get(reject_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('requests'))

        with self.assertRaises(Users.DoesNotExist):
            Users.objects.get(id=self.not2.id)

    def test_no_requests_message(self):
        Users.objects.all().delete()
        Users.objects.create_superuser(
            first_name='super', 
            last_name='user', 
            email='AdminUser@icloud.com', 
            password='testPass', 
            verified=True, 
        )
        self.client.login(email='AdminUser@icloud.com', password='testPass')
        
        response = self.client.get(reverse('requests'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You have no current account requests.")

class billingsTests(TestCase):
    def setUp(self):
        # Create User
        self.user = Users.objects.create_user(
            first_name='test', 
            last_name='user', 
            email='TestUser@icloud.com', 
            password='testPass', 
            verified=True, 
        )
        # Create superuser
        self.superuser = Users.objects.create_superuser(
            first_name='super', 
            last_name='user', 
            email='AdminUser@icloud.com', 
            password='testPass', 
            telephone=''
        )
        # Create equipment
        self.equipment = Equipment.objects.create(
            equipmentName='Projector', 
            hourlyRate=10.00, 
        )
        # Create events
        self.event1 = Event.objects.create(
            invoiceRef='10A', 
            bookingName=f'{self.user.first_name} {self.user.last_name}', 
            supervisorName='John Pork', 
            email=self.user.email, 
            bookingDate=timezone.now().date() + timezone.timedelta(days=1), 
            startTime='10:00', 
            finishTime='12:00', 
            totalTime=2.0, 
            notes='Test note', 
            equipment=self.equipment.equipmentName, 
            hourlyRate=self.equipment.hourlyRate, 
        )
        self.event2 = Event.objects.create(
            invoiceRef='10A', 
            bookingName=f'{self.user.first_name} {self.user.last_name}', 
            supervisorName='John Pork', 
            email=self.user.email, 
            bookingDate=timezone.now().date() + timezone.timedelta(days=1), 
            startTime='10:00', 
            finishTime='13:00', 
            totalTime=3.0, 
            notes='Test note', 
            equipment=self.equipment.equipmentName, 
            hourlyRate=self.equipment.hourlyRate, 
        )
        # Create billing
        self.billing = Billing.objects.create(
            invoiceRef='10A', 
            supervisor='John Pork', 
            issueDate=timezone.now().date(), 
            startDate=(timezone.now() - relativedelta(months=3)).date(), 
            finishDate=timezone.now().date(), 
            totalCost=50.00, 
        )
        self.billing.events.add(self.event1)
        self.billing.events.add(self.event2)
        self.billing.equipment.add(self.equipment)
    
    # Tests
    def test_redirect_if_not_superuser(self):
        self.client.login(email='TestUser@icloud.com', password='testPass')
        response = self.client.get(reverse('billings'))
        self.assertEqual(response.status_code, 302)

        self.assertRedirects(response, reverse('loginPage'))
    
    def test_access_if_superuser(self):
        self.client.login(email='AdminUser@icloud.com', password='testPass')
        response = self.client.get(reverse('billings'))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'billings.html')
        self.assertIn('Billing', response.content.decode())

    def test_delete_billing(self):
        self.client.login(email='AdminUser@icloud.com', password='testPass')
        response = self.client.get(reverse('deleteBilling', args=[self.billing.id]))
        self.assertEqual(response.status_code, 302)

        self.assertFalse(Billing.objects.filter(id=self.billing.id).exists())
        self.assertEqual(Event.objects.get(id=self.event1.id).invoiceRef, 'None')
        self.assertEqual(Event.objects.get(id=self.event2.id).invoiceRef, 'None')

    def test_delete_some_event(self):
        self.client.login(email='AdminUser@icloud.com', password='testPass')
        response = self.client.post(reverse('deleteEvent'), data={'selected_events': [self.event1.id]})
        self.assertEqual(response.status_code, 302)

        updated_event = Event.objects.get(id=self.event1.id)
        self.assertEqual(updated_event.invoiceRef, 'None')

        updated_billing = Billing.objects.get(id=self.billing.id)
        self.assertEqual(updated_billing.totalCost, 30.0)

    def test_delete_all_event(self):
        self.client.login(email='AdminUser@icloud.com', password='testPass')
        response = self.client.post(reverse('deleteEvent'), data={'selected_events': [self.event1.id]})
        response = self.client.post(reverse('deleteEvent'), data={'selected_events': [self.event2.id]})
        self.assertEqual(response.status_code, 302)

        updated_event = Event.objects.get(id=self.event1.id)
        self.assertEqual(updated_event.invoiceRef, 'None')
        updated_event = Event.objects.get(id=self.event2.id)
        self.assertEqual(updated_event.invoiceRef, 'None')

        # Since no events billing should be deleted too
        self.assertFalse(Billing.objects.filter(id=self.billing.id).exists())        
