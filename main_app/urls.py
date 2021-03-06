from django.urls import path, include
from . import views

urlpatterns = [
    
    # Daily / Weekly / Monthly
    path('daily/', views.DailySchedule.as_view(), name="daily_schedule"), 
    path('weekly/', views.WeeklySchedule.as_view(), name="weekly_schedule"),
    path('monthly/', views.MonthlySchedule.as_view(), name="monthly_schedule"),
    
    # Create
    path('day/new', views.DayCreate.as_view(), name="day_create"),
    path('schedule/new/<int:day_id>', views.ScheduleCreate.as_view(), name="schedule_create"),
    
    # Update
    path('schedule/<int:pk>/update',
        views.ScheduleUpdate.as_view(), name="schedule_update"),
    path('memo/<int:pk>/update',
        views.MemoUpdate.as_view(), name="memo_update"),
   
    # Delete
    path('schedule/<int:pk>/delete',
        views.ScheduleDelete.as_view(), name="schedule_delete"),
    
    # Sign on / Sign off
    path('accounts/signup/', views.Signup.as_view(), name="signup"),

]