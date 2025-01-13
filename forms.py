# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # Adjust this import as needed

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'password', 'address', 'mailid',]

# Registration

from django import forms
from .models import Datas

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Datas
        fields = ['Name', 'Age', 'Gender', 'Address', 'Contact', 'Mail']



from django import forms
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'email', 'password', 'address', 'mailid']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

from django import forms
from .models import Artist

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'genre', 'birth_date', 'bio']

from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import UserProfile

class ProfileUpdateForm(UserChangeForm):
    profile_picture = forms.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'profile_picture']

    def save(self, commit=True):
        user = super().save(commit=False)
        if 'profile_picture' in self.cleaned_data:
            profile_picture = self.cleaned_data['profile_picture']
            user.profile.profile_picture = profile_picture
        if commit:
            user.save()
        return user

# forms.py
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import UserPreferences
from django.contrib.auth.models import User

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput, required=True)
    new_password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_new_password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_new_password = cleaned_data.get("confirm_new_password")
        if new_password != confirm_new_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class NotificationPreferencesForm(forms.ModelForm):
    class Meta:
        model = UserPreferences
        fields = ['email_notifications', 'sms_notifications']

# In forms.py
from django import forms
from EMUSIC_Application.models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email') # Add any additional fields here


# forms.py
from django import forms
from .models import SubscriptionPlan, SongCategory, Genre, MusicTrack

class SubscriptionPlanForm(forms.ModelForm):
    class Meta:
        model = SubscriptionPlan
        fields = ['name', 'price', 'duration', 'features']

class SongCategoryForm(forms.ModelForm):
    class Meta:
        model = SongCategory
        fields = ['name']

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']

class MusicTrackForm(forms.ModelForm):
    class Meta:
        model = MusicTrack
        fields = ['title', 'artist', 'genre', 'category', 'file', 'price']


from django import forms
from .models import SongRequest

class SongRequestForm(forms.ModelForm):
    class Meta:
        model = SongRequest
        fields = ['song_title', 'artist']


# forms.py
class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio']  # Fields from UserProfile

    bio = forms.CharField(widget=forms.Textarea, required=False)  # Add bio field if needed for the profile

    # Adding extra fields for username and email from the CustomUser model
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(max_length=255, required=True)

    def __init__(self, *args, **kwargs):
        # Initialize the form with instance data
        user = kwargs.get('instance')  # This should be a CustomUser instance
        super(ProfileForm, self).__init__(*args, **kwargs)

        if user:
            # Access the username and email directly from the CustomUser instance
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email
            # Access bio from UserProfile (not CustomUser)
            self.fields['bio'].initial = user.userprofile.bio if user.userprofile else None  # Check for UserProfile

    def save(self, commit=True):
        # Save the profile data, including user information
        user = super().save(commit=False)

        # Ensure the user has a UserProfile (create it if it doesn't exist)
        user_profile, created = UserProfile.objects.get_or_create(user=user)

        # Save the user and profile data
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']

        # Save bio and profile picture to the UserProfile model
        user_profile.bio = self.cleaned_data['bio']
        user_profile.profile_picture = self.cleaned_data['profile_picture']

        if commit:
            user.save()
            user_profile.save()

        return user_profile



from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # Correct import of CustomUser model

class SignupForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        help_text='Enter a valid email address',
        error_messages={
            'invalid': 'Please enter a valid email address.',
            'required': 'Email address is required.',
        }
    )
    first_name = forms.CharField(
        max_length=100,
        error_messages={'required': 'First name is required.'}
    )
    last_name = forms.CharField(
        max_length=100,
        error_messages={'required': 'Last name is required.'}
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']  # Using 'email' instead of 'mailid'

        error_messages = {
            'username': {
                'required': 'This field is required.',
                'unique': 'This username is already taken.',
            },
            'password1': {
                'required': 'Please enter a password.',
            },
            'password2': {
                'required': 'Please confirm your password.',
                'mismatch': 'The two password fields don’t match.',
            },
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')  # Using 'email' field name
        if CustomUser.objects.filter(mailid=email).exists():  # Check against 'mailid' in model
            raise forms.ValidationError('This email is already taken.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.mailid = self.cleaned_data.get('email')  # Setting the 'mailid' field in model
        if commit:
            user.save()
        return user




class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    


from django import forms
from .models import SubscriptionPlan

class SubscriptionPlanForm(forms.ModelForm):
    class Meta:
        model = SubscriptionPlan
        fields = ['name', 'description', 'price', 'is_active']


from django.conf import settings

admin_email = settings.ADMIN_EMAIL  # This will give you the value from settings.py


# forms.py
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
