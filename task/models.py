from django.db import models


# Create your models here.
class Checkpoint(models.Model):
    location_name = models.CharField(max_length=128, blank=False, null=False)
    latitude = models.FloatField(blank=False, null=False)
    longitude = models.FloatField(blank=False, null=False)
    min_number = models.IntegerField(blank=False, null=False)


class User(models.Model):
    email = models.EmailField(max_length=50, blank=False, null=False)
    user_name = models.CharField(max_length=50, blank=False, null=False)
    password = models.CharField(max_length=50, blank=False, null=False)
    trusted = models.BooleanField(blank=False, null=False)


class Claim(models.Model):
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE,
                             related_name="claim_user_id")
    checkpoint = models.ForeignKey(Checkpoint, blank=False, null=False, on_delete=models.CASCADE,
                                   related_name="claim_checkpoint_id")
    state = models.BooleanField(blank=False, null=False)
    timestamp = models.BigIntegerField(blank=False, null=False)


class SubscribedPoints(models.Model):
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE,
                             related_name="subscribed_user_id")
    checkpoint = models.ForeignKey(Checkpoint, blank=False, null=False, on_delete=models.CASCADE,
                                   related_name="subscribed_checkpoint_id")
