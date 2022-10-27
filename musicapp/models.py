from email.policy import default
from django.db import models

# Create your models here.


class Artiste(models.Model):
    first_name = models.CharField (
        max_length=255,
    )
    
    last_name = models.CharField (
        max_length=255,
    )
    
    age = models.IntegerField (
        
    )
    
class  Song(models.Model):
    
    title = models.CharField(
        max_length=255
    )
    
    date_released = models.DateTimeField(
        
    )
    
    likes = models.IntegerField(
        default=0
        
    )
    
    artiste = models.ForeignKey(
        Artiste,on_delete = models.CASCADE,
    )


class  Lyric(models.Model):
    
    content = models.CharField(
        max_length=255,
        default=""
    )
    
    song = models.ForeignKey(
        Song,on_delete = models.CASCADE,
    )
    