from django.urls import path
from . import views





urlpatterns = [
    # path('form/', views.mission_form_01,name="mission_form"),
    path('missionslist/',views.MissionList.as_view(),name="mission_list"),
    path('missiondetail/<int:pk>/',views.MissionDetail.as_view(),name="mission_detail"),
    path('new/',views.MissionCreate.as_view(),name="mission_create"),
    path('missionedit/<int:pk>/',views.MissionUpdate.as_view(),name="mission_edit"),
    path('missiondelete/<int:pk>/',views.MissionDelete.as_view(),name="mission_delete"),
    path('testemail/',views.send_email,name='send_email'),
    path('testjava/',views.test_java,name='test_java'),
    
    ]
    




