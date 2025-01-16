from django.contrib import admin
from django.urls import path
from . import views

app_name = 'EMUSIC_Application'

urlpatterns = [
    # Authentication
    path('admin/', admin.site.urls),  # Admin URL
    path('login/', views.login_view, name='login'),
    path('', views.home_view, name='home'),
    path('home/', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),

    # Home and Profile
    
    path('profile/', views.profile_view, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('profile_settings/', views.profile_settings, name='profile_settings'),
    path('change_password/', views.change_password, name='change_password'),
    path('update_notifications/', views.update_notifications, name='update_notifications'),

    # Dashboards
    path('dashboard/', views.dashboard, name='user_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Subscription and Plans
    path('subscription_plans/', views.subscription_plans, name='subscription_plans'),
    path('subscription/basic/', views.basic_plan, name='subscription_basic'),
    path('subscription/premium/', views.premium_plan, name='subscription_premium'),
    path('subscription/vip/', views.vip_plan, name='subscription_vip'),
    path('subscription_payment/', views.payment_process, name='payment_process'),
    path('manage_plans/', views.manage_plans, name='manage_plans'),
    path('remove_plan/<int:plan_id>/', views.remove_plan, name='remove_plan'),

    # Music Management
    path('emusic/', views.emusic, name='EMUSIC'),
    path('create_music/', views.create_music, name='create_music'),
    path('manage-tracks/', views.manage_tracks, name='manage_tracks'),
    path('manage-playlists/', views.manage_playlists, name='manage_playlists'),
    path('manage-genres/', views.manage_genres, name='manage_genres'),
    path('manage-categories/', views.manage_categories, name='manage_categories'),
    path('music-feed/', views.music_feed, name='music_feed'),
    path('ai-recommendations/', views.ai_recommendations, name='ai_recommendations'),

    # Notifications
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/mark_as_read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),

    # Search
    path('search/', views.search_music, name='search_music'),
    path('song-search/', views.song_search, name='song_search'),

    # Favorites
    path('favorites/', views.favorites, name='favorites'),

    # Activity and Settings
    path('recent-activity/', views.recent_activity, name='recent_activity'),
    path('settings/', views.settings, name='settings'),

    # Spotify Integration
    path('songs/', views.spotify_login, name='spotify_login'),
    path('spotify_dashboard/', views.spotify_dashboard, name='spotify_dashboard'),
    path('callback/', views.spotify_callback, name='spotify_callback'),
    path('logout/', views.spotify_logout, name='spotify_logout'),

    # Static Pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    
]
