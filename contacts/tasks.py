import string
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.db import models, connection, transaction
from django.http import HttpResponse
import os
import csv
import io

from celery import shared_task
from celery_progress.backend import ProgressRecorder
import time

@shared_task(bind=True)
def my_task(self, seconds):
    progress_recorder = ProgressRecorder(self)
    for i in range(seconds):
        time.sleep(1)
        progress_recorder.set_progress(i + 1, seconds)
    return 'done'


