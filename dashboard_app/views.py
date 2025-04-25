from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, MeetingNote
from .forms import TaskForm, MeetingNoteForm
from django.http import JsonResponse
import json
from datetime import datetime
from django.utils.dateparse import parse_date
from collections import OrderedDict
from calendar import monthrange

# 홈 대시보드: 작업 + 회의록 리스트
def task_dashboard(request):
    tasks = Task.objects.all().order_by('end_date')
    meeting_notes = MeetingNote.objects.all().order_by('-created_at')[:5]
    return render(request, 'dashboard_app/task_dashboard.html', {
        'tasks': tasks,
        'meeting_notes': meeting_notes,
    })

# 작업 추가
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_dashboard')
    else:
        form = TaskForm()
    return render(request, 'dashboard_app/task_form.html', {'form': form})

# 작업 상세 보기

def task_detail(request, id):
    task = get_object_or_404(Task, id=id)
    meeting_notes = task.meetingnote_set.all().order_by('-created_at')
    return render(request, 'dashboard_app/task_detail.html', {
        'task': task,
        'meeting_notes': meeting_notes,
    })

# 작업 인라인 업데이트
def update_task_inline(request, id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=id)
        data = json.loads(request.body)
        field = data.get('field')
        value = data.get('value')

        if hasattr(task, field):
            # 날짜 처리
            if field in ['start_date', 'end_date']:
                value = parse_date(value)
            # 숫자 처리
            elif field == 'progress':
                try:
                    value = int(value)
                except ValueError:
                    return JsonResponse({'success': False})
            # 불리언 처리
            elif field == 'is_done':
                value = value in ['true', 'True', True]

            setattr(task, field, value)
            task.save()
            return JsonResponse({'success': True})

    return JsonResponse({'success': False})

# 회의록 추가
def add_meeting_note(request):
    if request.method == 'POST':
        form = MeetingNoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_dashboard')
    else:
        form = MeetingNoteForm()
    return render(request, 'dashboard_app/meeting_form.html', {'form': form})

def meeting_list(request):
    notes = MeetingNote.objects.all().order_by('-created_at')
    return render(request, 'dashboard_app/meeting_list.html', {'notes': notes})

def meeting_detail(request, id):
    note = get_object_or_404(MeetingNote, id=id)
    return render(request, 'dashboard_app/meeting_detail.html', {'note': note})

def add_meeting_note(request):
    if request.method == 'POST':
        form = MeetingNoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('meeting_list')
    else:
        form = MeetingNoteForm()
    return render(request, 'dashboard_app/meeting_form.html', {'form': form})

def board_view(request):
    tasks = Task.objects.all()
    return render(request, 'dashboard_app/board_view.html', {
        'tasks': tasks,
        'status_choices': Task.STATUS_CHOICES,
        'view_name': 'board_view',
    })

from django.utils.timezone import datetime

def timeline_view(request):
    tasks = Task.objects.all().order_by('start_date')

    reference_date = datetime(2024, 1, 1)  # 예시 기준일
    task_data = []

    for task in tasks:
        if task.start_date and task.end_date:
            duration = (task.end_date - task.start_date).days
            offset = (task.start_date - reference_date.date()).days
            task_data.append({
                'title': task.title,
                'duration': duration,
                'offset': offset,
            })

    return render(request, 'dashboard_app/task_timeline.html', {
        'tasks': task_data,
        'month_labels': month_labels.values(),
        'view_name': 'timeline_view'
    })


reference_date = datetime(2024, 4, 1).date()
last_date = max([task.end_date for task in Task.objects.all() if task.end_date])

# 월별 라벨 데이터 구성
month_labels = OrderedDict()
current = reference_date
while current <= last_date:
    year_month = current.strftime('%Y-%m')
    days_in_month = monthrange(current.year, current.month)[1]
    month_labels[year_month] = {
        'label': current.strftime('%m월'),
        'offset': (current - reference_date).days * 10,
        'width': days_in_month * 10
    }
    # 다음 달로 이동
    if current.month == 12:
        current = current.replace(year=current.year + 1, month=1, day=1)
    else:
        current = current.replace(month=current.month + 1, day=1)