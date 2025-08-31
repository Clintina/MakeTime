from datetime import datetime, timedelta
from django.shortcuts import render
from core.models import Profile

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
        item = items[i % len(items)]  # Rotate through items
        schedule[block.strftime('%I:%M %p')] = item
    return schedule

def schedule_view (request):
    profile = request.user.profile
    blocks = generate_time_blocks(profile.free_time_start, profile.free_time_end)

    # Example items — replace with actual user selections
    items = ["Hobby", "Person", "Self", "Work", "Other"]
    schedule = assign_items_to_blocks(blocks, items)

    return render(request, 'schedule_demo.html', {'schedule': schedule})

def onboarding_view(request):
    return render(request, 'maketime/onboarding.html')
