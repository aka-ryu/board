from django.db import models
from django.contrib.postgres.fields import ArrayField

class Post(models.Model):
    id = models.AutoField(primary_key=True) 
    title = models.CharField(max_length=255) 
    content = models.TextField()
    words = models.TextField()
    relation_ids = ArrayField(models.IntegerField(), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.title  
