from django.db import models
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from datetime import date
from django.contrib.auth.models import User

class Vaccine(models.Model):
    DISEASE_TYPE_CHOICES = [('Diptheria', 'Diptheria'),('Hepatitis B', 'Hepatitis B'),('Haemophilus influenzae type b', 'Haemophilus influenzae type b'),('Human papillomavirus', 'Human papillomavirus'), ('Seasonal influenza', 'Seasonal influenza'), ('Measles', 'Measles'), ('Mumps', 'Mumps'), ('Pertussis (Whooping Cough)', 'Pertussis (Whooping Cough)'), ('Rubella', 'Rubella'), ('Pneumococcal disease', 'Pneumococcal disease'), ('Poliomyelitis (Polio)', 'Poliomyelitis (Polio)'), ('Rotavirus', 'Rotavirus'), ('Tetanus', 'Tetanus'), ('Tuberculosis (TB)', 'Tuberculosis (TB)'), ('Varicella', 'Varicella')] 
    vaccine_name = models.CharField(max_length=200)
    disease_type = models.CharField(max_length=200, choices=DISEASE_TYPE_CHOICES, blank=True)
    required_doses = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def get_absolute_url(self):
        return reverse('vaccine-detail', args=[str(self.id)])

    def __str__(self):
        return self.vaccine_name

class Profile(models.Model):
    MEMBER_CHOICES = [('Dog', 'Dog'),('Cat', 'Cat'),('Other', 'Other')]
    family_name = models.CharField(max_length=200)
    pet_name = models.CharField(max_length=200)
    pet_microchip_id = models.CharField(max_length=200)
    date_of_birth = models.DateField(default=None)
    doctor_name_contact = models.CharField(max_length=200, blank=True)
    family_member_type = models.CharField(max_length=200, choices=MEMBER_CHOICES, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    owner = models.ForeignKey(User, null=True, blank=True, editable=False, on_delete=models.CASCADE)
    
    def get_absolute_url(self):
        return reverse('profile-detail', args=[str(self.id)])

    def __str__(self):
        return self.pet_name

    def calculate_age(self):
        today = date.today()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age
        
class Immunization(models.Model):
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE, blank=True, null=True) 
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)    
    expired_by = models.DateField(null=True, blank=True)
    date_administered = models.DateField(null=True, blank=True)
    administered_by = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    owner = models.ForeignKey(User, null=True, blank=True, editable=False, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('immunization-detail', args=[str(self.id)])

    def __str__(self):
        return self.vaccine.vaccine_name 

    def vaccine_expired(self):
        return self.expired_by < datetime.now().date()

