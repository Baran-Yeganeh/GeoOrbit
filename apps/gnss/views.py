# from django.shortcuts import render, redirect
# from apps.gnss.forms.mission_form import Mission_Form_1
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Mission
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse

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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_mission_id = self.request.session.get('last_mission_id')
        context['last_mission_id'] = last_mission_id
        return context

class MissionDetail(DetailView):
    model = Mission
    template_name = 'gnss/mission_detail.html'
    context_object_name = 'mission' 
    
    def get_object(self, queryset = None):
        mission = super().get_object(queryset)
        self.request.session['last_mission_id'] = mission.pk  
        return mission
     
    
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
    
    
def test_java(request):
    data = request.GET.get('name')
    missions = Mission.objects.filter( project_name__icontains = data )
    mission_list = []
    for mission in missions:
        mission_list.append({
            'name': mission.project_name,
            'id': mission.id
            })
        
    
    
    context = { 'mission': mission_list }
    return JsonResponse(context)   
 
    
    