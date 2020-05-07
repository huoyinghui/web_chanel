#!/usr/bin/env python
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import mychat.routing


application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            mychat.routing.websocket_urlpatterns
        )
    ),
})


def main():
    pass


if __name__ == '__main__':
    main()
