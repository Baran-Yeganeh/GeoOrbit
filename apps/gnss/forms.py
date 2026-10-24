
from django import forms
from .models import Mission, Receiver, SatelliteSystem


class MissionForm(forms.ModelForm):
    """Form used by the create and update mission pages."""

    DATETIME_FORMAT = '%Y-%m-%dT%H:%M'

    class Meta:
        model = Mission
        fields = [
            'project_name',
            'project_location',
            'surveying_start_date',
            'surveying_end_date',
            'receiver',
            'satellite_systems',
            'mission_image',
        ]
        widgets = {
            'project_name': forms.TextInput(
                attrs={'placeholder': 'e.g. Tehran control network'}
            ),
            'project_location': forms.TextInput(
                attrs={'placeholder': 'e.g. Tehran, Iran'}
            ),
            'satellite_systems': forms.SelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ('surveying_start_date', 'surveying_end_date'):
            self.fields[name].widget = forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format=self.DATETIME_FORMAT,
            )
            self.fields[name].input_formats = [self.DATETIME_FORMAT]
        self.fields['satellite_systems'].help_text = (
            'Hold Ctrl (or Cmd) to select more than one.'
        )


class ReceiverForm(forms.ModelForm):
    class Meta:
        model = Receiver
        fields = [
            'receiver_name',
            'manufacturer',
            'receiver_model',
            'receiver_image',
        ]
        widgets = {
            'receiver_name': forms.TextInput(
                attrs={'placeholder': 'Enter receiver name...'}
            ),
            'manufacturer': forms.TextInput(
                attrs={'placeholder': 'Enter manufacturer...'}
            ),
            'receiver_model': forms.TextInput(
                attrs={'placeholder': 'Enter receiver model...'}
            ),
        }


class SatelliteSystemForm(forms.ModelForm):
    class Meta:
        model = SatelliteSystem
        fields = [
            'satellite_name',
            'satellite_country',
            'satellite_image',
        ]
        widgets = {
            'satellite_name': forms.TextInput(
                attrs={'placeholder': 'Enter satellite system name...'}
            ),
            'satellite_country': forms.TextInput(
                attrs={'placeholder': 'Enter country...'}
            ),
        }
