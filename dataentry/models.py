from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Student(models.Model):
    roll_no = models.IntegerField()
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self) -> str:
        return self.name
    
class Customer(models.Model):
    phone = models.IntegerField(
        validators=[
            MinValueValidator(1000000000),  # Minimum value of 10 digits
            MaxValueValidator(9999999999)   # Maximum value of 10 digits
        ]
    )
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self) -> str:
        return self.name
    
class Employee(models.Model):
    employee_id = models.IntegerField(primary_key=True)
    employee_name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    retirement = models.DecimalField(max_digits=10, decimal_places=2)
    other_benefits = models.DecimalField(max_digits=10, decimal_places=2)
    total_benefits = models.DecimalField(max_digits=10, decimal_places=2)
    total_compensation = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return self.employee_name