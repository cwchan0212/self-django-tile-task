from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpResponse
from .serializers import TileSerializer, TaskSerializer
from .models import Tile, Task
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, status

# Create your views here.
# =================================================================================================
#
# Note: 
# Trade-offs between views vs viewsets
# https://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/

# Using viewsets can be a really useful abstraction. It helps ensure that URL conventions will be 
# consistent across your API, minimizes the amount of code you need to write, and allows you to 
# concentrate on the interactions and representations your API provides rather than the specifics 
# of the URL conf.

# That doesn't mean it's always the right approach to take. There's a similar set of trade-offs 
# to consider as when using class-based views instead of function based views. Using viewsets is 
# less explicit than building your views individually.
#
# =================================================================================================
#
# -------------------------------------------------------------------------------------------------
# Method 1: Use ViewSet
# API Root: http://127.0.0.1:8080
# "tiles": "http://127.0.0.1:8000/tiles/",
# "tasks": "http://127.0.0.1:8000/tasks/"
#
# -------------------------------------------------------------------------------------------------
# Model: tile
class TileViewSet(viewsets.ModelViewSet):
    queryset = Tile.objects.all()
    serializer_class = TileSerializer
    
    # POST method
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # GET method
    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(id=kwargs['pk'])
        instance = get_object_or_404(queryset, pk=kwargs['pk'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # PUT method
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        queryset = self.get_queryset().filter(id=kwargs['pk'])
        instance = get_object_or_404(queryset, pk=kwargs['pk'])
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete method
    def destroy(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(id=kwargs['pk'])
        instance = get_object_or_404(queryset, pk=kwargs['pk'])
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# -------------------------------------------------------------------------------------------------
# Model: task
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    # POST method
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        # data['tile'] = kwargs['pk']
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # GET method
    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(id=kwargs['pk'])
        instance = get_object_or_404(queryset, pk=kwargs['pk'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # PUT method
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        queryset = self.get_queryset().filter(id=kwargs['pk'])
        instance = get_object_or_404(queryset, pk=kwargs['pk'])
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE method
    def destroy(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(id=kwargs['pk'])
        instance = get_object_or_404(queryset, pk=kwargs['pk'])
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# -------------------------------------------------------------------------------------------------
# Method 2: Use Views
# tile 
# GET: http://127.0.0.1:8000/v2/tiles
@api_view(['GET'])
def tiles_all(request, format=None):
    tiles = Tile.objects.all()
    serializer = TileSerializer(tiles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
#
# POST: http://127.0.0.1:8000/v2/tiles
# GET / PUT / DELETE: http://127.0.0.1:8000/v2/tile/<int:tile_id>
#
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def tile_one(request, tile_id=None, format=None):
    if request.method == 'POST':
        serializer = TileSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:         
        try:
            tile = Tile.objects.get(pk=tile_id)
        except Tile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if request.method == "GET":
            serializer = TileSerializer(tile)
            return Response(serializer.data)
        
        elif request.method == "PUT":
            serializer = TileSerializer(tile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == "DELETE":
            tile.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

# -------------------------------------------------------------------------------------------------
# task
# GET:  http://127.0.0.1:8000/v2/tasks
@api_view(['GET'])
def tasks_all(request, format=None):
    # GET method: Get all tasks
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
#
# POST: http://127.0.0.1:8000/v2/tile/<int:tile_id>/task
# GET / PUT / DELETE: http://127.0.0.1:8000/v2/tile/<int:tile_id>/task/<int:task_id>
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def task_one(request, tile_id, task_id=None, format=None):
    if tile_id is None:
        return Response({'error': 'tile_id parameter is missing'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        tile = Tile.objects.get(pk=tile_id)
    except Tile.DoesNotExist:
        return Response({'error': 'Tile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # POST method: Get one task
    if request.method == "POST":    
        serializer = TaskSerializer(data={**request.data, 'tile': tile.id }) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == "GET":
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        elif request.method == "PUT":
            serializer = TaskSerializer(task, data={**request.data, 'id': task.id, 'tile': tile.id })
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == "DELETE":
            task.delete()        
            return Response(status=status.HTTP_204_NO_CONTENT)