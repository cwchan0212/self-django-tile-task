from django.contrib.auth.models import User, Group
from .models import Tile, Task
from rest_framework import serializers

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'order', 'description', 'type', 'tile']
        required = False

class TileSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, source='task_set', required=False)
    class Meta:
        model = Tile
        fields = ['id', 'name', 'launch_date', 'status', 'tasks']