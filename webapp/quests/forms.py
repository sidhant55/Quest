from django import forms

class Registerkey(forms.Form):
    name=forms.CharField(max_length=50)
    email=forms.CharField(max_length=100)
    key=forms.CharField(max_length=100)

class Postone(forms.Form):
    key=forms.CharField(max_length=100)
    image=forms.FileField()

class Deleteone(forms.Form):
    key=forms.CharField(max_length=100)
    image=forms.FileField()

class Updateone(forms.Form):
    key=forms.CharField(max_length=100)
    image=forms.FileField()

class Getlist(forms.Form):
    key=forms.CharField(max_length=100)

class Getone(forms.Form):
    key=forms.CharField(max_length=100)
    image=forms.CharField(max_length=100)

class Forgotkey(forms.Form):
    email=forms.CharField(max_length=100)