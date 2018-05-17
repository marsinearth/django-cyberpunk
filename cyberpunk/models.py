from django.db import models
from django.contrib.auth.models import User
from google.appengine.ext import db

class Character(models.Model):    
    user = models.ForeignKey(User, related_name="chars", null=True)
    name = models.CharField(max_length=200, verbose_name=u'Name', unique=True)
    ethnicity = models.CharField(max_length=200, verbose_name=u'Ethnicity')
    primaryRole = models.CharField(max_length=50, verbose_name=u'Primary Role')
    secondaryRole = models.CharField(max_length=50, verbose_name=u'Secondary Role', blank=True, null=True)    
    monSalary = models.FloatField(verbose_name=u'Monthly Salary')
    contactpts = models.IntegerField(default=1, verbose_name=u'Contact Point')
    totskill = models.IntegerField(default=0, verbose_name=u'Total SkillPoint')
    notes = models.TextField(max_length=5000, verbose_name=u'Notes', blank=True, null=True)
    ip = models.IntegerField(default=0, verbose_name=u'IP')
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(blank=True, null=True)
    locked = models.BooleanField()
    def __unicode__(self):
        if self.name:
            return self.name

    def collect_skillpts(self):
        self.totskill = 0
        for skill in self.skills.all():
            self.totskill += skill.point
        self.save()

    def collect_contactpts(self):
        self.contactpts = 0
        for contact in self.contact.all():
            self.contactpts += sum([contact.capability, contact.loyalty, contact.access, contact.availability])
        if self.contactpts == 0:
            self.contactpts = 1
        self.save()

class Skill(models.Model):
    char = models.ForeignKey(Character, related_name='skills', null=True, blank=True)
    name = models.CharField(max_length=300, verbose_name=u'Skill Name')
    Category = models.CharField(max_length=100)
    point = models.IntegerField(default=0, verbose_name=u'Point')
    bonus = models.IntegerField(default=0, verbose_name=u'Bonus')
    def __unicode__(self):
        return "Skill"

    def __iter__(self):
        for field in self._meta.fields:
            yield (field.verbose_name, field.value_to_string(self))
    class Meta:
        ordering = ['name']

class Effect(models.Model):
    char = models.ForeignKey(Character, related_name='effects', null=True, blank=True)
    Category = models.CharField(max_length=10)
    desc = models.CharField(max_length=200, verbose_name=u'Description')
    effect = models.CharField(max_length=200, verbose_name=u'Effect')
    cost = models.CharField(max_length=20, verbose_name=u'Cost')
    def __unicode__(self):
        return "Effect"

    def __iter__(self):
        for field in self._meta.fields:
            yield (field.verbose_name, field.value_to_string(self))
    class Meta:
        ordering = ['desc']

class LifePath(models.Model):
    char = models.ForeignKey(Character, related_name='lifepath', null=True, blank=True)
    age = models.IntegerField(default=16, verbose_name=u'Age')
    desc = models.TextField(max_length=5000, verbose_name=u'Description')
    def __unicode__(self):
        return "Life Path"

    def __iter__(self):
        for field in self._meta.fields:
            yield (field.verbose_name, field.value_to_string(self))
    class Meta:
        ordering = ['age']

class Wound(models.Model):
    char = models.ForeignKey(Character, related_name='wound', null=True, blank=True)
    curWound = models.CharField(max_length=100, verbose_name=u'Current Wound')
    curRateperDay = models.CharField(max_length=50, verbose_name=u'Current Rate Per Day')
    def __unicode__(self):
        return "Wound"

    def __iter__(self):
        for field in self._meta.fields:
            yield (field.verbose_name, field.value_to_string(self))
    class Meta:
        ordering = ['curWound']

