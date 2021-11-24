from django.db import models
from django.contrib.auth.models import AbstractUser, User

from .validators import validate_file_extension, content_file_name,Applicant_photo
from datetime import *
from django.db.models import DO_NOTHING

# Create your models here.

# class User(AbstractUser):
#     is_security = models.CharField(max_length=20) 




class Student(models.Model):

    name = models.CharField(max_length=150, null=True)
    contact = models.PositiveIntegerField(null=True)
    email = models.EmailField(max_length=150, null=True)
    address = models.CharField(max_length=250, null=True)
    college = models.CharField(max_length=250, null=True)
    photo = models.ImageField(upload_to = content_file_name, validators = [validate_file_extension], null=True)
    date = models.DateField(null=True, default=date.today)
    from_time = models.TimeField(null=False, default=datetime.now())
    to_time = models.TimeField(null=False)
    purpose = models.CharField(max_length=150, null=True)
    status = models.CharField(max_length=20,default="pending")
    # student_entry_time=models.CharField(null=True,default="",max_length=20,blank=True)
    # student_exit_time=models.CharField(null=True,default="",max_length=20,blank=True)
    student_entry_time = models.TimeField(null=True,default=None,blank=True)
    student_exit_time = models.TimeField(null=True,default=None,blank=True)


    def __str__(self):
        return self.name


class Applicant(models.Model):
    username=models.CharField(max_length=150,unique = True)
    email=models.EmailField(max_length=150,unique = True)
    firstname=models.CharField(max_length=150)
    lastname=models.CharField(max_length=150)
    id_name=models.CharField(max_length=150)
    id_num=models.CharField(max_length=150)
    contact=models.CharField(max_length=150,unique = True)
    address=models.CharField(max_length=150)
    role=models.CharField(max_length=20,choices=(("HR","HR"),("Security","Security")))
    
    # photo = models.ImageField(upload_to=Applicant_photo)
    status = models.CharField(max_length=20,default="pending")
    def __str__(self):
        return self.username

class Security(models.Model):
    security_user = models.ForeignKey(User,on_delete=DO_NOTHING)
    student_id = models.ForeignKey(Student,on_delete=DO_NOTHING)
    class Meta:
     permissions = (
           ("is_Security", "Can edit the entry time of a student or employee"),
     )
class HR(models.Model):
    hr_user=models.ForeignKey(User,on_delete=DO_NOTHING)
    class Meta:
         permissions = (
           ("is_hr", "Can edit the meeting time of a visitor"),
     )
