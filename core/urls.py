from django.urls import path
from django.contrib.auth import views as auth_views
from .views import onboarding_view
from .views import make_time_for_view
from .views import schedule_demo_view
from .views import signup_view

urlpatterns = [
    path('onboarding/', onboarding_view, name='onboarding'),
    path('make_time_for/', make_time_for_view, name='make_time_for'),
    path('schedule_demo/', schedule_demo_view, name='schedule_demo'),
    path('signup/', signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),

]