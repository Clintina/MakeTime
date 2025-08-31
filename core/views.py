from django.shortcuts import render, redirect
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from .models import MakeTimeItem, Profile
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime, timedelta
from .forms import ProfileForm, TimeForm
from .models import Profile, MakeTimeItem
from django.contrib import messages

@login_required
def onboarding_view(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(
            user=request.user,
            occupation='',
            time_commitment=0,
            free_time_start=time(9, 0),  # 9:00 AM
            free_time_end=time(17, 0)    # 5:00 PM
        )

    form = ProfileForm(request.POST or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('make_time_for')

    return render(request, 'core/onboarding.html', {'form': form})


def make_time_for_view(request):
    TimeFormSet = formset_factory(TimeForm, extra=1, can_delete=True)
    formset = TimeFormSet(request.POST or None)

    if request.method == 'POST':
        print("🔄 POST received")
        formset = TimeFormSet(request.POST)

        if formset.is_valid():
            print("✅ Formset is valid")
            items = []

            for i, form in enumerate(formset):
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    try:
                        entry = form.save(commit=False)
                        entry.user = request.user
                        entry.save()
                        items.append(entry.label)
                        print(f"✔️ Saved item {i}: {entry.label}")
                    except Exception as e:
                        print(f"❗ Error saving item {i}: {e}")

            try:
                profile = request.user.profile
                print("🕒 Profile free time:", profile.free_time_start, "to", profile.free_time_end)

                blocks = generate_time_blocks(profile.free_time_start, profile.free_time_end)
                print("🧱 Time blocks generated:", blocks)

                if not blocks:
                    messages.warning(request, "No time blocks available. Please update your free time range.")
                    return redirect('onboarding')  # or wherever the user sets their availability

                schedule = assign_items_to_blocks(blocks, items)
                print("📋 Schedule assigned:", schedule)

                if not schedule:
                    messages.warning(request, "Schedule could not be generated. Try adding more items or adjusting your time range.")
                    return redirect('make_time_for')

                request.session['schedule'] = schedule
                print("📦 Schedule saved to session")

                return redirect('schedule_demo')

            except Exception as e:
                print("🚨 Error during schedule generation or redirect:", e)
                messages.error(request, "Something went wrong while generating your schedule.")
                return redirect('make_time_for')

        else:
            print("❌ Formset is NOT valid")
            for i, form in enumerate(formset.forms):
                print(f"Form {i} errors: {form.errors}")
            print("Non-form errors:", formset.non_form_errors())
            messages.error(request, "Please fix the errors in the form.")

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
        # No need to create Profile here — signal will handle it
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

def home_view(request):
    if request.user.is_authenticated:
        profile = getattr(request.user, 'profile', None)
        if profile and profile.occupation and profile.time_commitment and profile.free_time_start and profile.free_time_end:
            return redirect('schedule_demo')
        else:
            return redirect('onboarding')
    return render(request, 'core/home.html')