# views.py
from email.mime import base
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.urls import reverse
import requests
from .forms import CustomUserCreationForm, ProfileUpdateForm, NotificationPreferencesForm, UserChangeForm
from .models import Datas, UserPreferences, SubscriptionPlan
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseRedirect, JsonResponse
from .models import UserProfile
from django.contrib.auth.models import User
from .models import MusicTrack, SongCategory, Genre
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Song, SongRequest
from .forms import SongRequestForm
from django.http import JsonResponse

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import UserProfile
from django.http import HttpResponse
from .forms import LoginForm,SignupForm
from django.contrib import messages



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home after successful login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

from django.views.decorators.cache import never_cache
from django.shortcuts import render

@never_cache
def home_view(request):
    print("User in context:", request.user)  # Should show AnonymousUser after logout
    return render(request, 'home.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import ProfileForm  # Assuming you have a ProfileForm to handle user data
from django.contrib import messages

@login_required
def profile_view(request):
    user = request.user  # Get the logged-in user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page
    else:
        form = ProfileForm(instance=user)  # Pass the user instance for the form

    return render(request, 'my_profile.html', {'form': form})

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    print("Before logout - User:", request.user)  # Should show the authenticated user
    logout(request)
    request.session.flush()  # Ensure session data is cleared
    print("After logout - User:", request.user)  # Should show AnonymousUser
    return redirect('home')
    
from django.shortcuts import render, redirect
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required

@login_required
def update_profile(request):
    # Get current user
    user = request.user

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()  # Save the form with new profile data

            # Once saved, render the profile page with updated details
            return render(request, 'my_profile.html', {'user': user, 'form': form})
    
    else:
        form = ProfileForm(instance=user)

    return render(request, 'my_profile.html', {'user': user, 'form': form})




# Signup page view

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user to the database
            login(request, user)  # Log the user in automatically
            messages.success(request, 'Signup successful! You are now logged in.')
            return redirect('home')  # Redirect to the home page or any other page
        else:
            print(form.errors)  # Debugging: Print errors to the console
            messages.error(request, 'There was an error in your form. Please try again.')
    else:
        form = SignupForm()
    
    return render(request, 'signup.html', {'form': form})


# Images page view
def images(request):
    return render(request, 'images.html')  # This renders the images page

# Registration page view (For handling user data and saving it to the database)
def registration(request):
    # Fetch all data for "View Details"
    all_data = None # Initialize a variable to store data after registration
    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        mail = request.POST.get('mail')
        # Validate if age is provided and is a valid integer
        if not age:
            messages.error(request, "Age is required")
            return render(request, 'home.html', {'datas': all_data})  # Return with error message
        
        try:
            # Convert age to integer, if it is not a valid integer, show error
            age = int(age)
        except ValueError:
            messages.error(request, "Age must be a number")
            return render(request, 'home.html', {'datas': all_data})  # Return with error message and existing data
        
        obj = Datas()  
        obj.Name = name
        obj.Age = age
        obj.Gender = gender
        obj.Address = address
        obj.Contact = contact
        obj.Mail = mail
        obj.save()
        
        # After saving, use redirect to prevent resubmission
        messages.success(request, "Registration successful!")
        # Fetch all data to display in "View Details"
        all_data = Datas.objects.all()

        # Return with the data after successful registration
        return render(request, 'registration.html', {'datas': all_data})

    # Return the registration page with no data initially
    return render(request, 'registration.html', {'datas': all_data})

# milestone 2
# About Us page view
def about(request):
    return render(request, 'about.html')


# views.py
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm  # If using a custom form class

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        full_message = f"Message from {name} ({email}):\n\n{message}"
        
        try:
            send_mail(
                'New Contact Form Submission', 
                full_message, 
                'youremail@example.com',  # Replace with your sender email
                [email],                  # Recipient: provided email
                fail_silently=False,
            )
            messages.success(request, 'Thank you for your message! We have sent you a confirmation email.')
            return redirect('contact')  # Adjust to your URL name
        except Exception as e:
            messages.error(request, 'An error occurred while sending the email.')
    return render(request, 'contact.html')

# Profile Settings Page
def profile_settings(request):
    return render(request, 'profile_settings.html')

# DASHBOARD
from django.shortcuts import render

def dashboard(request):
    # your logic here (e.g., fetching user data)
    return render(request, 'dashboard.html')  # or use HttpResponse, redirect, etc.

# View for Profile Page
def my_profile(request):
    # You can pass the user's profile information here
    return render(request, 'my_profile.html')

# View for Music Feed Page
def music_feed(request):
    # Render music feed (you might fetch data from a model or API)
    return render(request, 'music_feed.html')


# View for AI Recommendations Page
def ai_recommendations(request):
    # AI recommendations logic here (you can query AI suggestions)
    return render(request, 'ai_recommendations.html')

# View for Settings Page
def settings(request):
    return render(request, 'settings.html')


@login_required
def settings_view(request):
    profile_form = ProfileUpdateForm(instance=request.user)
    password_form = PasswordChangeForm(user=request.user)
    try:
        user_preferences = request.user.userpreferences
    except UserPreferences.DoesNotExist:
        user_preferences = UserPreferences(user=request.user)
        user_preferences.save()

    notification_form = NotificationPreferencesForm(instance=user_preferences)

    if request.method == 'POST':
        forms = {
            'profile': profile_form,
            'password': password_form,
            'notification': notification_form
        }

        for form_name, form in forms.items():
            if form.is_valid():
                form.save()
                messages.success(request, f"{form_name.capitalize()} updated successfully!")

        return redirect('settings')

    return render(request, 'settings.html', {
        'profile_form': profile_form,
        'password_form': password_form,
        'notification_form': notification_form
    })



# Upgrade Subscription view
@login_required
def upgrade_subscription(request):
    return render(request, 'upgrade_subscription.html')

# Process subscription upgrade
def process_upgrade_subscription(request, plan):
    selected_plan = SubscriptionPlan.objects.get(name=plan.capitalize())
    user_preferences = UserPreferences.objects.get(user=request.user)
    user_preferences.subscription_plan = selected_plan
    user_preferences.save()
    return redirect('settings')

# Change Password view
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Keep the user logged in after password change
            return redirect('settings')  # Redirect to settings page after successful password change
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

# Update Notifications view
@login_required
def update_notifications(request):
    notifications = request.user.notifications.all()
    for notification in notifications:
        notification.mark_as_read()
    return redirect('notifications')



# Admin dashboard view
from django.shortcuts import render, redirect
from django.shortcuts import render 

# admin Dashboard view
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


# views.py
from django.shortcuts import render, redirect
from .forms import SubscriptionPlanForm, SongCategoryForm, GenreForm, MusicTrackForm
from .models import SubscriptionPlan, SongCategory, Genre, MusicTrack
from django.contrib.auth import get_user_model

def manage_users(request):
    User = get_user_model()
    # Example logic to pass a list of users
    users = User.objects.all()  # You can modify this as per your requirement
    return render(request, 'manage_users.html', {'users': users})


# Subscription Plan Management
def manage_plans(request):
    if request.method == 'POST':
        form = SubscriptionPlanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_plans')
    else:
        form = SubscriptionPlanForm()
    plans = SubscriptionPlan.objects.all()
    return render(request, 'manage_plans.html', {'form': form, 'plans': plans})

# Genre Management
def manage_genres(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_genres')
    else:
        form = GenreForm()
    genres = Genre.objects.all()
    return render(request, 'manage_genres.html', {'form': form, 'genres': genres})

# Song Category Management
def manage_categories(request):
    if request.method == 'POST':
        form = SongCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_categories')
    else:
        form = SongCategoryForm()
    categories = SongCategory.objects.all()
    return render(request, 'manage_categories.html', {'form': form, 'categories': categories})

# Music Track Management
def manage_tracks(request):
    if request.method == 'POST':
        form = MusicTrackForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_tracks')
    else:
        form = MusicTrackForm()
    tracks = MusicTrack.objects.all()
    return render(request, 'manage_tracks.html', {'form': form, 'tracks': tracks})

from django.http import JsonResponse
from .models import SubscriptionPlan

def remove_plan(request, plan_id):
    if request.method == 'POST':
        try:
            # Attempt to delete the plan
            plan = SubscriptionPlan.objects.get(id=plan_id)
            plan.delete()  # Delete the plan from the database
            return JsonResponse({'success': True})  # Success response
        except SubscriptionPlan.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Plan not found.'})  # Plan not found error
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})  # Any other errors
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


