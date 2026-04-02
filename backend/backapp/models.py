from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
class EmberUser(models.Model):
    ROLES= (("user", "User"), ("ngo", "NGO"))
    cognito_sub=models.CharField(max_length=500, unique=True)
    role=models.CharField(max_length=20, choices=ROLES)
    phone=PhoneNumberField(region='IN', blank=True)
    location=models.CharField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.phone}->{self.role}"

class Shelter(models.Model):
    name=models.CharField(max_length=500)
    region=models.CharField(max_length=250)
    latitude=models.FloatField()
    longitude=models.FloatField()
    total_capac=models.IntegerField(default=100)
    occupied=models.IntegerField(default=0)
    is_active=models.BooleanField(default=True)
    @property
    def remaining(self):
        return self.total_capac-self.occupied
    
    def __str__(self):
        return f"{self.name}-{self.region}"

class NGOShelter(models.Model):
    user=models.OneToOneField(EmberUser, on_delete=models.CASCADE, related_name="ngo_profile")
    org_name=models.CharField(max_length=255)
    base_latitude=models.FloatField()
    base_longitude=models.FloatField()
    ambulances=models.IntegerField(default=0)
    food_pac=models.IntegerField(default=0)
    volunteers=models.IntegerField(default=0)
    def __str__(self):
        return self.org_name

class History(models.Model):
    LEVELS= ( ("LOW", "low"), ("MEDIUM", "medium"), ("HIGH", "high"))
    event_id=models.CharField(unique=True, max_length=100)
    region=models.CharField(max_length=250)
    risk=models.CharField(max_length=10,choices=LEVELS)
    latitude=models.FloatField()
    longitude=models.FloatField()
    timestamp=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.event_id}->{self.region}->{self.risk}"



