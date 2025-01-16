from django.contrib import admin
from django.urls import path, include
from EMUSIC_Application import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

app_name = 'EMUSIC_Application'

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin URL
    path('', include('EMUSIC_Application.urls')),  # Include the app's URLs here

    # Authentication URLs
    path('login/', views.login_view, name='login'),  # Custom login view
    path('', views.home_view, name='home'),  # Home page
    path('home/', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),  # Add the signup URL here
    

    # Home and Dashboard URLs
    path('', views.home_view, name='home'),  # Home page
    path('home/', views.home_view, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # User profile and subscription URLs
    path('my_profile/', views.my_profile, name='my_profile'),
    path('profile/', views.profile_view, name='profile'),  # Ensure this URL pattern exists
    path('update_profile/', views.update_profile, name='update_profile'),
    path('subscription_plans/', views.subscription_plans, name='subscription_plans'),
    path('profile_settings/', views.profile_settings, name='profile_settings'),
    path('change_password/', views.change_password, name='change_password'),
    path('update_notifications/', views.update_notifications, name='update_notifications'),
    path('upgrade_subscription/', views.upgrade_subscription, name='upgrade_subscription'),
    path('subscription/basic/', views.basic_plan, name='subscription_basic'),
    path('subscription/premium/', views.premium_plan, name='subscription_premium'),
    path('subscription/vip/', views.vip_plan, name='subscription_vip'),
    path('subscription_success/', views.subscription_success, name='subscription_success'),
    path('subscription_payment/', views.payment_process, name='payment_process'),

    # Music and genres
    path('emusic/', views.emusic, name='emusic'),  # The genres page
    path('music-feed/', views.music_feed, name='music_feed'),
    path('create_music/', views.create_music, name='create_music'),
    path('ai-recommendations/', views.ai_recommendations, name='ai_recommendations'),

    # Settings and notifications
    path('settings/', views.settings, name='settings'),
    path('notifications/', views.notifications, name='notifications'),

    # Admin and management URLs
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage_users/', views.manage_users, name='manage_users'),
    path('manage_categories/', views.manage_categories, name='manage_categories'),
    path('manage_genres/', views.manage_genres, name='manage_genres'),
    path('manage_plans/', views.manage_plans, name='manage_plans'),
    path('manage_tracks/', views.manage_tracks, name='manage_tracks'),

      # Spotify Integration
    path('songs/', views.spotify_login, name='spotify_login'),
    path('spotify_dashboard/', views.spotify_dashboard, name='spotify_dashboard'),
    path('callback/', views.spotify_callback, name='spotify_callback'),


    # Static content
    path('about/', views.about, name='about'),  # About Us page
    path('contact/', views.contact, name='contact'),  # Contact Us page
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
