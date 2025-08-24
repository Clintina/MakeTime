# views.py
from django.shortcuts import render, redirect
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from .forms import MakeTimeFormSet
from .models import MakeTimeItem

def onboarding_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('schedule_demo')  # Next phase
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'onboarding.html', {'form': form})

@login_required
def onboarding_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('make_time_for')  # next phase
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'core/onboarding.html', {'form': form})

@login_required
def make_time_for_view(request):
    formset = MakeTimeFormSet(queryset=MakeTimeItem.objects.filter(user=request.user))
    if request.method == 'POST':
        formset = MakeTimeFormSet(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.user = request.user
                instance.save()
            return redirect('schedule_demo')  # next phase
    return render(request, 'core/make_time_for.html', {'formset': formset})