from django.db import models

# Create your models here.
class Dash(models.Model):
    Type = models.CharField(max_length=255)
    Rotational_speed_rpm = models.IntegerField(default=0)
    Torque_Nm = models.FloatField(default=0)  # Change to FloatField
    Tool_wear_min = models.IntegerField(default=0)
    Machine_failure = models.IntegerField(default=0)
    TWF = models.IntegerField(default=0)
    HDF = models.IntegerField(default=0)
    PWF = models.IntegerField(default=0)
    OSF = models.IntegerField(default=0)
    RNF = models.IntegerField(default=0)
    type_of_failure = models.CharField(max_length=255)
    Air_temperature =  models.FloatField(default=0)
    Process_temperature =  models.FloatField(default=0)
    

    
    # def __str__(self):
    #     return f'{self.Document} - {self.Article}'
    