from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('familygroups/', views.FamilyGroupListView.as_view(), name='familygroups'),  
    path('familygroup/<int:pk>', views.FamilyGroupDetailView.as_view(), name='familygroup-detail'),
    path('familygroup/add/', views.FamilyGroupCreate.as_view(), name='familygroup-add'),
    path('familygroup/<int:pk>/', views.FamilyGroupUpdate.as_view(), name='familygroup-update'),
    path('familygroup/<int:pk>/delete/', views.FamilyGroupDelete.as_view(), name='familygroup-delete'),
    path('profiles/', views.ProfileListView.as_view(), name='profiles'),  
    path('profile/<int:pk>', views.ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/add/', views.ProfileCreate.as_view(), name='profile-add'),
    path('profile/<int:pk>/', views.ProfileUpdate.as_view(), name='profile-update'),
    path('profile/<int:pk>/delete/', views.ProfileDelete.as_view(), name='profile-delete'),
    path('vaccines/', views.VaccineListView.as_view(), name='vaccines'),  
    path('vaccine/<int:pk>', views.VaccineDetailView.as_view(), name='vaccine-detail'), 
    path('vaccine/add/', views.VaccineCreate.as_view(), name='vaccine-add'),
    path('vaccine/<int:pk>/', views.VaccineUpdate.as_view(), name='vaccine-update'),
    path('vaccine/<int:pk>/delete/', views.VaccineDelete.as_view(), name='vaccine-delete'), 
    path('immunizations/', views.ImmunizationListView.as_view(), name='immunizations'),  
    path('immunization/<int:pk>', views.ImmunizationDetailView.as_view(), name='immunization-detail'),
    path('immunization/add/', views.ImmunizationCreate.as_view(), name='immunization-add'),
    path('immunization/<int:pk>/', views.ImmunizationUpdate.as_view(), name='immunization-update'),
    path('immunization/<int:pk>/delete/', views.ImmunizationDelete.as_view(), name='immunization-delete'),    
]