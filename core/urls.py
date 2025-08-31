from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    home_view,
    signup_view,
    onboarding_view,
    make_time_for_view,
    schedule_demo_view,
)

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('signup/', signup_view, name='signup'),
    path('onboarding/', onboarding_view, name='onboarding'),
    path('make_time_for/', make_time_for_view, name='make_time_for'),
    path('schedule/', schedule_demo_view, name='schedule_demo'),
]