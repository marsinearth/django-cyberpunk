from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from cyberpunk.models import *
from datetime import datetime

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_active',
                  'is_staff', 'is_superuser')

class CustomUserAdmin(UserAdmin):
    fieldsets = None
    form = UserForm
    search_fields = ('=username',)

class StatInline(admin.StackedInline):
    model = Statistics
    readonly_fields = ('total',)
    fields = (('body', 'bodybonus', 'reflex', 'reflexbonus', 'move', 'movebonus'), ('intelligence', 'intelbonus', 'tech', 'techbonus', 'cool', 'coolbonus'), ('empathy', 'empbonus', 'attractiveness', 'attrbonus', 'luck', 'luckbonus'), 'total')

class WeaponInline(admin.StackedInline):
    model = Weapon
    fields = (('wpname', 'accuracy', 'damage', 'rof'), ('ammo', 'Range', 'reliability', 'conceal'), 'equipped')
    extra = 0

class VehicleInline(admin.StackedInline):
    model = Vehicle
    fields = (('vcname', 'topSpeed', 'accel', 'deccel'), ('crew', 'Range', 'passengers', 'cargo'), ('maneuver', 'sdp', 'sp', 'Type'), ('mass', 'cost'), 'equipped') 
    extra = 0

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

class ArmorInline(admin.StackedInline):
    model = Armor
    form = ArmorForm
    extra = 0

class MoneyInline(admin.TabularInline):
    model = Money

class ResidenceInline(admin.TabularInline):
    model = Residence
    extra = 1

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
    class Meta:
        model = Skill
        exclude = {
            'char',
            }    

class SkillInline(admin.TabularInline):
    model = Skill
    extra = 0
    form = SkillForm

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

class EffectInline(admin.TabularInline):
    model = Effect
    extra = 0
    form = EffectForm

class LifePathInline(admin.TabularInline):
    model = LifePath
    extra = 0

class WoundInline(admin.TabularInline):
    model = Wound
    extra = 0

class ContactInline(admin.TabularInline):
    model = Contact
    extra = 0
    
class EquipInline(admin.TabularInline):
    model = Equipment
    extra = 0

class CyberInline(admin.TabularInline):
    model = Cyber_Bio
    extra = 0
 
class CharForm(forms.ModelForm):        
    class Meta:
        model = Character
    def save(self, commit=True):
        model = super(CharForm, self).save(commit=False)
        model.collect_skillpts() #calculate skill points
        model.collect_contactpts() #calculate contact points
        if not model.created:
            model.created = datetime.now().strftime('%Y-%m-%d %H:%M')
        else:
            model.modified = datetime.now().strftime('%Y-%m-%d %H:%M')
        if commit:            
            model.save()
        return model

class CharAdminPage(admin.ModelAdmin):    
    inlines = [
        StatInline,
        MoneyInline,
        ResidenceInline,
        WeaponInline,
        VehicleInline,
        SkillInline,
        ArmorInline,
        CyberInline,        
        EffectInline,
        LifePathInline,
        WoundInline,
        ContactInline,
        EquipInline,        
    ]
    form = CharForm
    readonly_fields = ('totskill', 'contactpts','created',)
    fieldsets = (
        (None, {
                'fields': ('user', 'name', 'ethnicity', ('primaryRole', 'secondaryRole'), ('monSalary', 'totskill', 'contactpts'), 'notes', 'ip', ('locked'))
        }),
        (None, {
                'classes': ('collapse',),
                'fields': ('created', 'modified',)
        }),
    )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin) 
admin.site.register(Character, CharAdminPage)
