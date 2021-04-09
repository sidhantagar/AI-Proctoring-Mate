from django.db import models
from django.contrib.auth.models import User


# Creating a Temporary Model for User Details
class UserDetails(models.Model):

    details = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(null=True,blank=False,max_length = 50)
    last_name = models.CharField(null=True,blank=False,max_length = 50)
    username = models.CharField(max_length = 40,blank = False,null = True,unique = True)
    email = models.EmailField(max_length = 40)

    def __str__(self):
        return self.details.username

    class Meta:
        verbose_name = 'User Detail'
        verbose_name_plural = 'User Details'
