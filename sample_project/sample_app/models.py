from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    top_name = models.CharField(max_length=264, unique=True)

    def __str__(self):
        return self.top_name

class Webpage(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.DO_NOTHING) #Newer version of Django requires on_delete in this constructor
    name = models.CharField(max_length=264, unique=True)
    url = models.URLField(unique=True)

    def __str__(self):
        return self.name

class AccessRecord(models.Model):
    name = models.ForeignKey(Webpage, on_delete=models.DO_NOTHING)
    date = models.DateField()

    def __str__(self):
        return str(self.date)

#sample_app's User (not admin's User)
class WebUser(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(max_length=264, unique=True)
    DoB = models.DateField(default=datetime.now, blank=False)
    notes = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

class UserProfileInfo(models.Model):
    #Exending the User class WITHOUT inheriting User class
    #because this is NOT another User instance.
    #In OOP design this is one-to-one composition
    #https://docs.djangoproject.com/en/4.0/topics/db/examples/one_to_one/
    #and instances of the two classes can actually refer to each other
    #E.g.:
    #up = UserProfileInf(user = some_user)
    #some_user.userprofileinfo is now referencing up as well.
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)

    # additional members outside of User
    portfolio_site = models.URLField(blank=True)
    # note that profile_pics is a folder under media
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.user.username
