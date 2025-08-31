from django import forms
from .models import Profile
from .models import MakeTimeItem
from django.forms import modelformset_factory
from .models import MakeTimeItem

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['occupation', 'time_commitment', 'free_time_start', 'free_time_end']

class MakeTimeItemForm(forms.ModelForm):
    class Meta:
        model = MakeTimeItem
        fields = ['category', 'label', 'contact_name', 'phone_number']

MakeTimeItemFormSet = modelformset_factory(
    MakeTimeItem,
    form=MakeTimeItemForm,
    extra=1,
    can_delete=True)

class TimeForm(forms.ModelForm):
    class Meta:
        model = MakeTimeItem
        fields = ['category', 'label', 'contact_name', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False




