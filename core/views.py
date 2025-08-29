from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, MakeTimeFormSet
from .models import MakeTimeItem, Profile
from django.contrib.auth.forms import UserCreationForm

@login_required
def onboarding_view(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(
            user=request.user,
            occupation='',
            time_commitment=0,
            free_time_start='00:00',
            free_time_end='00:00'
        )

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('make_time_for')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'core/onboarding.html', {'form': form})


@login_required
def make_time_for_view(request):
    if request.method == 'POST':
        print("POST request received")
        formset = MakeTimeFormSet(request.POST)
        if formset.is_valid():
            print("Formset is valid!")
            for form in formset:
                print("Cleaned data:", form.cleaned_data)
                data = form.cleaned_data
                if data.get('category') and data.get('label'):
                    instance = form.save(commit=False)
                    instance.user = request.user
                    instance.save()
            print("Redirecting now...")
            return redirect('schedule_demo')
        else:
            print("Formset is invalid!")
            print(formset.errors)
    else:
        formset = MakeTimeFormSet(queryset=MakeTimeItem.objects.filter(user=request.user))

    return render(request, 'core/make_time_for.html', {'formset': formset})


@login_required
def schedule_demo_view(request):
    return render(request, 'core/schedule_demo.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('onboarding')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})