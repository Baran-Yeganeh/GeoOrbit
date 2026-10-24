from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

class Mission(models.Model):
    project_name = models.CharField(max_length=500,verbose_name='Project Name')
    project_location = models.CharField(max_length=300, verbose_name='Location')
    surveying_start_date = models.DateTimeField(default=timezone.now, verbose_name='Start Date')
    surveying_end_date = models.DateTimeField(default=timezone.now, verbose_name='End Date')


    # Foreign Key ---> One Receiver can have many Missions
    receiver = models.ForeignKey('Receiver',
                                    on_delete=models.CASCADE,
                                    related_name='mission',
                                    verbose_name='Receiver',
                                    null=True,
                                    blank=True)

    # ManyToMany ---> one Mission can use Many Satellite Systems
    satellite_systems = models.ManyToManyField('SatelliteSystem',
                                            related_name='mission',
                                            verbose_name='satellite system',
                                            blank=True)
    mission_image = models.ImageField(verbose_name='Image',
                                      upload_to='gnss/mission_image/',
                                      null=True,
                                      blank=True)


    def __str__(self):
        return self.project_name

    def clean(self):
        super().clean()
        if (self.surveying_start_date and self.surveying_end_date
                and self.surveying_end_date < self.surveying_start_date):
            raise ValidationError(
                {'surveying_end_date': 'End date cannot be before the start date.'}
            )



class Receiver(models.Model):
    receiver_name = models.CharField(max_length=200, verbose_name='Receiver Name')
    manufacturer = models.CharField(max_length=200, verbose_name='Manufacturer')
    receiver_model = models.CharField(max_length=200, verbose_name='Receiver Model')
    receiver_image = models.ImageField(upload_to='gnss/receivers/',blank=True,null=True,verbose_name='Receiver image')

    def __str__(self):
        return f'{self.receiver_name} {self.receiver_model}'

class SatelliteSystem(models.Model):
    satellite_name =  models.CharField(max_length=200, verbose_name='Satellite Name')
    satellite_country = models.CharField(max_length=200, verbose_name='Satellite Country')
    satellite_image = models.ImageField(upload_to='gnss/satellite_systems/',blank=True,null=True,verbose_name='Satellite image')
    def __str__(self):
        return f'{self.satellite_name} ({self.satellite_country})'


class ProcessingReport(models.Model):
    method= models.CharField(max_length=200, verbose_name='Method')
    accuracy = models.CharField(max_length=200, verbose_name='Accuracy')
    description = models.TextField(default='...', verbose_name='Description')

    #OneToOne --->
    mission = models.OneToOneField(Mission,
                                   on_delete =models.CASCADE,
                                   verbose_name='Mission',
                                   related_name='processing_report',
                                   null=True,
                                    blank=True)

    def __str__(self):
        return f'{self.method} ({self.accuracy})'



