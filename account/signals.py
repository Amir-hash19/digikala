from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.dispatch import receiver
from .models import CustomUser



@receiver(post_save, sender=CustomUser)
def assign_user_group(sender, instance, created, **kwargs):
    if created:
        instance.groups.clear()

        if instance.user_type == "support":
            group, _ = Group.objects.get_or_create(name='Support')
        elif instance.user_type == "admin":
            group, _ = Group.objects.get_or_create(name='Admin')
        else:
            group, _ = Group.objects.get_or_create(name='Normal')

        instance.groups.add(group)            