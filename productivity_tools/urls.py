from django.urls import path
from .views import dashboard, excalidraw, agenda, reset_agenda, save_event, pomodoro, add_to_do, delete_to_do, weekly_report, create_weekly_report, detail_weekly_report, delete_weekly_report, update_weekly_report

app_name = 'productivity_tools'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('agenda/', agenda, name='agenda'),
    path('save_event/', save_event, name='save_event'),
    path('reset_agenda/', reset_agenda, name='reset_agenda'),
    path('excalidraw/', excalidraw, name='excalidraw'),
    path("pomodoro/", pomodoro, name="pomodoro"),
    path("add-to-do/", add_to_do, name="add_to_do"),
    path("delete-to-do/<int:pk>/", delete_to_do, name="delete_to_do"),
    path("weekly-report/", weekly_report, name="weekly_report"),
    path("create-weekly-report/", create_weekly_report, name="create_weekly_report"),
    path("detail-weekly-report/<int:pk>/", detail_weekly_report, name="detail_weekly_report"),
    path("delete-weekly-report/<int:pk>/", delete_weekly_report, name="delete_weekly_report"),
    path("update-weekly-report/<int:pk>/", update_weekly_report, name="update_weekly_report"),
]