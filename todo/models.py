from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)  # ← 追加！

    class Meta:
        ordering = ['order']  # 自動並び順指定

    def __str__(self):
        return self.title
