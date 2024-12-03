from .models import Profile
from django import forms
from django.contrib.auth.models import User
from app import models


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        data = super().clean()

        return data


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    reapeatenPassword = forms.CharField(widget=forms.PasswordInput)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean(self):
        data = super().clean()
        if data.get('password') != data.get('reapeatenPassword'):
            raise forms.ValidationError('Passwords do not match')

        if User.objects.filter(username=data.get('username')).exists():
            raise forms.ValidationError(
                'User with this username is already exists')

        if User.objects.filter(email=data.get('email')).exists():
            raise forms.ValidationError(
                'User with this email is already exists')

        return data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        avatar = self.cleaned_data.get('avatar')
        Profile.objects.create(user=user, avatar=avatar)

        return user


class SettingsForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean(self):
        data = super().clean()
        return data

    def save(self, commit=True):
        user = User.objects.get(id=self.instance.id)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.save()

        profile = models.Profile.objects.get(user=user)
        avatar = self.cleaned_data.get('avatar')
        profile.avatar = avatar
        profile.save()

        return user
