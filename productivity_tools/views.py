from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect, render
from .forms import TaskForm, weekly_report_form
from .models import Task , WeeklyReport, Event
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

def homePage(request):
    return render(request, 'productivity_tools/home.html')

@login_required
def dashboard(request):
    task = Task.objects.filter(user=request.user)[:15]
    report = WeeklyReport.objects.filter(user=request.user).order_by('-date')[:5]

    context = {
        'task': task,
        'report': report,
    }
    return render(request, 'productivity_tools/dashboard.html', context)

def excalidraw(request):
    return render(request, 'productivity_tools/excalidraw.html')

def pomodoro(request):
    return render(request, 'productivity_tools/pomodoro.html')


def add_to_do(request):
    tasks = Task.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False) 
            task.user = request.user
            form.save()
            return redirect('productivity_tools:add_to_do')
    else:
        form = TaskForm()
    
    return render(request, 'productivity_tools/todo.html', {'form': form, 'tasks': tasks})


def delete_to_do(request, pk):
    task = Task.objects.get(pk=pk)
    task.delete()
    return redirect('productivity_tools:add_to_do')


def weekly_report(request):
    reports = WeeklyReport.objects.filter(user=request.user).order_by('-date')  

    paginator = Paginator(reports, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'productivity_tools/weekly-report.html', {'reports': reports, 'page_obj': page_obj})

def create_weekly_report(request):
    if request.method == 'POST':
        form = weekly_report_form(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            form.save()
            return redirect('productivity_tools:weekly_report')
        else:
            print(form.errors)
    else:
        form = weekly_report_form()    
    return render(request, 'productivity_tools/create_weekly_report.html', {'form': form})

def detail_weekly_report(request, pk):
    reports = get_object_or_404(WeeklyReport, pk=pk)  
    return render(request, 'productivity_tools/detail_weekly_report.html', {'reports': reports})


def delete_weekly_report(request, pk):
    report = WeeklyReport.objects.get(pk=pk)
    report.delete()
    return redirect('productivity_tools:weekly_report')


def update_weekly_report(request, pk):
    report = get_object_or_404(WeeklyReport, pk=pk)
    if request.method == 'POST':
        form = weekly_report_form(request.POST, instance=report)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            form.save()
            return redirect('productivity_tools:detail_weekly_report', pk=report.pk)
    else:
        form = weekly_report_form(instance=report)
    return render(request, 'productivity_tools/update_weekly_report.html', {'form': form})

@login_required
def agenda(request):
    days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    hours = [f"{hour}:00" for hour in range(5, 24)]
    
    events = Event.objects.filter(user=request.user).select_related('user')
    event_data = {}
    
    for event in events:
        key = f"{event.day}-{event.start_hour}"
        event_data[key] = {
            'event_text': event.event_text,
            'color': event.color,
            'end_hour': event.end_hour
        }
    
    return render(request, 'productivity_tools/agenda.html', {
        'events': event_data,
        'hours': hours,
        'days': days,
    })

@login_required
def save_event(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            required_fields = ['event', 'color', 'day', 'hour', 'end-hour']
            if not all(field in data for field in required_fields):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Données incomplètes'
                })
            
            # Création de l'événement
            event = Event.objects.create(
                user=request.user,
                event_text=data['event'],
                color=data['color'],
                day=data['day'],
                start_hour=data['hour'],
                end_hour=data['end-hour']
            )
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    return JsonResponse({
        'status': 'error',
        'message': 'Méthode non autorisée'
    })


@login_required
def reset_agenda(request):
    if request.method == 'POST':
        try:
            # Suppression sécurisée des événements de l'utilisateur
            events_deleted = Event.objects.filter(user=request.user).delete()[0]
            
            return JsonResponse({
                'status': 'success',
                'message': f'{events_deleted} événement(s) ont été supprimés'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Méthode non autorisée'
    }, status=405)