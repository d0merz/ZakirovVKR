from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class Guest(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    phoneNumber = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.user)

    def numOfBooking(self):
        return Booking.objects.filter(guest=self).count()

    def numOfDays(self):
        totalDay = 0
        bookings = Booking.objects.filter(guest=self)
        for b in bookings:
            day = b.endDate - b.startDate
            totalDay += int(day.days)

        return totalDay

    def numOfLastBookingDays(self):
        try:
            return int(
                (
                    Booking.objects.filter(guest=self).last().endDate
                    - Booking.objects.filter(guest=self).last().startDate
                ).days
            )
        except:
            return 0

    def currentRoom(self):
        booking = Booking.objects.filter(guest=self).last()
        return booking.roomNumber


class Event(models.Model):
    EVENT_TYPES = (
        ("Фильм", "Фильм"),
        ("Театр", "Театр"),
        ("Конференция", "Конференция"),
        ("Концерт", "Концерт"),
        ("Развлечения", "Развлечения"),
        ("Живая музыка", "Живая музыка"),
    )

    EVENT_LOCATIONS = (
        ("Кинозал", "Кинозал"),
        ("Театральный зал", "Театральный зал"),
        ("Конфернцзал", "Конфернцзал"),
        ("Концертный зал", "Концертный зал"),
        ("Лаундж-зона", "Лаундж-зона"),
    )

    eventType = models.CharField(max_length=20, choices=EVENT_TYPES)
    location = models.CharField(max_length=100, choices=EVENT_LOCATIONS)
    startDate = models.DateField()
    endDate = models.DateField()
    explanation = models.TextField()

    def __str__(self):
        return str(self.eventType)


class EventAttendees(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    numberOfDependees = models.IntegerField(default=0)
    guest = models.ForeignKey(Guest, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.event) + " " + str(self.guest)


class Employee(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    phoneNumber = models.IntegerField(unique=True)
    # phoneNumber = PhoneNumberField(unique=True)
    salary = models.FloatField()

    def __str__(self):
        return str(self.user)


class Task(models.Model):
    employee = models.ForeignKey(Employee, null=True, on_delete=models.CASCADE)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    description = models.TextField()

    def str(self):
        return str(self.employee)


class Room(models.Model):
    ROOM_TYPES = (
        ("Королевская", "Королевская"),
        ("Люкс", "Люкс"),
        ("Стандарт", "Стандарт"),
        ("Эконом", "Эконом"),
    )
    number = models.IntegerField(primary_key=True)
    capacity = models.SmallIntegerField(null=True)
    numberOfBeds = models.SmallIntegerField()
    roomType = models.CharField(max_length=20, choices=ROOM_TYPES)
    price = models.FloatField()

    image = models.ImageField("Картинка", upload_to="rooms/", blank=True)

    statusStartDate = models.DateField(null=True, blank=True)
    statusEndDate = models.DateField(null=True, blank=True)

    description = models.TextField()

    def __str__(self):
        return str(self.number)


class Booking(models.Model):
    roomNumber = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, null=True, on_delete=models.CASCADE)
    dateOfReservation = models.DateField(default=timezone.now)
    startDate = models.DateField(null=True)
    endDate = models.DateField(null=True)

    def numOfDep(self):
        return Dependees.objects.filter(booking=self).count()

    def __str__(self):
        return str(self.roomNumber) + " " + str(self.guest)


class Dependees(models.Model):
    booking = models.ForeignKey(Booking, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def str(self):
        return str(self.booking) + " " + str(self.name)


class RoomServices(models.Model):
    SERVICES_TYPES = (
        ("Еда", "Еда"),
        ("Уборка", "Уборка"),
        ("Тех.обслуживание", "Тех.обслуживание"),
    )

    curBooking = models.ForeignKey(
        Booking, null=True, on_delete=models.CASCADE
    )
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    createdDate = models.DateField(default=timezone.now)
    servicesType = models.CharField(max_length=20, choices=SERVICES_TYPES)
    price = models.FloatField()

    def str(self):
        return (
            str(self.curBooking)
            + " "
            + str(self.room)
            + " "
            + str(self.servicesType)
        )