class Contact(models.Model):
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

    char = models.ForeignKey(Character, related_name='contact', null=True, blank=True)
    ctname = models.CharField(max_length=100, verbose_name=u'Name')
    capability = models.IntegerField(choices=capability_choices, default=0, verbose_name=u'Capability')
    loyalty = models.IntegerField(choices=loyalty_choices, default=0, verbose_name=u'Loyalty')
    access = models.IntegerField(choices=access_choices, default=0, verbose_name=u'Access')
    availability = models.IntegerField(choices=availability_choices, default=0, verbose_name=u'Availability')
    notes = models.TextField(max_length=5000, verbose_name=u'Notes', blank=True, null=True)
    def __unicode__(self):
        return "Contact"

    def __iter__(self):
        for field in self._meta.fields:
            yield (field.verbose_name, field.value_to_string(self))
    class Meta:
        ordering = ['ctname']

class Equipment(models.Model):
    char = models.ForeignKey(Character, related_name='inventory', null=True, blank=True)
    eqname = models.CharField(max_length=300, verbose_name=u'Name')
    itemDesc = models.CharField(max_length=300, verbose_name=u'Description')
    Effect = models.CharField(max_length=300, verbose_name=u'Effect')
    cost = models.FloatField(default=0, verbose_name=u'Cost')
    def __unicode__(self):
        return "Equipment"

    def __iter__(self):
        for field in self._meta.fields:
            yield (field.verbose_name, field.value_to_string(self))
    class Meta:
        ordering = ['eqname']
            
class Cyber_Bio(models.Model):
    char = models.ForeignKey(Character, related_name='cyber_bio', null=True, blank=True)
    eqname = models.CharField(max_length=300, verbose_name=u'Name')
    itemDesc = models.CharField(max_length=1000, verbose_name=u'Item Description')
    itemEffect = models.CharField(max_length=1000, verbose_name=u'Item Effect')
    humLoss = models.CharField(max_length=600, verbose_name=u'Humanity Loss')
    cost = models.FloatField(default=0, verbose_name=u'Cost')
    equipped = models.BooleanField()
    def __unicode__(self):
        return "Cybertech/Bioware"

    def __iter__(self):
        for field in self._meta.fields:
            yield (field.verbose_name, field.value_to_string(self))
    class Meta:
        ordering = ['eqname']
     
class Statistics(models.Model):
    char = models.ForeignKey(Character, related_name="stat", unique=True)
    body = models.IntegerField(default=0, verbose_name=u'Body')
    bodybonus = models.IntegerField(default=0, verbose_name=u'Bonus')
    reflex = models.IntegerField(default=0, verbose_name=u'Reflex')
    reflexbonus = models.IntegerField(default=0, verbose_name=u'Bonus')
    move = models.IntegerField(default=0, verbose_name=u'Move')
    movebonus = models.IntegerField(default=0, verbose_name=u'Bonus')
    intelligence = models.IntegerField(default=0, verbose_name=u'Intelligence')
    intelbonus = models.IntegerField(default=0, verbose_name=u'Bonus')
    tech = models.IntegerField(default=0, verbose_name=u'Tech')
    techbonus = models.IntegerField(default=0, verbose_name=u'Bonus')
    cool = models.IntegerField(default=0, verbose_name=u'Cool')
    coolbonus = models.IntegerField(default=0, verbose_name=u'Bonus')
    empathy = models.IntegerField(default=0, verbose_name=u'Empathy')
    empbonus = models.IntegerField(default=0, verbose_name=u'Bonus')
    attractiveness = models.IntegerField(default=0, verbose_name=u'Attractiveness')
    attrbonus = models.IntegerField(default=0, verbose_name=u'Bonus')
    luck = models.IntegerField(default=0, verbose_name=u'Luck')
    luckbonus = models.IntegerField(default=0, verbose_name=u'Bonus')
    total = models.IntegerField(default=0, verbose_name=u'Total')
    
    def save(self, *args, **kwargs):
        self.total = self.body + self.reflex + self.move + self.intelligence + \
            self.tech + self.cool + self.empathy + self.attractiveness + self.luck
        super(Statistics, self).save(*args, **kwargs)

