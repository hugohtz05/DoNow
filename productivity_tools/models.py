from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    

class WeeklyReport(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    date = models.DateField()
    content = models.TextField()

    def __str__(self):
        return self.title
    

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.CharField(max_length=20)
    start_hour = models.CharField(max_length=5)
    end_hour = models.CharField(max_length=5)
    event_text = models.CharField(max_length=200)
    color = models.CharField(max_length=7)

    def __str__(self):
        return f"{self.event_text} ({self.day} {self.start_hour}-{self.end_hour})"

    class Meta:
        indexes = [
            models.Index(fields=['user', 'day']),
        ]