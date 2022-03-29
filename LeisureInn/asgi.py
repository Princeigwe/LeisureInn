"""
ASGI config for LeisureInn project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
# import django
# django.setup()

from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()  # comment this if it doesn't work

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

# import chat.routing
import guest_chatRoom.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LeisureInn.settings')

#application = get_asgi_application()


# routing configuration setting...
"""if the url requested contains ws:// or wss://, it will beauthenticated to
check if it matches with those in the URLRoute"""
application = ProtocolTypeRouter({
    # "http": get_asgi_application(), # uncomment this if it doesn't work'
    "http": django_asgi_app, # comment this if it doesn't work'
    "websocket": AuthMiddlewareStack(
        URLRouter(
            guest_chatRoom.routing.websocket_urlpatterns # importing websocket urls from guest_chatRoom
        )
    )
})