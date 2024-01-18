# from channels.staticfiles import StaticFilesConsumer
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
# channel_routing = {
#     # This makes Django serve static files from settings.STATIC_URL, similar
#     # to django.views.static.serve. This isn't ideal (not exactly production
#     # quality) but it works for a minimal example.
#     'http.request': StaticFilesConsumer(),
# }

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
})