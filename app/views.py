from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
from .forms import UserChangeForm
from django.http import HttpResponse
from django.db.models import Q
from .models import Profile, Vaccine, Immunization
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

def index(request):
    return render(request, 'app/index.html')

def about(request):
    return render(request, 'app/about.html')

def contact(request):
    return render(request, 'app/contact.html')

def sendmail(request):
    subject = 'Hello from Health Passport'
    message = 'Hello there, This is an automated message.'
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [request.user.email], fail_silently=False)
    messages.success(request, "Email has been sent. Please check your mail. Thank You!", extra_tags='alert')
    # return HttpResponse("Mail has been sent. Please check your mail. Thank YOU!")
    return redirect('profiles')

@login_required
def edituser(request):
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated", extra_tags='alert')
            return redirect('/')
    else:
        form = UserChangeForm(instance=request.user)
    context = {'form': form}
    return render(request, 'registration/edit_user.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!', extra_tags='alert')
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.', extra_tags='alert')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })

class SignUpView(generic.CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    success_message = "You have signed up successfully"

class ProfileListView(LoginRequiredMixin, generic.ListView):
    model = Profile
    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Profile.objects.all()
        else:
            try:
                queryset = Profile.objects.all().filter(owner=self.request.user)
            except:
                queryset = Change.objects.none()
        return queryset

class ProfileDetailView(LoginRequiredMixin, generic.DetailView):
    model = Profile

class ProfileCreate(LoginRequiredMixin, CreateView):
    model = Profile
    template_name_suffix = '_create_form'
    fields = ['family_name','pet_name','pet_microchip_id', 'date_of_birth', 'doctor_name_contact','family_member_type']
    success_url = reverse_lazy('profiles')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name_suffix = '_update_form'
    fields = ['pet_name', 'pet_microchip_id', 'date_of_birth', 'doctor_name_contact','family_member_type']
    success_url = reverse_lazy('profiles')

class ProfileDelete(LoginRequiredMixin, DeleteView):
    model = Profile
    template_name_suffix = '_delete_form'
    success_url = reverse_lazy('profiles')

class VaccineListView(LoginRequiredMixin, generic.ListView):
    model = Vaccine
    
class VaccineDetailView(LoginRequiredMixin, generic.DetailView):
    model = Vaccine

class VaccineCreate(LoginRequiredMixin, CreateView):
    model = Vaccine
    template_name_suffix = '_create_form'
    fields = ['vaccine_name']
    success_url = reverse_lazy('vaccines')

class VaccineUpdate(LoginRequiredMixin, UpdateView):
    model = Vaccine
    template_name_suffix = '_update_form'
    fields = ['vaccine_name']
    success_url = reverse_lazy('vaccines')

class VaccineDelete(LoginRequiredMixin, DeleteView):
    model = Vaccine
    template_name_suffix = '_delete_form'
    success_url = reverse_lazy('vaccines')

class ImmunizationListView(LoginRequiredMixin, generic.ListView):
    model = Immunization

class ImmunizationDetailView(LoginRequiredMixin, generic.DetailView):
    model = Immunization
 
class ImmunizationCreate(LoginRequiredMixin, CreateView):
    model = Immunization
    template_name_suffix = '_create_form'
    fields = ['profile', 'vaccine', 'expired_by', 'date_administered', 'administered_by']
    success_url = "/profile/{profile_id}"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ImmunizationUpdate(LoginRequiredMixin, UpdateView):
    model = Immunization
    template_name_suffix = '_update_form'
    fields = ['vaccine', 'expired_by', 'date_administered', 'administered_by']
    success_url = "/profile/{profile_id}"

class ImmunizationDelete(LoginRequiredMixin, DeleteView):
    model = Immunization
    template_name_suffix = '_delete_form'
    success_url = "/profile/{profile_id}"
