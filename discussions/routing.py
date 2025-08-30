from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/discussions/(?P<circle_id>\d+)/$", consumers.ChatConsumer.as_asgi()),
]
