from django import forms

class UploadVideoForm(forms.Form):
     video = forms.FileField()

class RTSPForm(forms.Form):
    rtsp_url = forms.CharField(label="RTSP URL", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))