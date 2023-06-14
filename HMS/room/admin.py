from django.contrib import admin
from hotel.models import *

# Register your models here.
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Dependees)
admin.site.register(RoomServices)

