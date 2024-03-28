# import_data.py
import csv
from datetime import datetime
from itertools import islice
from django.conf import settings
from django.core.management.base import BaseCommand
from app.models import Dash


class Command(BaseCommand):
    help = 'Load data from file'
    
    def handle(self, *args, **kwargs):
        datafile = settings.BASE_DIR / 'Data' / 'data_for_eda.csv'
        
        with open(datafile, 'r') as csvfile:
            reader = csv.DictReader(islice(csvfile, 0, None))
            
            for row in reader:
                # # Preprocess other fields
                # Document = row['Document']
                # Customer_Vendor = row['Customer_Vendor']
                # Opening = float(row['Opening'])
                # Received = float(row['Received'])
                # Delivered = float(row['Delivered'])
                # Balance = float(row['Balance'])
                # Article = row['article']
                Type = row['Type']
                Rotational_speed_rpm = row['Rotational speed [rpm]']
                Torque_Nm = row['Torque [Nm]']
                Tool_wear_min = row['Tool wear [min]']
                Machine_failure = row['Machine failure']
                TWF = row['TWF']
                HDF = row['HDF']
                PWF = row['PWF']
                OSF = row['OSF']
                RNF = row['RNF']
                type_of_failure = row['type_of_failure']
                Air_temperature = row['Air temperature [°C]']
                Process_temperature = row['Process temperature [°C]']


                # Create Dash object with processed values
                Dash.objects.create(
                    # NP_Date=NP_Date,
                    # Document=Document,
                    # Customer_Vendor=Customer_Vendor,
                    # Opening=Opening,
                    # Received=Received,
                    # Delivered=Delivered,
                    # Balance=Balance,
                    # Article=Article
                    Type = Type,
                    Rotational_speed_rpm = Rotational_speed_rpm,
                    Torque_Nm = Torque_Nm,
                    Tool_wear_min = Tool_wear_min,
                    Machine_failure = Machine_failure,
                    TWF = TWF,
                    HDF = HDF,
                    PWF = PWF,
                    OSF = OSF,
                    RNF = RNF,
                    type_of_failure = type_of_failure,
                    Air_temperature = Air_temperature,
                    Process_temperature = Process_temperature,
                    
                    
                )
