from django.contrib import admin
from .models import *


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):

    list_display = (
        'project_name',
        'project_location',
        'surveying_end_date',
        'surveying_start_date',
        'receiver',
        'display_satellite_systems',
    )
    
        
    list_filter = ('project_location',
                   'surveying_start_date',
                   'surveying_end_date',
                   'receiver')
    
    search_fields = ('project_name',
                    'project_location',
                    'surveying_start_date',
                    'surveying_end_date',
                    'receiver__receiver_name')        
    

    def display_satellite_systems(self, obj):
        sat_names=[]
        for satellite in obj.satellite_systems.all():
            sat_names.append(satellite.satellite_name)
        
        return ", ".join(sat_names)

    
@admin.register(Receiver)
class ReceiverAdmin(admin.ModelAdmin):
    list_display=(
        'receiver_name',
        'manufacturer',
        'receiver_model',        
    )   
    list_filter = (
        'receiver_name',
        'manufacturer',
        'receiver_model'
    )
    
    search_fields = (
        'receiver_name',
        'manufacturer',
        'receiver_model'
    )  
    
@admin.register(SatelliteSystem)
class SatelliteSystemAdmin(admin.ModelAdmin):
    list_display=(
        'satellite_name',
        'satellite_country',
    )   
    
    list_filter = (
        'satellite_name',
        'satellite_country',  
    ) 
    search_fields = (
        'satellite_name',
        'satellite_country',  
    )      
    
    
@admin.register(ProcessingReport)
class ProcessingReportAdmin(admin.ModelAdmin):
    list_display=(
        'method',
        'accuracy',
        'description',
        'mission',
    )          

    list_filter = (
        'method',
        'mission',        
    ) 
    search_fields = (
        'method',
        'mission__project_name', 
    )   
