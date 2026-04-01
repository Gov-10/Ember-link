from django.urls import re_path
from .consumers import FloodConsumer

websocket_urlpatterns = [
    re_path(r"ws/flood/(?P<region>\w+)/$", FloodConsumer.as_asgi()),
]
