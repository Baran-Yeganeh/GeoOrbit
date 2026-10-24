from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token





urlpatterns = [
    # path('form/', views.mission_form_01,name="mission_form"),
    path('missionslist/',views.MissionList.as_view(),name="mission_list"),
    path('missiondetail/<int:pk>/',views.MissionDetail.as_view(),name="mission_detail"),
    path('new/',views.MissionCreate.as_view(),name="mission_create"),
    path('missionedit/<int:pk>/',views.MissionUpdate.as_view(),name="mission_edit"),
    path('missiondelete/<int:pk>/',views.MissionDelete.as_view(),name="mission_delete"),
    path('search/', views.mission_search, name='mission_search'),
    path('api/missions/',views.mission_api_list,name='mission_api_list'),
    path('api/mission/<int:pk>/',views.MissionApiDetail.as_view(),name='mission_api_detail'),
    path('api/mission/create/',views.MissionApiCreate.as_view(),name='mission_api_create'),
    path('api/token/',obtain_auth_token,name='obtain_auth_token'),
    path('api/receivers/',views.ReceiverApiListCreate.as_view(),name='receiver_api_list_create'),
    path('api/receiver/<int:pk>/',views.ReceiverApiDetail.as_view(),name='receiver_api_detail'),
    path('api/satellite-systems/',views.SatelliteSystemApiListCreate.as_view(),name='satellite_system_api_list_create'),
    path('api/satellite-system/<int:pk>/',views.SatelliteSystemApiDetail.as_view(),name='satellite_system_api_detail'),
    path('api/processing-reports/',views.ProcessingReportApiListCreate.as_view(),name='processing_report_api_list_create'),
    path('api/processing-report/<int:pk>/',views.ProcessingReportApiDetail.as_view(),name='processing_report_api_detail'),

]
    




