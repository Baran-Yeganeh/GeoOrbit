from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Mission, Receiver, SatelliteSystem, ProcessingReport
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (MissionSerializer, ReceiverSerializer,
                          SatelliteSystemSerializer, ProcessingReportSerializer)
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .permissions import MissionPermission



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
 
@api_view(['GET'])
@permission_classes([MissionPermission])
def mission_api_list(request):
    missions = Mission.objects.all()
    serializer = MissionSerializer(missions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([MissionPermission])

def mission_api_detail(request,pk):
    mission = get_object_or_404(Mission, pk=pk)
    serializer = MissionSerializer(mission)
    return Response(serializer.data)
    
class MissionApiCreate(APIView):
    permission_classes = [MissionPermission]
    def post(self,request):
        serializer = MissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class MissionApiDetail(RetrieveUpdateDestroyAPIView):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    permission_classes = [MissionPermission]


class ReceiverApiListCreate(APIView):
    permission_classes = [MissionPermission]

    def get(self, request):
        receivers = Receiver.objects.all()
        serializer = ReceiverSerializer(receivers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReceiverSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

class ReceiverApiDetail(RetrieveUpdateDestroyAPIView):
    queryset = Receiver.objects.all()
    serializer_class = ReceiverSerializer
    permission_classes = [MissionPermission]


class SatelliteSystemApiListCreate(APIView):
    permission_classes = [MissionPermission]

    def get(self, request):
        systems = SatelliteSystem.objects.all()
        serializer = SatelliteSystemSerializer(systems, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SatelliteSystemSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


class SatelliteSystemApiDetail(RetrieveUpdateDestroyAPIView):
    queryset = SatelliteSystem.objects.all()
    serializer_class = SatelliteSystemSerializer
    permission_classes = [MissionPermission]


class ProcessingReportApiListCreate(APIView):
    permission_classes = [MissionPermission]

    def get(self, request):
        reports = ProcessingReport.objects.all()
        serializer = ProcessingReportSerializer(reports, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProcessingReportSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


class ProcessingReportApiDetail(RetrieveUpdateDestroyAPIView):
    queryset = ProcessingReport.objects.all()
    serializer_class = ProcessingReportSerializer
    permission_classes = [MissionPermission]
