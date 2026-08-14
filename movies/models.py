from django.db import models
class Movie(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    year = models.IntegerField()
    rating = models.FloatField()
    description = models.TextField()
    watched = models.BooleanField(default=False)
    favorite = models.BooleanField(default=False)
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)

# Create your models here.
