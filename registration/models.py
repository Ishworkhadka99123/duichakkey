from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

CITY_CHOICES = (
    ('Kathmandu', 'Kathmandu'),
    )

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer', null=False, blank=False)
    full_name = models.CharField(max_length=100)
    city = models.CharField(choices=CITY_CHOICES, max_length=100, default='Kathmandu')
    address = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    phone_no = models.PositiveBigIntegerField()
    house_no = models.PositiveIntegerField()
    zip_code = models.PositiveIntegerField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.full_name