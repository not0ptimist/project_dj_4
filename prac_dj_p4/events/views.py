from django.shortcuts import redirect, render
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from .models import Event, Venue
from .forms import VenueForm, EventForm, EventFormAdmin
from django.http import HttpResponse, FileResponse
import csv
# import PDF stuff
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
# import pagination stuff
from django.core.paginator import Paginator
from django.contrib import messages
# импорт модели юзера из джанго
from django.contrib.auth.models import User
# для методово, когда нужно "ИЛИ"
from django.db.models import Q


# Список
def show_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    return render(request, 'events/show_event.html', {
        'event': event,
    })

# Список events по выбранному venue
def venue_event(request, venue_id):
    # Grab the venue
    venue = Venue.objects.get(id=venue_id)
    # Grab the events from that venue
    events = venue.event_set.all()
    if events:
        return render(request, 'events/venue_event.html', {
            'events': events
            })
    else:
        messages.success(request, "No events were found")
        return redirect('list-events')

# Admin Page
def admin_approval(request):
    # Get The Venues 
    venue_list = Venue.objects.all()# не лучший способ, так же можно явно заметить что ниже мы опять это же пишем
    # подсчет event, venue, user
    event_count = Event.objects.all().count()
    venue_count = Venue.objects.all().count()
    user_count = User.objects.all().count()
    event_list = Event.objects.all().order_by('-event_date')
    if request.user.is_superuser:
        if request.method == 'POST':
            id_list = request.POST.getlist('boxes')# имя нашей галки, нашего checkbox
            # unchecked all events. Это не лучший вариант сбрасывать галки перед записью
            event_list.update(approved=False)
            print(event_list)
            # Update the datebase
            for x in id_list:
                Event.objects.filter(pk=int(x)).update(approved=True)
            # отправляем сообщение об удачном обновлении списка
            messages.success(request, "Event list approval")
            return redirect('list-events')
        else:
            return render(request, 'events/admin_approval.html', 
                {'event_list': event_list, 
                'event_count': event_count,
                'venue_count': venue_count,
                'user_count': user_count,
                'venue_list': venue_list,
                })
    else:
        messages.success(request, "You aren't autorized to view this page")
        return redirect('home')


# search_events,
def search_events(request):
    if request.method == "POST":
        searched = request.POST['searched']
        # https://docs.djangoproject.com/en/4.0/ref/models/querysets/#field-lookups
        # https://docs.djangoproject.com/en/4.0/topics/db/queries/#complex-lookups-with-q-objects
        events = Event.objects.filter(Q(name__contains=searched)|Q(description__contains=searched))# использование ИЛИ
        return render(request, 'events/search_events.html', 
            {'searched': searched, 
            'events': events})
    else:
        return render(request, 'events/search_events.html', {})


# my_events, показ списка owner
def my_events(request):
    if request.user.is_authenticated:
        me = request.user.id# id  потомучто мы сравниваем с owner, который цифра
        events = Event.objects.filter(attendees=me).order_by('-event_date')
        return render(request, 'events/my_event_list.html', {
            'events': events
        })
    else:
        messages.success(request, "You aren't autorized to look this event")
        return redirect('list-events')

# для данной функции нам нужно поставить reportlab, через pip, подключаем FileResponse
def venue_pdf(request):
    # создание Bytesteam buffer
    buf = io.BytesIO()
    # Создание Canvas
    # https://www.reportlab.com/docs/reportlab-userguide.pdf
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # Создание текстового объекта
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)
    # Добавление диний в текст
    # lines = [
    #     "this is line 1"
    # ]
    lines = []
    venues = Venue.objects.all()
    for venue in venues:
        # \n добавляет в файал pdf черные квадратики
        # lines.append(f'{venue.name}\n{venue.address}\n{venue.zip_code}\n{venue.phone}\n{venue.web}\n{venue.email_address}\n\n')
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append("")
    for line in lines:
        textob.textLine(line)
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='venue.pdf')

# генератор csv файла
def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    # https://docs.djangoproject.com/en/4.0/ref/request-response/#telling-the-browser-to-treat-the-response-as-a-file-attachment
    response['Content-Disposition'] = 'attachment; filename=venue.csv'
    # создаем csv файл
    writer = csv.writer(response)
    venues = Venue.objects.all()
    # добавляем шапку в файл
    writer.writerow(['Venue name', 'Address', 'Zip code', 'phone', 'website', 'email'])
    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.zip_code, venue.phone, venue.web, venue.email_address])
    return response

