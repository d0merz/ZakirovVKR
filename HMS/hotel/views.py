import pickle
import random
from datetime import date, datetime, timedelta
import datetime
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django.core.mail import send_mail
from django.db.models import Count, Q
from django.shortcuts import redirect, render
import pandas as pd
from hotel.models import *
from django.http import HttpResponse, JsonResponse
from .forms import *
from sklearn.ensemble import RandomForestRegressor
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .simulation import maid_simulation, profit_simulation



@login_required(login_url="login")
def home(request):
    role = str(request.user.groups.all()[0])
    if role == "guest":
        return redirect("guest-profile", pk=request.user.id)
    else:
        return redirect("employee-profile", pk=request.user.id)


@login_required(login_url="login")
def events(request):
    role = str(request.user.groups.all()[0])
    path = role + "/"

    events = Event.objects.all()

    # eventAttendees = EventAttendees.objects.filter(guest = request.user.guest, event = )

    attendedEvents = None
    if role == "guest":
        attendedEvents = EventAttendees.objects.filter(
            guest=request.user.guest
        )

    if request.method == "POST":
        if "filter" in request.POST:
            if request.POST.get("type") != "":
                events = events.filter(
                    eventType__contains=request.POST.get("type")
                )

            if request.POST.get("name") != "":
                events = events.filter(
                    location__contains=request.POST.get("location")
                )

            if request.POST.get("fd") != "":
                events = events.filter(startDate__gte=request.POST.get("fd"))

            if request.POST.get("ed") != "":
                events = events.filter(endDate__lte=request.POST.get("ed"))

            context = {
                "role": role,
                "events": events,
                "type": request.POST.get("type"),
                "location": request.POST.get("location"),
                "fd": request.POST.get("fd"),
                "ed": request.POST.get("ed"),
            }
            return render(request, path + "events.html", context)

        if "Save" in request.POST:
            n = request.POST.get("id-text")
            temp = EventAttendees.objects.get(id=request.POST.get("id-2"))
            temp.numberOfDependees = n
            temp.save()

        if "attend" in request.POST:
            attendedEvents = EventAttendees.objects.filter(
                guest=request.user.guest
            )
            tempEvent = events.get(id=request.POST.get("id"))
            # print("query set**", attendedEvents)
            # print("**object***", tempEvent)
            # print(tempEvent in attendedEvents)
            check = False
            for t in attendedEvents:
                if t.event.id == tempEvent.id:
                    check = True
                    break
            if not check:
                a = EventAttendees(event=tempEvent, guest=request.user.guest)
                a.save()
                return redirect("events")

        elif "remove" in request.POST:
            tempEvent = events.get(id=request.POST.get("id"))
            EventAttendees.objects.filter(
                event=tempEvent, guest=request.user.guest
            ).delete()
            return redirect("events")  # refresh page

    context = {
        "role": role,
        "events": events,
        "attendedEvents": attendedEvents,
        "type": request.POST.get("type"),
        "location": request.POST.get("location"),
        "fd": request.POST.get("fd"),
        "ed": request.POST.get("ed"),
    }
    return render(request, path + "events.html", context)


@login_required(login_url="login")
def createEvent(request):
    role = str(request.user.groups.all()[0])
    path = role + "/"

    form = createEventForm()
    if request.method == "POST":
        form = createEventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("events")

    context = {"form": form, "role": role}
    return render(request, path + "createEvent.html", context)


@login_required(login_url="login")
def deleteEvent(request, pk):
    role = str(request.user.groups.all()[0])
    path = role + "/"

    event = Event.objects.get(id=pk)
    if request.method == "POST":
        event.delete()
        return redirect("events")

    context = {"role": role, "event": event}
    return render(request, path + "deleteEvent.html", context)


@login_required(login_url="login")
def event_profile(request, id):
    role = str(request.user.groups.all()[0])
    path = role + "/"

    tempEvent = Event.objects.get(id=id)
    attendees = EventAttendees.objects.filter(event=tempEvent)

    context = {"role": role, "attendees": attendees, "event": tempEvent}
    return render(request, path + "event-profile.html", context)


