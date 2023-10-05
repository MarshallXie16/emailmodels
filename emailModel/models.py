from django.db import models
import uuid
from datetime import datetime, timedelta

# Represents a user, who is initially inactive
class User(models.Model):

    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)

    # future additions:
    # date registered (models.DateField)

# Represents a randomly generated token, mapped to a user
class EmailVerificationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    expiration = models.DateTimeField(default=datetime.now() + timedelta(days=1))
