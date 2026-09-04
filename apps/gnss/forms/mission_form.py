from django import forms
from apps.gnss.models import Mission


class Mission_Form_1(forms.ModelForm):
    class Meta:
        model = Mission
        fields = "__all__"
        widgets = {
            'project_name' : forms.TextInput(
                attrs={'placeholder': 'Enter the project name...'},
                
            ),
            'project_location' : forms.TextInput(
                attrs={'placeholder': 'Enter the project locathin...'},
            ),
            
            
        }
    