@login_required(login_url="login")
def event_edit(request, pk):
    role = str(request.user.groups.all()[0])
    path = role + "/"

    event = Event.objects.get(id=pk)
    form = editEvent(instance=event)

    context = {
        "role": role,
        "event": event,
        "form": form,
    }

    if request.method == "POST":
        form = editEvent(request.POST, instance=event)
        if form.is_valid:
            form.save()
            return redirect("events")

    return render(request, path + "event-edit.html", context)


@login_required(login_url="login")
def error(request):
    role = str(request.user.groups.all()[0])
    path = role + "/"

    context = {"role": role}
    return render(request, path + "error.html", context)


@login_required(login_url="login")
def payment(request):
    role = str(request.user.groups.all()[0])
    path = role

    import random
    import string

    code = "".join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase)
        for _ in range(10)
    )

    context = {"role": role, "code": code}

    def send(request, receiver, code):
        subject = "Подтверждение оплаты"
        text = """
            Уважаемый {guestName},
            Пожалуйста, скопируйте и вставьте этот код в форму проверки:

            {code}

            Пожалуйста, проигнорируйте это письмо, если вы не совершали эту транзакцию!
        """

        email_text = text.format(
            guestName=receiver.user.first_name + " " + receiver.user.last_name,
            code=code,
        )

        message_email = "hms@support.com"
        message = email_text
        receiver_name = (
            receiver.user.first_name + " " + receiver.user.last_name
        )

        send_mail(
            receiver_name + " " + subject,
            message,
            message_email,
            [receiver.user.email],
            fail_silently=False,
        )

        messages.success(request, "Verification email Was Successfully Sent")

        return render(request, path + "/verify.html", context)

    if role == "guest":
        send(request, request.user.guest, code)
    elif role == "receptionist":
        send(request, Booking.objects.all().last().guest, code)

    return render(request, path + "/payment.html", context)


@login_required(login_url="login")
def verify(request):
    role = str(request.user.groups.all()[0])
    path = role + "/"
    if request.method == "POST":
        tempCode = request.POST.get("tempCode")
        if "verify" in request.POST:
            realCode = request.POST.get("realCode")

            if realCode == tempCode:
                messages.success(request, "Successful Booking")
            else:
                Booking.objects.all().last().delete()
                messages.warning(request, "Invalid Code")

            return redirect("rooms")
    context = {"role": role, "code": tempCode}
    return render(request, path + "verify.html", context)


@login_required(login_url="login")
def stats_page(request):
    role = str(request.user.groups.all()[0])
    path = role + "/"
    tempCode = request.POST.get("tempCode")
    context = {"role": role, "code": tempCode}
    return render(request, path + "statistics.html", context)


def predict(request):
    with open('./ml/model.pkl', 'rb') as file:
        model = pickle.load(file)
    
    if request.method == 'POST':
        date_str = request.POST.get('date')
        date = date_str.split('-')
        df = pd.DataFrame([date], columns=['year', 'month', 'day'])
        prediction = model.predict(df) 
        print(prediction)
        return JsonResponse({'prediction': round(prediction[0], 2)})
      

class MaidSimulationView(APIView):
    def post(self, request, format=None):
        num_rooms = int(request.data.get('num_rooms'))
        num_maids = int(request.data.get('num_maids'))
        arrival_interval = float(request.data.get('arrival_interval'))
        cleaning_time = float(request.data.get('cleaning_time'))
        cleaning_schedule = maid_simulation(num_rooms, num_maids, arrival_interval, cleaning_time)
        return JsonResponse({'cleaning_schedule': cleaning_schedule})
    

class ProfitSimulationView(APIView):
    def post(self, request):
        num_rooms = int(request.data.get('num_rooms'))
        price_per_room = float(request.data.get('price_per_room'))
        cost_per_room = float(request.data.get('cost_per_room'))
        maid_wage = float(request.data.get('maid_wage'))
        num_maids = int(request.data.get('num_maids'))
        arrival_interval = float(request.data.get('arrival_interval'))
        stay_duration = float(request.data.get('stay_duration'))

        formatted_profit = profit_simulation(num_rooms, price_per_room, cost_per_room, maid_wage, num_maids, arrival_interval, stay_duration)
        return Response({'formatted_profit': formatted_profit})









