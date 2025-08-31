from django.shortcuts import render, redirect
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from .models import MakeTimeItem, Profile
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime, timedelta
from .forms import ProfileForm, TimeForm
from .models import Profile, MakeTimeItem

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

    form = ProfileForm(request.POST or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('make_time_for')

    return render(request, 'core/onboarding.html', {'form': form})


def make_time_for_view(request):
    TimeFormSet = formset_factory(TimeForm, extra=1, can_delete=True)

    if request.method == 'POST':
        formset = TimeFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    entry = form.save(commit=False)
                    entry.user = request.user  # if using auth
                    entry.save()
            return redirect('schedule_demo')
    else:
        formset = TimeFormSet()

    return render(request, 'core/make_time_for.html', {'formset': formset})



@login_required
def schedule_demo_view(request):
    schedule = request.session.get('schedule')
    if not schedule:
        return redirect('make_time_for')  # fallback if session is empty
    return render(request, 'core/schedule_demo.html', {'schedule': schedule})


def signup_view(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        return redirect('onboarding')
    return render(request, 'core/signup.html', {'form': form})


def generate_time_blocks(start, end):
    blocks = []
    current = datetime.combine(datetime.today(), start)
    end_time = datetime.combine(datetime.today(), end)
    while current < end_time:
        blocks.append(current.time())
        current += timedelta(hours=1)
    return blocks


def assign_items_to_blocks(blocks, items):
    schedule = {}
    for i, block in enumerate(blocks):
        item = items[i % len(items)] if items else "Free Time"
        schedule[block.strftime('%I:%M %p')] = item
    return schedule