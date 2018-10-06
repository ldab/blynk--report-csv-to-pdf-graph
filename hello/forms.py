from django import forms
#from models import Document

class UploadFileForm(forms.Form):
    #title = forms.CharField(max_length=50) #change length size
    file  = forms.FileField()

#class DocumentForm(forms.ModelForm):
#    class Meta:
#        model = Document
#        fields = ('description', 'document', )
