from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Student(models.Model):
    user=models.ForeignKey(User,on_delete=models.PROTECT)
    name=models.CharField(max_length=255)
    email=models.EmailField(max_length=255,unique=True)
    education=models.CharField(max_length=255)
    course=models.CharField(max_length=255)
    admission_date=models.DateField(auto_now_add=True)
    paid_fee=models.DecimalField(max_digits=7,decimal_places=2)
    total_fee=models.DecimalField(max_digits=7,decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        db_table='student'

