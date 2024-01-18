import os
import logging
import worker
from django.conf import settings
from celery.schedules import crontab
logger = logging.getLogger(__name__)
from celery import shared_task
import os
import json
app = worker.app
