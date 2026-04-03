from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
import uuid
class EmberUser(models.Model):
    ROLES= (("user", "User"), ("ngo", "NGO"))
    cognito_sub=models.CharField(max_length=500, unique=True)
    role=models.CharField(max_length=20, choices=ROLES, default="user")
    phone=PhoneNumberField(region='IN', blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.phone}->{self.role}"

class Shelter(models.Model):
    name=models.CharField(max_length=500)
    region=models.CharField(max_length=250, db_index=True)
    latitude=models.FloatField(null=True, blank=True)
    longitude=models.FloatField(null=True, blank=True)
    total_capac=models.IntegerField(default=100)
    occupied=models.IntegerField(default=0)
    is_active=models.BooleanField(default=True)
    @property
    def remaining(self):
        return max(self.total_capac-self.occupied, 0)
    
    def __str__(self):
        return f"{self.name}-{self.region}"

class NGOProfile(models.Model):
    user=models.OneToOneField(EmberUser, on_delete=models.CASCADE, related_name="ngo_profile")
    org_name=models.CharField(max_length=255)
    base_latitude=models.FloatField(null=True, blank=True)
    base_longitude=models.FloatField()
    ambulances=models.IntegerField(default=0)
    food_pac=models.IntegerField(default=0)
    volunteers=models.IntegerField(default=0)
    def __str__(self):
        return self.org_name

class History(models.Model):
    LEVELS= ( ("LOW", "low"), ("MEDIUM", "medium"), ("HIGH", "high"))
    event_id=models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    region=models.CharField(max_length=250)
    risk=models.CharField(max_length=10,choices=LEVELS, default="LOW")
    risk_score=models.FloatField(default=0.0)
    latitude=models.FloatField(null=True, blank=True)
    longitude=models.FloatField(null=True, blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.event_id}->{self.region}->{self.risk}"



