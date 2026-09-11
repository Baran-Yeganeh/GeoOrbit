# from django.shortcuts import render, redirect
# from apps.gnss.forms.mission_form import Mission_Form_1
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Mission
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.http import HttpResponse

def send_email(request):
    send_mail(
        subject='GeoOrbit Test Email.',
        message='this is just a test.',
        from_email=None,
        recipient_list=['Baran.yeganeh.1995@gmail.com'],
        fail_silently=False
        
    )
    return HttpResponse('Email sent successfully!')

# def mission_form_01(request):
    
#     if request.method == 'POST':
#         mission_form = Mission_Form_1(request.POST)
#         if mission_form.is_valid():
#             mission_form.save()    
#             return redirect('mission_list')
#     else:    
#         mission_form = Mission_Form_1()
            
#     context = {'form' : mission_form}
#     return render(request,'gnss/mission_form.html',context)

class MissionCreate(CreateView):
    model = Mission
    fields = '__all__'
    template_name = 'gnss/create_mission.html'
    success_url = reverse_lazy('mission_list')
    
class MissionList(ListView):
    model = Mission
    template_name = 'gnss/missions_list.html'

class MissionDetail(DetailView):
    model = Mission
    template_name = 'gnss/mission_detail.html'
    context_object_name = 'mission'    
    
class MissionUpdate(UpdateView):
    model = Mission
    fields = '__all__'
    template_name = 'gnss/mission_update.html'
    context_object_name = 'mission'       
    success_url = reverse_lazy('mission_list')
    
class MissionDelete(DeleteView):
    model = Mission
    template_name = 'gnss/mission_delete.html'
    context_object_name = 'mission'       
    success_url = reverse_lazy('mission_list')    
    
    
    
    
    