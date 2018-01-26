from __future__ import unicode_literals
from django import forms
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget

'''
class Postform(forms.Form):
    title=forms.CharField(max_length=50,widget=forms.
                          TextInput(attrs={'placeholder':'Title'}))
    content=forms.CharField(widget=forms.
Textarea(attrs=
         {'placeholder':'Comment','rows':4,'cols':30,'style':'resize:none'}))
    
'''
#here no need to define all the fields
class PostForm(forms.ModelForm):
    
    title=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder': 'Name of a book/movie','class':'form-control','style':'width:300px;'}))
    content=forms.CharField(widget=CKEditorUploadingWidget())
    pic=models.FileField()
    class Meta:
        model=Post
        #fields=['title','content'] 
        fields='__all__'

class Regforms(forms.ModelForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),
    max_length=30,required=True)
    email=forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control'}),
    max_length=30,required=True)
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),
    max_length=30,required=True)
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),
    label="Confirm your password", max_length=30,required=True)
    class Meta:
        model=User
        fields=['username','email','password','confirm_password']

    def clean(self):
        cleaned_data = super(Regforms, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )


class MyProfile(forms.ModelForm):
    first_name=forms.CharField(widget=forms.TextInput
                             (attrs={'class':'form-control'}),
                             max_length=30,
                             required=True)
    
    last_name=forms.CharField(widget=forms.TextInput
                             (attrs={'class':'form-control'}),
                             max_length=30,
                             required=True)

    email=forms.CharField(widget=forms.EmailInput
                             (attrs={'class':'form-control'}),
                             max_length=30,
                             required=True)
    gender=forms.CharField(widget=forms.Select(
                 choices=Profile.gender_choices),
                           required=False)
    location=forms.CharField(widget=forms.TextInput
                             (attrs={'class':'form-control'}),
                             max_length=30,
                             required=False)
    bio=forms.CharField(widget=forms.TextInput
                             (attrs={'class':'form-control'}),
                             max_length=100,
                             required=True)
    profilepic=forms.FileField(required=True)
    facebook=forms.URLField(widget=forms.URLInput
                             (attrs={'class':'form-control'}),
                             required=False)
    twitter=forms.URLField(widget=forms.URLInput
                             (attrs={'class':'form-control'}),
                             required=False)
    instagram=forms.URLField(widget=forms.URLInput
                             (attrs={'class':'form-control'}),
                             required=False)
    
    class Meta:
        model=User
        fields=['first_name','last_name','email','location','profilepic','bio','facebook','twitter','instagram','gender']
        

class Password(forms.ModelForm):
    old_password=forms.CharField(widget=forms.PasswordInput
                             (attrs={'class':'form-control'}),
                             max_length=30,
                             label="Old password",
                             required=True)
    new_password=forms.CharField(widget=forms.PasswordInput
                             (attrs={'class':'form-control'}),
                             max_length=30,
                             label="New password",
                             required=True)
    confirm_password=forms.CharField(widget=forms.PasswordInput
                             (attrs={'class':'form-control'}),
                             max_length=30,
                             label="Confirm new password",
                             required=True)

    
        
    class Meta:
        model=User
        fields=['old_password','new_password','confirm_password']
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')
