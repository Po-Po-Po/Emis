from django.conf import settings
from .templatetags.user_tags import get


# class MiddlewareUpdateSystem(object):
#
#     def process_request(self, request):
#
#         update = {
#             'status': settings_update.status,
#             'send_email': settings_update.send_email,
#             'message': settings_update.message
#         }
#         request.__dict__['update'] = update