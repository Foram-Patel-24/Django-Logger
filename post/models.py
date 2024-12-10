from django.db import models
from user.models import User
from django.utils.timezone import now

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User , on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    content = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE , related_name='post_created')
    updated_by = models.ForeignKey(User,on_delete=models.SET_NULL , null=True , related_name='post_updated')
    deleted = models.IntegerField(default=0)