from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=30)
    isAdmin = models.BooleanField(default=False)
    username = models.EmailField(unique=True)

    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        
        self.isAdmin = self.isAdmin or self.is_superuser
        super(User, self).save(*args, **kwargs)

    # groups = models.ManyToManyField(
    #     'auth.Group',
    #     related_name='custom_user_set',
    #     blank=True,
    #     help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    # )

    # user_permissions = models.ManyToManyField(
    #     'auth.Permission',
    #     related_name='custom_user_set',
    #     blank=True,
    #     help_text='Specific permissions for this user.',
    # )

class Bus(models.Model):
    busId = models.AutoField(primary_key=True)
    busNumber = models.CharField(max_length=100,unique=True)
    totalSeats = models.PositiveIntegerField()

class Schedule(models.Model):
    scheduleId = models.AutoField(primary_key=True)
    busId = models.ForeignKey(Bus, on_delete=models.CASCADE)
    availableSeats = models.PositiveIntegerField()
    BookingStart = models.DateTimeField()  
    BookingEnd = models.DateTimeField()    
    departure = models.DateTimeField()


class Booking(models.Model):
    bookingId = models.AutoField(primary_key=True)
    scheduleId = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    id = models.ForeignKey(User, on_delete=models.CASCADE)
    bookingTime = models.DateTimeField(auto_now_add=True)