class Armor(models.Model):
    char = models.ForeignKey(Character, related_name='armor')
    amname = models.CharField(max_length=500, verbose_name=u'Name')
    ampoint = models.IntegerField(default=0, verbose_name=u'Point')
    Category = models.CharField(max_length=10)
    cost = models.FloatField(default=0, verbose_name=u'Cost')
    equipped = models.BooleanField()
    def __unicode__(self):
        return "Armor"

    def __iter__(self):
        for field in self._meta.fields:
            yield (field.verbose_name, field.value_to_string(self))
    class Meta:
        ordering = ['amname']
            
class Weapon(models.Model):
    char = models.ForeignKey(Character, related_name='weapon')
    wpname = models.CharField(max_length=500, verbose_name=u'Name')
    accuracy = models.CharField(max_length=50, verbose_name=u'Accuracy')
    damage = models.CharField(max_length=50, verbose_name=u'Damage')
    rof = models.CharField(max_length=50, verbose_name=u'Rate of Fire')
    ammo = models.CharField(max_length=50, verbose_name=u'Ammo')
    Range = models.CharField(max_length=50, verbose_name=u'Range')
    reliability = models.CharField(max_length=50, verbose_name=u'Reliability')
    conceal = models.CharField(max_length=50, verbose_name=u'Conceal')
    cost = models.FloatField(default=0, verbose_name=u'Cost')
    equipped = models.BooleanField()
    def __unicode__(self):
        return "Weapon"
    
    def __iter__(self):
        for field in self._meta.fields:
            yield (field.verbose_name, field.value_to_string(self))
    class Meta:
        ordering = ['wpname']

class Vehicle(models.Model):
    char = models.ForeignKey(Character, related_name='vehicle')
    vcname = models.CharField(max_length=500, verbose_name=u'Name')
    topSpeed = models.CharField(max_length=50, verbose_name=u'Top Speed')
    accel = models.CharField(max_length=50, verbose_name=u'Acceleration')
    deccel = models.CharField(max_length=50, verbose_name=u'Decceleration')
    crew = models.CharField(max_length=500, verbose_name=u'Crew(s)')
    Range = models.CharField(max_length=50, verbose_name=u'Range')
    passengers = models.CharField(max_length=50, verbose_name=u'Passenger(s)')
    cargo = models.CharField(max_length=50, verbose_name=u'Cargo')
    maneuver = models.CharField(max_length=50, verbose_name=u'Maneuver')
    sdp = models.CharField(max_length=50, verbose_name=u'SDP')
    sp = models.CharField(max_length=50, verbose_name=u'SP')
    Type = models.CharField(max_length=50, verbose_name=u'Type')
    mass = models.CharField(max_length=50, verbose_name=u'Mass')
    cost = models.FloatField(default=0, verbose_name=u'Cost')
    equipped = models.BooleanField()
    def __unicode__(self):
        return "Vehicle"

    def __iter__(self):
        for field in self._meta.fields:
            yield (field.verbose_name, field.value_to_string(self))
    class Meta:
        ordering = ['vcname']

class Money(models.Model):
    char = models.ForeignKey(Character, related_name='money', unique=True)
    cash = models.FloatField(default=0, verbose_name=u'Cash')
    onlineAcct = models.FloatField(default=0, verbose_name=u'Online Account')

class Residence(models.Model):
    char = models.ForeignKey(Character, related_name='residence', unique=True)
    resDetails = models.CharField(max_length=500, default='None', verbose_name=u'Residence Details')
    districtLoc = models.CharField(max_length=500, default='None', verbose_name=u'District Location')
    Type = models.CharField(max_length=500, default='None', verbose_name=u'Type')
    rent = models.CharField(max_length=500, default='None', verbose_name=u'Rent')

class UserProfile(models.Model):
    user = models.ForeignKey(User, related_name='profile', unique=True)
    chatzyname = models.CharField(max_length=50, null=True, blank=True)
    AIM_Skype = models.CharField(max_length=50, null=True, blank=True)
    def __unicode__(self):
        return self.user
