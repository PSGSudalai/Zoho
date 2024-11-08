from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='home'),
    path('add/lead/', views.add_lead, name='add-lead'),
    path('lead/list/',views.all_lead,name='lead'),
    path('lead/edit/<int:lead_id>/', views.edit_lead, name='edit-lead'),
    path('delete/lead/<int:pk>/',views.delete_lead,name='delete-lead'),
    path('add-status/', views.add_status, name='add_status'),

]
