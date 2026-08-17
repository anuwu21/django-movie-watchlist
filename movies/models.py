from django.db import models
from django.contrib.auth.models import User
class Movie(models.Model):

    user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='movies'
    )

    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    year = models.IntegerField()
    rating = models.FloatField()
    description = models.TextField()
    watched = models.BooleanField(default=False)
    favorite = models.BooleanField(default=False)
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)

    
# Create your models here.
