# CS3028-GroupAssignment-Kilo
Group Kilo - Software Engineering Assignment: Microscopy and Histology Management System

# Running the application and tests

In order to run the calendar, make sure you are in the MHBook directory first.

In terminal: py manage.py runserver
In your browser: http://127.0.0.1:8000/MCalendar/login/

In order to run tests, once again make sure you are in the MHBook directory

To run all tests; in terminal: py manage.py test
To run a specific class; in terminal: py manage.py test MCalendar.tests.x - where x is the class name (e.g. CreateBillingTests)

# Models.py overview

The *CustomUserManager* model's sole purpose is to be able to access the default django databases as regular users are unable to enter it.
An example of this would be our login function. The user manager would check for example in the django databases if the user is already logged in, authenticated, etc.

The *Users* model is used to create both regular users of our app and the superusers. It also holds accounts that are pending to be accepted.
These users are identified by their unique *email* field.

The *Supervisor* model holds all created and active supervisors that can later be associated with bookings.
Just like *Users*, it is identified by its *email* field.

The *CancelledBooking* model holds all same day cancellations. This model will be frequently used and wiped by the superusers.

The *Event* model holds all bookings made by both users and superusers. This model can be both associated by the *email* field, which will be the field linked with the user who created it, or by its *id*.
This model also holds the function to calculate the total time of each booking.

The *Equipment* model is used to create new equipment and holds their hourly rates.

The *Billing* model is used for creating invoices for the supervisors. It is linked with the majority of the other models through its many to many fields.

# Templates overview

The templates *archive*, *billings*, *CalendarPageAdmin*, *createBilling* and *requests* are only accessible by superuser accounts. Superusers can also view all the other templates which are accessible for users.

The difference between *CalendarPage* and *CalendarPageAdmin* is the ability to create equipment, supervisors and create bookings for other users. Superusers are also able to see all bookings created by users whereas *CalendarPage* only displays the bookings associated with the logged in user.

The sidebar is present in the majority of templates other than *404*, *login* and *register*. It is used to navigate between all pages.
Its content changes depending on whether a regular user is logged in or a superuser.

# Urls and Views

The file *urls.py* holds all the links to all templates aswell as their functionalities. For example, canceling a booking in the *editBooking* template, has its own link.

The file *views.py* holds the majority of the application backend and functionality other than a few functions written in javascript in the templates. This is where the models are manipulated and data is altered. All templates and models are accessed and linked through *views*.