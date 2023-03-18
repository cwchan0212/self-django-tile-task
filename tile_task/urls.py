from django.urls import path, include
from . import views
from .views import TileViewSet, TaskViewSet
from rest_framework import routers, permissions
from rest_framework.urlpatterns import format_suffix_patterns
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# =================================================================================================
# Schema View for API doc
#
schema_view = get_schema_view(
    openapi.Info(
        title="Tile-Task",
        default_version='v1',
        description="Tile-Task API description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# -------------------------------------------------------------------------------------------------
# Set the "Viewsets" router of Django REST Framework
router = routers.DefaultRouter()
router.register(r'tiles', TileViewSet)
router.register(r'tasks', TaskViewSet)

# Set urlpatterns to the "Viewsets" routers and "Views"
urlpatterns = [
    # Viewsets
    path('', include(router.urls)),
    # Views
    path("v2/tiles", views.tiles_all),
    path("v2/tile", views.tile_one),
    path("v2/tile/<int:tile_id>", views.tile_one),
    path("v2/tasks", views.tasks_all),
    path("v2/tile/<int:tile_id>/task", views.task_one),
    path("v2/tile/<int:tile_id>/task/<int:task_id>", views.task_one),
    # Schema for API doc
    path('swagger(<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

# urlpatterns = format_suffix_patterns(urlpatterns)
# =================================================================================================
