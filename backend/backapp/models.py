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

