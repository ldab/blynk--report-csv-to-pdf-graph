from django import forms
from uploads.core.models import Document

class UploadFileForm(forms.Form):
    file  = forms.FileField()

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )
        