from django.db.models.signals import post_save
# from notifications import notify
from django.dispatch import receiver

from .models import Student

# @receiver(post_save, sender=Student)
# def my_handler(sender, instance, created, **kwargs):
#     notify.send(instance, verb='was saved')

