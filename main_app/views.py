from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic.base import TemplateView
from main_app.forms import ScheduleCreateForm
from .models import Day, Schedule
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse
import calendar
from datetime import date, datetime, timedelta
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class DayCreate(View):
    def get(self, request):
        return render(request, "day_create.html")
    
    def post(self, request):
        date = request.POST.get("date")
        time = request.POST.get("time")
        content = request.POST.get("content")
        memo = request.POST.get("memo")
        dayContent = Day.objects.create(date=date, memo=memo)
        Schedule.objects.create(time=time, content=content, day_id=dayContent.id)
        return redirect('daily_schedule')

@method_decorator(login_required, name='dispatch')
class ScheduleCreate(View):
    def get(self, request, day_id):
        form = ScheduleCreateForm()
        return render(request, "schedule_create.html", context={'form':form})
    def post(self, request, day_id):
        form = ScheduleCreateForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.user = request.user
            schedule.day_id = day_id
            schedule.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return render(request, "schedule_create.html", context={'form':form})
    
@method_decorator(login_required, name='dispatch')
class ScheduleUpdate(UpdateView):
    model = Schedule
    fields = ['time', 'content', 'day']
    template_name = "schedule_update.html"
    success_url = "/daily/"
      
@method_decorator(login_required, name='dispatch')    
class MemoUpdate(UpdateView):
    model = Day
    fields = ['memo']
    template_name = "memo_update.html"
    success_url = "/daily/"   

@method_decorator(login_required, name='dispatch')
class ScheduleDelete(DeleteView):
    model = Schedule
    template_name = "schedule_delete.html"
    success_url = "/daily/"

@method_decorator(login_required, name='dispatch')
class DailySchedule(TemplateView):
    template_name = "daily_view.html"
    def get_context_data(self, **kwargs):
        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        context = super().get_context_data(**kwargs)
        context["days"] = Day.objects.filter(date__in=[today, tomorrow]) 
        return context

@method_decorator(login_required, name='dispatch')
class WeeklySchedule(TemplateView):
    template_name = "weekly_view.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = datetime.now().date()
        week_start = date - timedelta(date.weekday())
        week_end = week_start + timedelta(6)
        day_of_week = date.isoweekday()
        context["first_day"] = week_start
        context["last_day"] = week_end
        context["week_day"] = day_of_week
        context["days"] = Day.objects.filter(date__range=[week_start, week_end]) 
        return context
     
@method_decorator(login_required, name='dispatch')
class MonthlySchedule(View):

    def get(self, request):
        context = {}
        date = datetime.now().date()
        current_month_name = calendar.month_name[date.today().month]
        month_start = date.replace(day = 1)
        month_end = date.replace(day = calendar.monthrange(date.year, date.month)[1])
        context["current_month"] = current_month_name
        context["first_day"] = month_start
        context["last_day"] = month_end
        context["range"] = range(month_start.day, month_end.day+1)
        context["days"] = Day.objects.filter(date__range=[month_start, month_end]) 
        return render(request, "monthly_view.html", context=context)
    
class Signup(View):
    def get(self, request):
        form = UserCreationForm()
        context = {"form": form}
        return render(request, "registration/signup.html", context)
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("daily_schedule")
        else:
            context = {"form": form}
            return render(request, "registration/signup.html", context)