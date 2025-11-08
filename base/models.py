from django.db import models
from django.utils import timezone

class GymPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    duration = models.IntegerField(help_text="Duration in days")

    def __str__(self):
        return self.name



from django.db import models

class Member(models.Model):
    MEMBERSHIP_CHOICES = [
        ('IRON', 'IRON'),
        ('PLATINUM', 'PLATINUM'),
        ('GOLD', 'GOLD'),
    ]

    TIME_CHOICES = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=128)
    membership = models.CharField(max_length=10, choices=MEMBERSHIP_CHOICES)
    preferred_time = models.CharField(max_length=10, choices=TIME_CHOICES)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    payment_confirmed = models.BooleanField(default=False)
    admin_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def end_date(self):
        if self.start_date and self.membership:
            duration_map = {'GOLD': 28, 'PLATINUM': 30, 'IRON': 35}
            return self.start_date + timezone.timedelta(days=duration_map.get(self.membership, 0))
        return None



class SupportMessage(models.Model):
    member = models.ForeignKey('Member', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    admin_reply = models.TextField(blank=True, null=True)
    replied_at = models.DateTimeField(blank=True, null=True)


class Trainer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    experience = models.IntegerField(default=0, help_text="Years of experience")

    is_approved = models.BooleanField(default=False, help_text="Approved by admin?")

    def __str__(self):
        return self.name


