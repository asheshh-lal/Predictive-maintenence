from django.db import models

# Create your models here.
class Dash(models.Model):
    # NP_Date = models.DateField()
    # Document = models.CharField(max_length=100)
    # Customer_Vendor = models.CharField(max_length=255)
    # Opening = models.IntegerField(default=0)  # Assuming default value is 0
    # Received = models.IntegerField(default=0)  # Assuming default value is 0
    # Delivered = models.IntegerField(default=0)  # Assuming default value is 0
    # Balance = models.IntegerField(default=0)  # Assuming default value is 0
    # Article = models.CharField(max_length=100)
    Type = models.CharField(max_length=255)
    Rotational_speed_rpm = models.IntegerField(default=0)
    Torque_Nm =  models.IntegerField(default=0)
    Tool_wear_min = models.IntegerField(default=0)
    Machine_failure = models.IntegerField(default=0)
    TWF = models.IntegerField(default=0)
    HDF = models.IntegerField(default=0)
    PWF = models.IntegerField(default=0)
    OSF = models.IntegerField(default=0)
    RNF = models.IntegerField(default=0)
    type_of_failure = models.CharField(max_length=255)
    Air_temperature = models.IntegerField(default=0)
    Process_temperature = models.IntegerField(default=0)
    # def __str__(self):
    #     return f'{self.Document} - {self.Article}'
    