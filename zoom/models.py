from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    department_name = models.CharField(max_length=255)

    def __str__(self):
        return self.department_name
# Create your models here.
# models.py


class LeaveType(models.Model):
    name = models.CharField(max_length=255,default="")

    def __str__(self):
        return self.name
class Employee(models.Model):
    empId = models.CharField(max_length=255)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    dob = models.DateField()
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    joiningDate = models.DateField()
    photo = models.ImageField(upload_to='employee_photos/', blank=True, null=True)
    address = models.TextField()

class Leave(models.Model):
    leave_type_choices = [
        ('vacation', 'Vacation'),
        ('sick', 'Sick Leave'),
        ('personal', 'Personal Leave'),
        # Add more choices as needed
    ]

    status_choices = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    leave_type = models.CharField(max_length=20, choices=leave_type_choices)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=status_choices, default='pending')