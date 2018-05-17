import re
from django.contrib.auth.models import User
from django import forms
from cyberpunk.models import *

class RegistrationForm(forms.Form):
    username = forms.CharField(label=u'Username', max_length=30)
    email = forms.EmailField(label=u'Email')    
    password1 = forms.CharField(
        label=u'Password',
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label=u'Password (Again)',
        widget=forms.PasswordInput()
    )
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only contain '
                                        'alphanumeric characters and the underscore.')
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Username is already taken.')

    def clean_password(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Passwords do not match.')

class UserProfileForm(forms.ModelForm):    
    class Meta:
        model = UserProfile
        exclude = {
            'user'
            }

class CharacterForm(forms.ModelForm):    
    class Meta:
        model = Character
        widgets = {            
            'created' : forms.HiddenInput(),            
            'modified': forms.HiddenInput(),
            'notes' : forms.Textarea(attrs={'cols': 20, 'rows' : 10}),
            }
        exclude = (
            'user',    
            'contactpts',
            'ip',
            'totskill',
            'locked',
            )

class StatisticsForm(forms.ModelForm):
    body = forms.ChoiceField(choices=[(x,x) for x in range(0,19)])
    reflex = forms.ChoiceField(choices=[(x,x) for x in range(0,19)])
    move = forms.ChoiceField(choices=[(x,x) for x in range(0,19)])
    intelligence = forms.ChoiceField(choices=[(x,x) for x in range(0,19)])
    tech = forms.ChoiceField(choices=[(x,x) for x in range(0,19)])
    cool = forms.ChoiceField(choices=[(x,x) for x in range(0,19)])
    empathy = forms.ChoiceField(choices=[(x,x) for x in range(0,19)])
    attractiveness = forms.ChoiceField(choices=[(x,x) for x in range(0,19)])
    luck = forms.ChoiceField(choices=[(x,x) for x in range(0,19)])
    class Meta:
        model = Statistics        
        exclude = {
            'char',
            'bodybonus',
            'reflexbonus',
            'movebonus',
            'intelbonus',
            'techbonus',
            'coolbonus',
            'empbonus',
            'attrbonus',
            'luckbonus',
            'total',
            }

class SkillForm(forms.ModelForm):
    skill_choices = (
        ('special', 'Special Skill'),
        ('attr', 'Attractiveness Skill'),
        ('body', 'Body Skill'),
        ('cool', 'Cool Skill'),
        ('empathy', 'Empathy Skill'),
        ('int', 'Intelligence Skill'),
        ('tech', 'Tech Skill'),
        ('ref', 'Reflex Skill'),
    )
    Category = forms.ChoiceField(choices=skill_choices)
    point = forms.ChoiceField(choices=[(x,x) for x in range(0,11)])
    class Meta:
        model = Skill
        exclude = {
            'char',
            'bonus',
            }

class EffectForm(forms.ModelForm):
    effect_choices = (
        ('benefit', 'Benefit'),
        ('penalty', 'Penalty'),
    )
    Category = forms.ChoiceField(choices=effect_choices)
    class Meta:
        model = Effect
        exclude = {
            'char',
            }

class LifePathForm(forms.ModelForm):
    class Meta:
        model = LifePath
        widgets = {
            'desc' : forms.Textarea(attrs={'cols': 30, 'rows' : 10}),
            }
        exclude = {
            'char',
            }        

class WoundForm(forms.ModelForm):
    class Meta:
        model = Wound
        exclude = {
            'char',
            }        

class ContactForm(forms.ModelForm):
    capability_choices = (
        (-2, "Snitch"),
        (-1, "Incapable"),
        (0, "Capable"),
        (1, "Very Capable"),
        (2, "Super Capable"),
    )

    loyalty_choices = (
        (-1, "Unreliable"),
        (0, "Reliable"),
        (1, "Very Reliable"),
        (2, "Super Reliable"),
    )
    
    access_choices = (
        (-1, "Specialist"),
        (0, "Typical"),
        (1, "Mid-Level"),
        (2, "Upper Echelon"),
    )

    availability_choices = (
        (-1, "Rarely"),
        (0, "Sometimes"),
        (1, "Usually"),
        (2, "Always"),
    )
    capability = forms.ChoiceField(choices=capability_choices)
    loyalty = forms.ChoiceField(choices=loyalty_choices)
    access = forms.ChoiceField(choices=access_choices)
    availability = forms.ChoiceField(choices=availability_choices)
    class Meta:
        model = Contact
        # widgets = {
          #  'notes' : forms.Textarea(attrs={'cols': 24, 'rows' : 10}),
          #  }
        exclude = {
            'char',
            }

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        exclude = {
            'char',
            }        

class Cyber_BioForm(forms.ModelForm):
    class Meta:
        model = Cyber_Bio
        exclude = {
            'char',
            }        

class WeaponForm(forms.ModelForm):
    class Meta:
        model = Weapon
        exclude = {
            'char',
            }

class ArmorForm(forms.ModelForm):
    armor_parts = (
        ('Head', 'Head'),
        ('Torso', 'Torso'),
        ('Left Arm', 'Left Arm'),
        ('Right Arm', 'Right Arm'),
        ('Left Leg', 'Left Leg'),
        ('Right Leg', 'Right Leg'),
    )
    Category = forms.ChoiceField(choices=armor_parts)
    class Meta:
        model = Armor
        exclude = {
            'char',
            }

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        exclude = {
            'char',
            }

class MoneyForm(forms.ModelForm):
    class Meta:
        model = Money
        exclude = {
            'char',
            }

class ResidenceForm(forms.ModelForm):
    class Meta:
        model = Residence
        exclude = {
            'char',
            }

StatFormSet = forms.models.inlineformset_factory(Character, Statistics, form=StatisticsForm, can_delete=False)
MoneyFormSet = forms.models.inlineformset_factory(Character, Money, form=MoneyForm, can_delete=False)
ResFormSet = forms.models.inlineformset_factory(Character, Residence, form=ResidenceForm, can_delete=False)    
