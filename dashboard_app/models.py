from django.db import models

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('낮음', '낮음'),
        ('중간', '중간'),
        ('높음', '높음'),
    ]

    STATUS_CHOICES = [
        ('계획 중', '계획 중'),
        ('진행 중', '진행 중'),
        ('완료', '완료'),
    ]

    title = models.CharField(max_length=100)
    assignee = models.CharField(max_length=100, blank=True)
    start_date = models.DateField(null=True, blank=True, default='2024-01-01')
    end_date = models.DateField(null=True, blank=True, default='2024-12-31')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='계획 중')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='중간')
    progress = models.PositiveIntegerField(default=0)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class MeetingNote(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

