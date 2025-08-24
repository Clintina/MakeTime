from django.urls import path
from .views import onboarding_view
from .views import make_time_for_view

urlpatterns = [
    path('onboarding/', onboarding_view, name='onboarding'),
    path('make_time_for/', make_time_for_view, name='make_time_for'),
]