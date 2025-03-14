from django.db import models
from django.contrib.auth import get_user_model

class Order(models.Model):
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')])
    customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, limit_choices_to={'role': 'customer'})
