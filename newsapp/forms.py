from django import forms
from .models import Contact, Comment, News


class BootstrapStyleMixin:
    field_names = None
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.field_names:
            for fieldname in self.field_names:
                self.fields[fieldname].widget.attrs = {'class': 'form-control'}
        else:
            raise ValueError('The field_names must be set')




class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
       
       
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
     

from django.forms import formset_factory
 
class ImageForm(forms.Form):
    image = forms.ImageField()

ImageFormSet = formset_factory(ImageForm, extra=1)

 
        
        
class AdminAddNewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields =  ('title', 'title_uz', 'title_ru', 'title_en', 'author',
            'body', 'body_uz', 'body_ru', 'body_en', 
            'image', 'category', 'status')

class CustomAdminAddNewsForm(BootstrapStyleMixin, AdminAddNewsForm):
    field_names = ('title', 'title_uz', 'title_ru', 'title_en', 'author',
            'body', 'body_uz', 'body_ru', 'body_en', 
            'image', 'category', 'status')
    
    


class AdminAddNewsAudioForm(forms.ModelForm):
    class Meta:
        model = News
        fields =  ('title', 'title_uz', 'title_ru', 'title_en', 
            'audio_file', 'category', 'author', 'status')

class CustomAdminAddNewsAudioForm(BootstrapStyleMixin, AdminAddNewsAudioForm):
    field_names = ('title', 'title_uz', 'title_ru', 'title_en',
            'audio_file', 'category', 'author', 'status')




class AdminAddNewsVideoForm(forms.ModelForm):
    class Meta:
        model = News
        fields =  ('title', 'title_uz', 'title_ru', 'title_en',
         'video_file', 'category', 'author', 'status')

class CustomAdminAddNewsVideoForm(BootstrapStyleMixin, AdminAddNewsVideoForm):
    field_names = ('title', 'title_uz', 'title_ru', 'title_en',
            'video_file', 'category', 'author', 'status')