import apps.main.views as views
from django.urls import path

urlpatterns = [
    path('',views.mainPage, name='mainPage'),
    path('introduction/',views.projectIntroduction,name='introductionPage'),
     
]
 