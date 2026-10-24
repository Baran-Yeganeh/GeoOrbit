from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView,
                                  ListView, UpdateView)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import MissionForm
from .models import Mission, ProcessingReport, Receiver, SatelliteSystem
from .permissions import MissionPermission
from .serializers import (MissionSerializer, ProcessingReportSerializer,
                          ReceiverSerializer, SatelliteSystemSerializer)


# --------------------------------------------------------------------------
# Web views (HTML)
# --------------------------------------------------------------------------

class MissionList(ListView):
    model = Mission
    template_name = 'gnss/missions_list.html'

    def get_queryset(self):
        # select_related / prefetch_related avoid one extra query per card.
        return (
            Mission.objects
            .select_related('receiver')
            .prefetch_related('satellite_systems')
            .order_by('-surveying_start_date', 'project_name')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_mission_id'] = self.request.session.get('last_mission_id')
        return context


class MissionDetail(DetailView):
    model = Mission
    template_name = 'gnss/mission_detail.html'
    context_object_name = 'mission'

    def get_queryset(self):
        return (
            Mission.objects
            .select_related('receiver', 'processing_report')
            .prefetch_related('satellite_systems')
        )

    def get_object(self, queryset=None):
        mission = super().get_object(queryset)
        self.request.session['last_mission_id'] = mission.pk
        return mission


class MissionCreate(LoginRequiredMixin, CreateView):
    model = Mission
    form_class = MissionForm
    template_name = 'gnss/create_mission.html'
    success_url = reverse_lazy('mission_list')


class MissionUpdate(LoginRequiredMixin, UpdateView):
    model = Mission
    form_class = MissionForm
    template_name = 'gnss/mission_update.html'
    context_object_name = 'mission'
    success_url = reverse_lazy('mission_list')


class MissionDelete(LoginRequiredMixin, DeleteView):
    model = Mission
    template_name = 'gnss/mission_delete.html'
    context_object_name = 'mission'
    success_url = reverse_lazy('mission_list')


def mission_search(request):
    """JSON endpoint used by the live search box in the navbar."""
    query = request.GET.get('name', '').strip()
    if not query:
        return JsonResponse({'mission': []})

    missions = (
        Mission.objects
        .filter(Q(project_name__icontains=query) | Q(project_location__icontains=query))
        .order_by('project_name')[:8]
    )
    return JsonResponse({
        'mission': [{'id': m.pk, 'name': m.project_name} for m in missions]
    })


# --------------------------------------------------------------------------
# REST API
# --------------------------------------------------------------------------

@api_view(['GET'])
@permission_classes([MissionPermission])
def mission_api_list(request):
    missions = Mission.objects.all()
    serializer = MissionSerializer(missions, many=True)
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
