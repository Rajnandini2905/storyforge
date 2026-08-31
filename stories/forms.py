"""
forms.py — StoryForge Forms

  SignUpForm   → username + password + confirm password
  SignInForm   → username + password
  CommentForm  → story comment
  ProfileForm  → edit bio & avatar
  UserEditForm → edit name & email
"""

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Comment, Profile
import re


# ═══════════════════════════════════════════════════════════════
#  SIGN UP FORM
# ═══════════════════════════════════════════════════════════════
class SignUpForm(forms.Form):
    username = forms.CharField(
        max_length=150, min_length=3, label='Username',
        widget=forms.TextInput(attrs={
            'class': 'forge-input', 'placeholder': 'Choose a username', 'autofocus': True,
        }),
        error_messages={
            'required': 'Please choose a username.',
            'min_length': 'Username must be at least 3 characters.',
        }
    )
    password = forms.CharField(
        min_length=6, label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'forge-input', 'placeholder': 'Create a password (min 6 characters)',
        }),
        error_messages={
            'required': 'Please enter a password.',
            'min_length': 'Password must be at least 6 characters.',
        }
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'forge-input', 'placeholder': 'Repeat your password',
        }),
        error_messages={'required': 'Please confirm your password.'}
    )

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if not re.match(r'^[\w.\-]+$', username):
            raise ValidationError('Only letters, numbers, underscores, dots, hyphens allowed.')
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('That username is already taken. Please choose another.')
        return username

    def clean(self):
        cleaned = super().clean()
        pw  = cleaned.get('password')
        cpw = cleaned.get('confirm_password')
        if pw and cpw and pw != cpw:
            self.add_error('confirm_password', 'Passwords do not match.')
        return cleaned


# ═══════════════════════════════════════════════════════════════
#  SIGN IN FORM
# ═══════════════════════════════════════════════════════════════
class SignInForm(forms.Form):
    username = forms.CharField(
        max_length=150, label='Username',
        widget=forms.TextInput(attrs={
            'class': 'forge-input', 'placeholder': 'Your username', 'autofocus': True,
        }),
        error_messages={'required': 'Please enter your username.'}
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'forge-input', 'placeholder': 'Your password',
        }),
        error_messages={'required': 'Please enter your password.'}
    )


# ═══════════════════════════════════════════════════════════════
#  COMMENT FORM
# ═══════════════════════════════════════════════════════════════
class CommentForm(forms.ModelForm):
    class Meta:
        model  = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'forge-input', 'rows': 3,
                'placeholder': 'Share your thoughts about this story…',
            })
        }
        labels = {'text': ''}


# ═══════════════════════════════════════════════════════════════
#  PROFILE FORM
# ═══════════════════════════════════════════════════════════════
class ProfileForm(forms.ModelForm):
    AVATAR_CHOICES = [
        ('🧙','🧙 Wizard'), ('🧝','🧝 Elf'), ('🧛','🧛 Vampire'),
        ('🦸','🦸 Hero'),   ('🦹','🦹 Villain'), ('🧚','🧚 Fairy'),
        ('🐉','🐉 Dragon'), ('⚔️','⚔️ Warrior'), ('🚀','🚀 Explorer'),
        ('🕵️','🕵️ Detective'),
    ]
    avatar_emoji = forms.ChoiceField(choices=AVATAR_CHOICES, widget=forms.RadioSelect())

    class Meta:
        model  = Profile
        fields = ('bio', 'avatar_emoji')
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'forge-input', 'rows': 3,
                'placeholder': 'Tell us about yourself…', 'maxlength': 500,
            })
        }


# ═══════════════════════════════════════════════════════════════
#  USER EDIT FORM
# ═══════════════════════════════════════════════════════════════
class UserEditForm(forms.ModelForm):
    class Meta:
        model  = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'forge-input'}),
            'last_name':  forms.TextInput(attrs={'class': 'forge-input'}),
            'email':      forms.EmailInput(attrs={'class': 'forge-input'}),
        }