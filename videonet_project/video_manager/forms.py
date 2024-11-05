from django import forms
from .models import Video

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["title", "description", "video_file", "thumbnail"]
        labels = {
            "title": "Título",
            "description": "Descripción",
            "video_file": "Archivo de Video",
            "thumbnail": "Miniatura",
        }

class VideoSearchForm(forms.Form):
    query = forms.CharField(label="Buscar", max_length=200, required=False)