from django.contrib.auth.models import User
from django import forms
from django.db import models
from django.forms import fields
from .models import Appoinment, Consultation


class UserForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class AppoinmentForm(forms.ModelForm):
    class Meta:
        model = Appoinment
        fields = ['date', 'patient_name', 'doctor',
                  'time', 'file_number', 'is_doctor']


class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['consultation_number', 'doctor_name',
                  'patient_name', 'file_number', 'is_doctor']
