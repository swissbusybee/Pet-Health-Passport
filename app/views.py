from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
from django.http import HttpResponse
from django.db.models import Q
from .models import FamilyGroup, Profile, Vaccine, Immunization

def index(request):
    return render(request, 'app/index.html')

def about(request):
    return render(request, 'app/about.html')

def contact(request):
    return render(request, 'app/contact.html')

class SignUpView(generic.CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    success_message = "You have signed up successfully"

class FamilyGroupListView(LoginRequiredMixin, generic.ListView):
    model = FamilyGroup
    # def get_queryset(self):
    #     return FamilyGroup.objects.filter(owner=self.kwargs['pk'])
    # def get_queryset(self):
    #     if request.user.is_superuser:
    #         queryset = FamilyGroup.objects.all()
    #     else:
    #         try:
    #             queryset = FamilyGroup.objects.filter(owner=request.user.id)
    #         except:
    #             queryset = Change.objects.none()
    #     return queryset
    # def get_queryset(self, *args, **kwargs):
    #  return Snippet.objects.all().filter(owner=self.request.user)

class FamilyGroupDetailView(LoginRequiredMixin, generic.DetailView):
    model = FamilyGroup

class FamilyGroupCreate(LoginRequiredMixin, CreateView):
    model = FamilyGroup
    template_name_suffix = '_create_form'
    fields = ['family_group_name']

class FamilyGroupUpdate(LoginRequiredMixin, UpdateView):
    model = FamilyGroup
    template_name_suffix = '_update_form'
    fields = ['family_group_name']

class FamilyGroupDelete(LoginRequiredMixin, DeleteView):
    model = FamilyGroup
    template_name_suffix = '_delete_form'
    success_url = reverse_lazy('familygroups')

class ProfileListView(LoginRequiredMixin, generic.ListView):
    model = Profile

class ProfileDetailView(LoginRequiredMixin, generic.DetailView):
    model = Profile

class ProfileCreate(LoginRequiredMixin, CreateView):
    model = Profile
    template_name_suffix = '_create_form'
    fields = ['familygroup','pet_name', 'pet_microchip_id', 'date_of_birth', 'doctor_name_contact','family_member_type']
    success_url = "/familygroup/{familygroup_id}"

class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name_suffix = '_update_form'
    fields = ['familygroup','pet_name', 'pet_microchip_id', 'date_of_birth', 'doctor_name_contact','family_member_type']
    success_url = "/familygroup/{familygroup_id}"

class ProfileDelete(LoginRequiredMixin, DeleteView):
    model = Profile
    template_name_suffix = '_delete_form'
    success_url = "/familygroup/{familygroup_id}"

class VaccineListView(LoginRequiredMixin, generic.ListView):
    model = Vaccine
    
    def get_queryset(self):
        val = self.request.GET.get("q")
        if val:
            vaccine_list = Vaccine.objects.filter(
                Q(vaccine_name__icontains=val) |
                Q(disease_type__icontains=val) 
                ).distinct()
        else:
            vaccine_list = Vaccine.objects.all()
        return vaccine_list

class VaccineDetailView(LoginRequiredMixin, generic.DetailView):
    model = Vaccine

class VaccineCreate(LoginRequiredMixin, CreateView):
    model = Vaccine
    template_name_suffix = '_create_form'
    fields = ['vaccine_name', 'disease_type', 'required_doses']
    success_url = reverse_lazy('vaccines')

class VaccineUpdate(LoginRequiredMixin, UpdateView):
    model = Vaccine
    template_name_suffix = '_update_form'
    fields = ['vaccine_name', 'disease_type', 'required_doses']
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
    fields = ['vaccine', 'profile', 'expired_by', 'date_administered', 'administered_by']
    success_url = "/profile/{profile_id}"

class ImmunizationUpdate(LoginRequiredMixin, UpdateView):
    model = Immunization
    template_name_suffix = '_update_form'
    fields = ['vaccine', 'profile', 'expired_by', 'date_administered', 'administered_by']
    success_url = "/profile/{profile_id}"

class ImmunizationDelete(LoginRequiredMixin, DeleteView):
    model = Immunization
    template_name_suffix = '_delete_form'
    success_url = "/profile/{profile_id}"