# Logout view
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    print("Before logout - User:", request.user)  # Should show the logged-in user
    logout(request)
    request.session.flush()  # Clear all session data
    print("After logout - User:", request.user)  # Should show AnonymousUser
    return redirect('home')

from django.shortcuts import render
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

def search_music(request):
    client_id = "your_client_id"
    client_secret = "your_client_secret"

    sp = Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

    # Get query from the request
    query = request.GET.get('q', 'Imagine Dragons')

    # Search for tracks
    results = sp.search(q=query, limit=10)
    tracks = results['tracks']['items']

    return render(request, 'search_results.html', {'tracks': tracks})


# View for submitting a song request
def submit_song_request(request):
    if request.method == 'POST':
        form = SongRequestForm(request.POST)
        if form.is_valid():
            song_request = form.save(commit=False)
            song_request.user = request.user
            song_request.save()
            return redirect('home')  # Or send a success message to the user

    return redirect('home')

from django.shortcuts import render
from .models import MusicTrack  # or wherever your music tracks are stored

def search_music(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        # Perform the search logic here
        results = MusicTrack.objects.filter(title__icontains=search_query)  # Example query
        return render(request, 'home.html', {'results': results})
    return render(request, 'home.html')  # Render the page if no search query is provided

from django.shortcuts import render
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def search_spotify(request):
    client_id = 'your-client-id'
    client_secret = 'your-client-secret'
    client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    search_query = request.GET.get('query', '')
    if search_query:
        results = sp.search(q=search_query, limit=10, type='track')
        return render(request, 'search_results.html', {'results': results['tracks']['items']})

    return render(request, 'search_results.html', {'results': []})


from django.shortcuts import render
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def search_spotify(request):
    client_id = 'your-client-id'
    client_secret = 'your-client-secret'

    client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    search_query = request.GET.get('query', '')
    if search_query:
        results = sp.search(q=search_query, limit=10, type='track')
        return render(request, 'search_results.html', {'results': results['tracks']['items']})
    return render(request, 'search_results.html')

@login_required
def emusic(request):
    return render(request, 'emusic.html') 

# views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import SubscriptionPlan

def subscription_plans(request):
    subscription_plans = SubscriptionPlan.objects.all()
    return render(request, 'subscription_plans.html', {
        'subscription_plans': subscription_plans
    })

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserSubscription  # Assume this is your model for tracking subscriptions

# For Basic Plan
def subscription_basic(request):
    if request.method == 'POST':
        # Assume you have logic to handle the subscription
        user = request.user  # Get the currently logged-in user
        # Assuming 'Basic' is a choice in the UserSubscription model
        subscription = UserSubscription.objects.create(
            user=user,
            plan='Basic',  # You can adjust this field based on your model
            price=5.00  # Set the price or other relevant data
        )
        messages.success(request, "You have successfully subscribed to the Basic Plan!")
        return redirect('subscription_success')  # Redirect to a success page
    return render(request, 'subscription_plans.html')  # Render the subscription plans page


# For Premium Plan
def subscription_premium(request):
    if request.method == 'POST':
        user = request.user
        subscription = UserSubscription.objects.create(
            user=user,
            plan='Premium',
            price=10.00
        )
        messages.success(request, "You have successfully subscribed to the Premium Plan!")
        return redirect('subscription_success')
    return render(request, 'subscription_plans.html')

# For VIP Plan
def subscription_vip(request):
    if request.method == 'POST':
        user = request.user
        subscription = UserSubscription.objects.create(
            user=user,
            plan='VIP',
            price=20.00
        )
        messages.success(request, "You have successfully subscribed to the VIP Plan!")
        return redirect('subscription_success')
    return render(request, 'subscription_plans.html')

def subscription_success(request):
    return render(request, 'subscription_success.html')


from django.shortcuts import render

def payment_process(request):
    # Your logic for processing the payment
    return render(request, 'payment_template.html')

from django.shortcuts import render, redirect

def premium_plan(request):
    if request.method == 'POST':
        # Handle subscription logic here (e.g., payment, user subscription update)
        return redirect('subscription_success')  # Redirect to a success page or another page
    
    return render(request, 'premium_plan.html')

# views.py

from django.shortcuts import render, redirect

# View for Basic Plan
def basic_plan(request):
    if request.method == 'POST':
        # Handle the logic for subscribing to the basic plan
        return redirect('subscription_success')  # Redirect to a success page
    
    return render(request, 'basic_plan.html')  # Replace with your actual template

# View for Premium Plan
def premium_plan(request):
    if request.method == 'POST':
        # Handle the logic for subscribing to the premium plan
        return redirect('subscription_success')  # Redirect to a success page
    
    return render(request, 'premium_plan.html')  # Replace with your actual template

# View for VIP Plan
def vip_plan(request):
    if request.method == 'POST':
        # Handle the logic for subscribing to the VIP plan
        return redirect('subscription_success')  # Redirect to a success page
    
    return render(request, 'vip_plan.html')  # Replace with your actual template



from .models import Notification
from django.contrib.auth.models import User

def create_notification(user, message):
    Notification.objects.create(user=user, message=message)
   # Create a notification for a user
    user = User.objects.get(username="some_username")
    create_notification(user, "You have a new message!")


from django.shortcuts import render
from .models import Notification

def notifications(request):
    user_notifications = Notification.objects.filter(user=request.user)
    return render(request, 'notifications.html', {'notifications': user_notifications})

from django.http import HttpResponseRedirect
from .models import Notification

def mark_as_read(notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        notification.is_read = True
        notification.save()
    except Notification.DoesNotExist:
        pass  # Handle the case where the notification doesn't exist


def get_unread_notifications(user):
    return Notification.objects.filter(user=user, is_read=False)

# In your view, for example:
from .models import Notification

def notifications_view(request):
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
    return render(request, 'notifications.html', {'unread_notifications': unread_notifications})

from django.shortcuts import render
from django.http import JsonResponse
from .models import Song  # Assuming you have a Song model for your database

# Home Dashboard view
def dashboard(request):
    return render(request, 'dashboard.html')

# Song Search view
def song_search(request):
    if request.method == 'GET':
        song_name = request.GET.get('song_name', '').lower()
        # Example song data, ideally, this should come from the database
        song_database = [
            {'title': 'Shape of You', 'artist': 'Ed Sheeran', 'file': 'path_to_shape_of_you.mp3'},
            {'title': 'Blinding Lights', 'artist': 'The Weeknd', 'file': 'path_to_blinding_lights.mp3'},
            {'title': 'Levitating', 'artist': 'Dua Lipa', 'file': 'path_to_levitating.mp3'}
        ]
        
        song = next((s for s in song_database if song_name in s['title'].lower()), None)
        
        if song:
            return JsonResponse({'found': True, 'title': song['title'], 'artist': song['artist'], 'file': song['file']})
        else:
            return JsonResponse({'found': False})
    return render(request, 'song_search.html')


# Favorites view
def favorites(request):
    return render(request, 'favorites.html')

# Create Music view
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render

@csrf_exempt  # Temporarily to disable CSRF protection for debugging (remove later)
@require_POST  # Ensure it only accepts POST requests
def create_music(request):
    try:
        # Get data from the request body
        import json
        data = json.loads(request.body)
        title = data.get('title')
        description = data.get('description')
        
        # Your logic to handle the music creation
        if title and description:
            # Placeholder for music creation logic
            return JsonResponse({'success': True, 'message': 'Music generated successfully!'})
        else:
            return JsonResponse({'success': False, 'message': 'Both title and description are required.'})

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
from django.http import JsonResponse
import json

def create_music(request):
    if request.method == 'POST':
        try:
            # Parse JSON data sent in the request body
            data = json.loads(request.body)
            title = data.get('title')
            description = data.get('description')

            # Simulate lyric generation logic (replace with your AI logic)
            lyrics = f"Generated lyrics for '{title}':\n\n{description}...\n\nThis is an AI-generated song."

            return JsonResponse({'success': True, 'lyrics': lyrics})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

# Recent Activity view
def recent_activity(request):
    return render(request, 'recent_activity.html')

# Manage Playlists view
def manage_playlists(request):
    return render(request, 'manage_playlists.html')

# Music Feed view
def music_feed(request):
    return render(request, 'music_feed.html')

# AI Recommendations view
def ai_recommendations(request):
    return render(request, 'ai_recommendations.html')

# Settings view
def settings(request):
    return render(request, 'settings.html')


from django.shortcuts import render
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

def search_music(request):
    client_id = "your_client_id"
    client_secret = "your_client_secret"

    sp = Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

    # Get query from the request
    query = request.GET.get('q', 'Imagine Dragons')

    # Search for tracks
    results = sp.search(q=query, limit=10)
    tracks = results['tracks']['items']

    return render(request, 'search_results.html', {'tracks': tracks})


def spotify_login(request):
    client_id = settings.SPOTIFY_CLIENT_ID
    redirect_uri = settings.SPOTIFY_REDIRECT_URI
    scope = "user-read-private user-read-email"  # Add the necessary scope
    spotify_url = (
        f"https://accounts.spotify.com/authorize?"
        f"response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}"
    )
    return redirect(spotify_url)


# Handle Callback from Spotify
def spotify_callback(request):
    code = request.GET.get("code")
    client_id = settings.SPOTIFY_CLIENT_ID
    client_secret = settings.SPOTIFY_CLIENT_SECRET
    redirect_uri = settings.SPOTIFY_REDIRECT_URI

    # Exchange code for an access token
    token_url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret,
    }
    response = requests.post(token_url, data=payload)
    token_data = response.json()

    # Access the token (save it for further API calls)
    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")

    # Use the access token to fetch Spotify data
    headers = {"Authorization": f"Bearer {access_token}"}
    user_profile_url = "https://api.spotify.com/v1/me"
    user_profile_response = requests.get(user_profile_url, headers=headers)
    user_data = user_profile_response.json()

    return render(request, "spotify_dashboard.html", {"user_data": user_data})

def spotify_dashboard(request):
    # Your logic for the Spotify dashboard
    return render(request, 'spotify_dashboard.html')

from django.shortcuts import redirect
from django.contrib.auth import logout

def spotify_logout(request):
    # Log the user out of the Django application
    logout(request)
    
    # Optionally, redirect the user to Spotify's logout URL
    spotify_logout_url = 'https://www.spotify.com/logout/'  # Spotify's logout URL
    return redirect(spotify_logout_url)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# View to handle music creation
@csrf_exempt  # Temporarily disable CSRF protection (for testing, ideally use proper CSRF handling)
def create_music(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            title = data.get('title')
            description = data.get('description')

            # Your logic for generating music (e.g., using AI or creating a mock response)
            # For now, just return a success message
            return JsonResponse({'success': True, 'message': 'Music generated successfully!'})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)

    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import SubscriptionPlan
from .forms import SubscriptionPlanForm


def edit_plan(request, plan_id):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    if request.method == 'POST':
        form = SubscriptionPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return redirect('manage_plans')
    else:
        form = SubscriptionPlanForm(instance=plan)
    return render(request, 'edit_plan.html', {'form': form, 'plan': plan})

