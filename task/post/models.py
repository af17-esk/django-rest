from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):

    title = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "User Post"
        verbose_name_plural = "User Post"

    def __str__(self):
        return self.title
