from django.db import models
from django.contrib.auth.models import User,AbstractUser

# Create your models here.
class User(AbstractUser):
    is_organizer = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
class Lead(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age   =  models.IntegerField(default=1)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    agent = models.ForeignKey("Agent", null=True, blank=True, on_delete=models.SET_NULL)
    # category = models.ForeignKey("Category", related_name="leads", null=True, blank=True, on_delete=models.SET_NULL)
    # description = models.TextField()
    # date_added = models.DateTimeField(auto_now_add=True)
    # phone_number = models.CharField(max_length=20)
    # email = models.EmailField()
    # profile_picture = models.ImageField(null=True, blank=True, upload_to="profile_pictures/")
    # converted_date = models.DateTimeField(null=True, blank=True)

class Agent(models.Model):
    user  = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)