from django import forms
from django.forms import ModelForm
from .models import Venue, Event


# Создаем форму ADMIN Event
class EventFormAdmin(ModelForm):
    class Meta:
        model = Event
        fields = ("name", "event_date", "venue", "manager", "attendees", "description")
        labels = {
            'name': '',
            'event_date': 'YYYY-MM-DD HH:mm:ss ',
            'venue': 'Venue',# добавили данные поля потомучто поле селект не отображает что именно ты выбираешь
            'manager': 'Manager',
            'attendees': 'Attendees',
            'description': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event name'}),
            'event_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event date'}),
            'venue': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Venue'}),
            'manager': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Manager'}),
            'attendees': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'attendees'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'description'}),
        }


# Создаем форму USER Event
class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ("name", "event_date", "venue", "attendees", "description")
        labels = {
            'name': '',
            'event_date': 'YYYY-MM-DD HH:mm:ss ',
            'venue': 'Venue',# добавили данные поля потомучто поле селект не отображает что именно ты выбираешь
            'attendees': 'Attendees',
            'description': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event name'}),
            'event_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event date'}),
            'venue': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Venue'}),
            'attendees': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'attendees'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'description'}),
        }

# Создаем форму Venue
class VenueForm(ModelForm):
    class Meta:
        model = Venue
        # fields = "__all__"
        fields = ("name", "address", "zip_code", "phone", "web", "email_address", "venue_image")
        # можно через лейбл(заголовки) сделать, но мы делаем через надписи в инпутах
        # labels = {
        #     'name': 'Enter your Venue name',
        #     'address': 'Enter address',
        #     'zip_code': '',
        #     'phone': '',
        #     'web': '',
        #     'email_address': '',
        # }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Venue name'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'address'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'zip_code'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your phone'}),
            'web': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Website'}),
            'email_address': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email_address'}),
        }