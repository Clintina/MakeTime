from django import forms
from .models import Profile
from .models import MakeTimeItem
from django.forms import modelformset_factory

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['occupation', 'time_commitment', 'free_time_start', 'free_time_end']

class MakeTimeItemForm(forms.ModelForm):
    class Meta:
        model = MakeTimeItem
        fields = ['category', 'label', 'contact_name', 'contact_email']

MakeTimeFormSet = modelformset_factory(
    MakeTimeItem,
    form=MakeTimeItemForm,
    extra=3,
    can_delete=True
)
