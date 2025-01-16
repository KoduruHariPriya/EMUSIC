from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model
class CustomUser(AbstractUser):
    name = models.CharField(max_length=100)  # Store the user's name
    password = models.CharField(max_length=100)  # Store the user's password
    address = models.TextField()  # Store the user's address
    mailid = models.EmailField(max_length=100, unique=True)  # Store the user's email address
    additional_field = models.CharField(max_length=255, blank=True, null=True)
    pass
    class Meta:
        db_table = 'EMUSIC_Application_user'  # Use the existing table name

    def __str__(self):
        return self.username  # Use username as the string representation

    
# Model for storing additional data for users (e.g. registration details)
class Datas(models.Model):
    Name = models.CharField(max_length=20, default="")
    Age = models.IntegerField()
    Gender = models.CharField(max_length=20, default="")
    Address = models.CharField(max_length=20, default="")
    Contact = models.IntegerField(default="")
    Mail = models.CharField(max_length=20, default="")

    def __str__(self):
        return self.Name

# for dashboard

# Artist model for music
from django.db import models

class Artist(models.Model):
    name = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    birth_date = models.DateField()
    bio = models.TextField()

    def __str__(self):
        return self.name
# admin.py
from django.contrib import admin
from .models import Artist

# Customizing the admin for Artist model
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre', 'birth_date')  # Display these fields in the list view
    search_fields = ('name', 'genre')  # Enable search functionality for these fields
    list_filter = ('genre',)  # Allow filtering by genre

    # Optional: Add more customization such as ordering, adding extra fields, etc.
    ordering = ['name']  # Order the artists alphabetically by name by default

# Registering Artist model with the custom admin interface
admin.site.register(Artist, ArtistAdmin)

from django.db import models
from django.contrib.auth.models import User  # Importing the default User model
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default="Default description")  # Add a default value here

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default="Default description")  # Add a default value here
    def __str__(self):
        return self.name

class Plan(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=100)  # e.g., 'Monthly', 'Yearly'
    description = models.TextField()
    features = models.TextField(help_text="Features of the subscription plan", default="No features specified")  # Add default value


    def __str__(self):
        return self.name

class Track(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    category = models.CharField(max_length=255, null=True, blank=True)  # Allow null values
    file = models.FileField(upload_to='uploads/', default='uploads/default_audio.mp3')  # Provide a default file
    duration = models.DurationField()

    def __str__(self):
        return f"{self.title} by {self.artist}"
    
    
    # models.py
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings  # Add this import
from .models import Plan 

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, related_name="users", on_delete=models.SET_NULL, null=True, blank=True)
    subscription_date = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)  # Add this line to define the bio field

    def __str__(self):
        return f"Profile of {self.user.username}"
        

# models.py
from django.db import models
from django.conf import settings
from django.utils import timezone


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(default=30)  # Set a default value (e.g., 30 days)
    features = models.TextField(default="Standard features included.")  # Default feature description
    date_subscribed = models.DateTimeField(auto_now_add=True, )
    is_active = models.BooleanField(default=True)  # New field


    def __str__(self):
        return self.name
    
from django.contrib import admin
from .models import SubscriptionPlan

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active')
    list_editable = ('price', 'is_active')
    search_fields = ('name',)


class SongCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default="Default description")  # Add a default value here

    def __str__(self):
        return f'{self.user.username} - {self.plan} Plan'


# models.py
class MusicTrack(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=100)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(SongCategory, on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to='music/', null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.title} by {self.artist}"


class UserPreferences(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    subscription_plan = models.ForeignKey(SubscriptionPlan, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Preferences for {self.user.username}"

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings  # Import settings


# Model for storing songs in the database
class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    duration = models.IntegerField()  # Duration in seconds
    file = models.FileField(upload_to='songs/')

    def __str__(self):
        return f'{self.title} by {self.artist}'

from django.db import models
from django.conf import settings 
# Model for storing user requests for unavailable songs
class SongRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request by {self.user.username} for {self.song_title}"



from django.conf import settings

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message[:50]  # Show first 50 chars of the message

from django.db import models
from django.contrib.auth.models import User

class UserSubscription(models.Model):
    PLAN_CHOICES = [
        ('Basic', 'Basic'),
        ('Premium', 'Premium'),
        ('VIP', 'VIP')
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    date_subscribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan} Plan"

# models.py
from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} at {self.created_at}"
