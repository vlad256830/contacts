from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


User = settings.AUTH_USER_MODEL

# Create your models here.
class Contact(models.Model):
    first_name = models.CharField(max_length=45)
    second_name = models.CharField(max_length=45)
    town = models.CharField(max_length=45, null=True)
    country = models.CharField(max_length=45, null=True)
    telephone = models.CharField(max_length=20)
    email = models.CharField(max_length=45)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False)
    created_at = models.DateTimeField(blank=True, auto_now_add=True)

    class Meta:
        db_table = 'contacts'

    
    def __str__(self):
        return '%s %s' % (self.first_name, self.second_name)

class Usersettings(models.Model):
    user = models.ForeignKey(User)   
    getvero_key = models.CharField(max_length=255)
    getvero_username = models.CharField(max_length=45)

    class Meta:
        db_table = 'usersettings'

    def __str__(self):
        return '%s %s %s' % (self.user, self.getvero_username, self.getvero_key)

    
    
        


