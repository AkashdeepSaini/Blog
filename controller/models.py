from django.db import models
from django.contrib.auth.models import User , AbstractUser
# Create your models here.

class Author(AbstractUser):
    bio = models.TextField()
    def __str__(self):
        return self.username    

    
class Article(models.Model):
    author = models.ForeignKey(Author , on_delete=models.CASCADE , related_name="written_by" )
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=225 , unique=True)
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.title} by {self.author}'