# Генератор текстового файла Venue List
def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    # https://docs.djangoproject.com/en/4.0/ref/request-response/#telling-the-browser-to-treat-the-response-as-a-file-attachment
    response['Content-Disposition'] = 'attachment; filename=venue.txt'
    venues = Venue.objects.all()
    # Создаем пустой список
    lines = []
    for venue in venues:
        lines.append(f'{venue.name}\n{venue.address}\n{venue.zip_code}\n{venue.phone}\n{venue.web}\n{venue.email_address}\n\n')
    # Пишем текстовый файл
    response.writelines(lines)
    return response

# Create your views here.
def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list-venues')

def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user == event.manager:
        event.delete()
        messages.success(request, "Event deleted successfully")
        return redirect('list-events')
    else:
        messages.success(request, "You aren't autorized to delete this event")
        return redirect('list-events')

def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_superuser:# Добавление возможности изменить менеджера, но только superuser
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
        form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list-events')
    return render(request, 'events/update_event.html',
    {'event': event, 
    'form': form})

def add_event(request):
    submitted = False
    if request.method == 'POST':
        if request.user.is_superuser:#  проверка на суперюзера, и выбор формы
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_event?submitted=True')
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user
                event.save()
                return HttpResponseRedirect('/add_event?submitted=True')
    else:
        # Just going th the page, not submitting
        if request.user.is_superuser:
            form = EventFormAdmin
        else:
            form = EventForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_event.html', {'form': form, 'submitted': submitted})

def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, request.FILES or None, instance=venue)# request.FILES добавили для возможности смены картинки
    if form.is_valid():
        form.save()
        return redirect('list-venues')
    return render(request, 'events/update_venue.html',
    {'venue': venue, 
    'form': form})

def search_venues(request):
    if request.method == "POST":
        # Другой способ через GET() ?
        searched = request.POST['searched']
        # https://docs.djangoproject.com/en/4.0/ref/models/querysets/#field-lookups
        venues = Venue.objects.filter(name__contains=searched)
        return render(request, 'events/search_venues.html', 
            {'searched': searched, 
            'venues': venues})
    else:
        return render(request, 'events/search_venues.html', {})

def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue_owner = User.objects.get(pk=venue.owner)
    return render(request, 'events/show_venue.html',
    {'venue': venue,
    'venue_owner': venue_owner
    })

def list_venues(request):
    venue_list = Venue.objects.all()#.order_by('name')# ? это значение рандомайзера
    # ставим/пишим пагинацию
    p = Paginator(Venue.objects.all(), 2)
    page = request.GET.get('page')
    venues = p.get_page(page)
    # указание страницы пагинации
    nums = 'a' * venues.paginator.num_pages
    return render(request, 'events/venue.html',
        {'venue_list': venue_list,
        'venues': venues,
        'nums': nums}
        )

def add_venue(request):
    submitted = False
    if request.method == 'POST':
        # https://docs.djangoproject.com/en/4.0/ref/forms/api/#binding-uploaded-files-to-a-form
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            # добавляем owner(логин юзер) для занесением автоматом при создании
            venue = form.save(commit=False)# сохраним, но не сейчас
            venue.owner = request.user.id# в поле owner записываем нынешнего юзера
            venue.save()
            # form.save() # закомментировали когда owner добавили
            # https://docs.djangoproject.com/en/4.0/topics/forms/#get-and-post
            # https://docs.djangoproject.com/en/4.0/topics/http/urls/#using-regular-expressions
            # https://docs.djangoproject.com/en/4.0/topics/forms/
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_venue.html', {
        'form': form, 
        'submitted': submitted
        })

def all_events(request):
    event_list = Event.objects.all().order_by('name')
    return render(request, 'events/events_list.html',
        {'event_list': event_list})

def home(request):
    now = datetime.now()
    month_number = now.month
    month = now.strftime('%B')
    current_year = now.year
    # создадим календарь
    cal = HTMLCalendar().formatmonth(
        current_year,
        month_number
        )
    event_list = Event.objects.filter(
        event_date__year=current_year, 
        event_date__month=month_number
        )

    return render(request,
        'events/home.html', {
        "month_number": month_number,
        'month': month,
        "cal": cal,
        "current_year": current_year,
        'event_list': event_list,
        })

def page_calendar(request, year, month):# можно задать год и месяц по умолчанию, если календарьотображался на первой странице("")
    # конвертируем строку месяца в число
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # создадим календарь
    cal = HTMLCalendar().formatmonth(
        year,
        month_number)
    
    # делаем нынешний год
    now = datetime.now()
    current_year = now.year

    # делаем нынешнее время
    time = now.strftime('%I:%M:%S %p')

    return render(request,
        'events/calendar.html', {
        "year": year,
        "month": month,
        "month_number": month_number,
        "cal": cal,
        "current_year": current_year,
        "time": time,
        })