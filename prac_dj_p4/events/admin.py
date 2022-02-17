from django.contrib import admin
from events.models import Venue, MyClubUser, Event
from django.contrib.auth.models import Group


# Register your models here.
# admin.site.register(Venue)
admin.site.register(MyClubUser)
# admin.site.register(Event)

# https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#django.contrib.admin.AdminSite.unregister
# https://github.com/django/django/blob/main/django/contrib/auth/models.py
# https://docs.djangoproject.com/en/4.0/topics/auth/default/#groups
# Удаление группы
admin.site.unregister(Group)# сделали потомучто можем

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'phone']
    ordering = ('name',)
    search_fields = ('name', 'address')
    #django.contrib.admin.ModelAdmin.prepopulated_fields
    # не перепутать с **eld , который автоматом не заполняет при заполнении указанного поля title
    # prepopulated_fields = {"slug": ("title",)}

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (('name', 'venue'), 'event_date', 'description', 'manager', 'approved')
    list_display = ('name', 'event_date', 'venue')
    # https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter
    list_filter = ('event_date', 'venue')
    # https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.ordering
    ordering = ('-event_date',)