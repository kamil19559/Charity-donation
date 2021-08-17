import null as null
from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=128)


class Institution(models.Model):
    institution_types = (
        ('fundacja', 'fundacja'),
        ('organizacja_pozarzadowa', 'organizacja_pozarzadowa'),
        ('zbiorka_lokalna', 'zbiorka_lokalna'),
    )

    name = models.CharField(max_length=256, null=True)
    description = models.TextField(null=True)
    type = models.CharField(max_length=64, null=True, default='fundacja', choices=institution_types)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=256, null=True)
    phone_number = models.CharField(max_length=32, null=True)
    city = models.CharField(max_length=128, null=True)
    zip_code = models.CharField(max_length=16, null=True)
    pick_up_date = models.DateField(null=True)
    pick_up_time = models.TimeField(null=True)
    pick_up_comment = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    is_taken = models.BooleanField(default=False)
