from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
# =================================================================================================
#
# Note: The requirement of the project
#
# We have task objects that a user has to complete, 
# each task has a title, an order field, a description 
# and a type (such as survey, discussion, diary). 

# We group tasks together in a container which we call a tile. 
# Each tile has a launch date and a status. 
# The status can be either live, pending or archived. 
# A tile can be made up of one or many tasks. 
# A task can only belong to a single tile.
#
# =================================================================================================
# 
# Model: Tile
class Tile(models.Model):
    # id =  models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    launch_date = models.DateField()
    STATUS_CHOICES = [
        ('live', 'Live'),
        ('pending', 'Pending'),
        ('archived', 'Archived'),
    ]
    status = models.CharField(max_length=20, default='live', choices=STATUS_CHOICES)

    def __str__(self):
        return self.name
#
# -------------------------------------------------------------------------------------------------
# Model: Tile

class Task(models.Model):
    # id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    order = models.IntegerField()
    description = models.TextField()
    TYPE_CHOICES = [
        ('survey', 'Survey'),
        ('discussion', 'Discussion'),   
        ('diary', 'Diary'),
    ]
    type = models.CharField(max_length=20, default='survey', choices=TYPE_CHOICES)
    tile = models.ForeignKey('Tile', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
#
# =================================================================================================

