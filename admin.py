from django.contrib import admin
from .models import CustomUser, Datas, Track, Category, Genre, Plan, UserProfile, SubscriptionPlan, SongCategory, Notification
from django.contrib.admin.sites import AlreadyRegistered

# Register the models with error checking to prevent "AlreadyRegistered" errors
try:
    admin.site.register(CustomUser)
except AlreadyRegistered:
    pass  # If already registered, don't do anything

try:
    admin.site.register(Datas)
except AlreadyRegistered:
    pass  # If already registered, don't do anything

try:
    admin.site.register(Track)
except AlreadyRegistered:
    pass  # If already registered, don't do anything

admin.site.register(Category)
admin.site.register(Plan)
admin.site.register(UserProfile)

# Registering the other models (SubscriptionPlan, SongCategory, MusicTrack)
try:
    admin.site.register(SubscriptionPlan)
except AlreadyRegistered:
    pass  # If already registered, don't do anything

admin.site.register(SongCategory)
admin.site.register(Genre)
admin.site.register(Notification)

# If the Artist model is not registered yet, register it
from .models import Artist
try:
    admin.site.register(Artist)
except AlreadyRegistered:
    pass  # If already registered, don't do anything


# admin.py
from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'message')
    search_fields = ('name', 'email')
    list_filter = ('created_at',)
    readonly_fields = ('name', 'email', 'message', 'created_at')
