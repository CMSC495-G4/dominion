from django.urls import path
from . import consumers

websocket_urlpatterns = [
  path('api/game/<id>/', consumers.GameConsumer),
]