from django.db import models

#Model creation in the database
class Toy(models.Model):
    id = models.BigAutoField(primary_key=True) 
    name = models.CharField(max_length = 100) 
    model = models.CharField(max_length=10, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    
