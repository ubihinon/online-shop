from django.db import models

from common.validators import phone_validator


class Order(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=6)
    phone_number = models.CharField(validators=[phone_validator], max_length=15, blank=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    products = models.ManyToManyField('products.Product', related_name='products')
