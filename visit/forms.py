from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

from .models import Student,Applicant,Security
from datetime import datetime

class SineUpForm(forms.ModelForm):
    class Meta:
        model=Applicant
        fields ="__all__"
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter Name', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'abc@xyz.com', 'class': 'form-control'}),
            'firstname': forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}),
            'lastname': forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}),
            'id_name': forms.TextInput(attrs={'placeholder': 'ID Name', 'class': 'form-control',"value":"Aadhar"}),
            'id_num': forms.TextInput(attrs={'placeholder': 'ID NO.', 'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'placeholder': 'Contact',"title":"Please Enter A Valid Contact Number", 'class': 'form-control', 'type': 'number', 'min': '999999999', 'max': '9999999999'}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter Address', 'class': 'form-control'}),
            'status': forms.TextInput(attrs={'type':'hidden', 'class': 'form-control'}),
            # 'photo': forms.FileInput(attrs={'class': 'form-control'}),
            # "role":forms.Choice(attrs={ 'class': 'form-control'}),
            # "role": forms.CharField(widget=forms.ChoiceField(choices=(("HR","HR"),("Security","Security")),attrs={'class': 'form-control'}))
        }

class SineUpForm1(forms.ModelForm):
    class Meta:
        model=Applicant
        fields ="__all__"
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter Name', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'abc@xyz.com', 'class': 'form-control'}),
            'firstname': forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}),
            'lastname': forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}),
            'id_name': forms.TextInput(attrs={'placeholder': 'ID Name', 'class': 'form-control',"value":"Aadhar"}),
            'id_num': forms.TextInput(attrs={'placeholder': 'ID NO.', 'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'placeholder': 'Contact', 'class': 'form-control',"title":"Please Enter A Valid Contact Number", 'type': 'number', 'min': '999999999', 'max': '9999999999'}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter Address', 'class': 'form-control'}),
            'status': forms.TextInput(attrs={'type':'hidden', 'class': 'form-control',"value":"Accepted"}),
            # 'photo': forms.FileInput(attrs={'class': 'form-control'}),
            # "role":forms.Choice(attrs={ 'class': 'form-control'}),
            # "role": forms.CharField(widget=forms.ChoiceField(choices=(("HR","HR"),("Security","Security")),attrs={'class': 'form-control'}))
        }

class StudentVisitForm(forms.ModelForm):
    
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Name', 'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'placeholder': 'Contact', 'class': 'form-control',"title":"Please Enter A Valid Contact Number", 'type': 'number', 'min': '999999999', 'max': '9999999999'}),
            'email': forms.EmailInput(attrs={'placeholder': 'abc@xyz.com', 'class': 'form-control'}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter Address', 'class': 'form-control'}),
            'college': forms.TextInput(attrs={'placeholder': 'College Name', 'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control','id':'datefield', 'type': 'date','name':'date'}),
            'from_time': forms.TimeInput(attrs={'class': 'form-control','id':'from_time', 'name':'from_time', 'type': 'time'},format = '%H:%M'),
            'to_time': forms.TimeInput(attrs={'class': 'form-control', 'id':'to_time','name':'to_time','type': 'time'},format = '%H:%M'),
            'purpose': forms.TextInput(attrs={'placeholder': 'eg: interview', 'class': 'form-control'}),
            
        }


class HrUpdateTimeForm(forms.ModelForm):
    
    class Meta:
        model = Student
        fields = ["from_time", "to_time"]
        widgets = {
            'from_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'},format = '%H:%M'),
            'to_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'},format = '%H:%M'),
        }

class SecurityTimeForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ["student_entry_time", "student_exit_time"]
        widgets = {
            'student_entry_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'},format = '%H:%M'),
            'student_exit_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'},format = '%H:%M'),
        }


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=15, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(max_length=15, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(max_length=15, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')
        labels = {'old password': 'Old Password',
                  'new password1': 'New Password',
                  'new password2': 'Confirm password'}
