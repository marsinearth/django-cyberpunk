from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth import logout
from cyberpunk.forms import *
from cyberpunk.models import *
from google.appengine.api import mail
from django.contrib import messages 
from datetime import datetime

def register_page(request):
  if request.method == 'POST':
    regform = RegistrationForm(request.POST)
    userform = UserProfileForm(request.POST)
    if regform.is_valid() and userform.is_valid():
      user = User.objects.create_user(
        username=regform.cleaned_data['username'],
        password=regform.cleaned_data['password1'],
        email=regform.cleaned_data['email']        
        )
      userprofile = UserProfile.objects.create(
        user = user,        
        AIM_Skype = userform.cleaned_data['AIM_Skype'],
        chatzyname = userform.cleaned_data['chatzyname'] 
        )                                         
      return HttpResponseRedirect('/register/success/')
  else:
    regform  = RegistrationForm()
    userform = UserProfileForm()    
  variables = {
    'regform' : regform,
    'userform': userform
    }
  return render(request,
    'registration/register.djhtml', variables
    )

def main_page(request):  
  return render(request, 'main_page.djhtml')

def user_page(request):  
  return render(request, 'user_page.djhtml')    

@login_required
def useredit(request, id):
  userprof = get_object_or_404(UserProfile, pk=id)
  if request.method == 'POST':
    userprofileform = UserProfileForm(request.POST, instance=userprof)
    if userprofileform.is_valid():
      userprofileform.save()
      return HttpResponseRedirect('/user/')
  else:
    userprofileform = UserProfileForm(instance=userprof)
  variables = {
    'form': userprofileform,
    }
  return render(request,
    'registration/userprof_edit.djhtml', variables
    )

@login_required
def character_page(request, charname):
  try:
    chardata = Character.objects.filter(name=charname)
    charobj = Character.objects.get(name=charname)
    charobj.collect_skillpts() #calculate skill points
    charobj.collect_contactpts() #calculate contact points 
  except Character.DoesNotExist:
    raise Http404(u'Requested character not found.')
  eqWeaponList = charobj.weapon.filter(equipped=True)
  unEqWeaponList = charobj.weapon.filter(equipped=False)
  unEqArmorList = charobj.armor.filter(equipped=False)
  eqArmorHead = charobj.armor.filter(Category='Head', equipped=True)
  eqArmorTorso = charobj.armor.filter(Category='Torso', equipped=True)
  eqArmorLA = charobj.armor.filter(Category='Left Arm', equipped=True)
  eqArmorRA = charobj.armor.filter(Category='Right Arm', equipped=True)
  eqArmorLL = charobj.armor.filter(Category='Left Leg', equipped=True)
  eqArmorRL = charobj.armor.filter(Category='Right Leg', equipped=True)
  eqVehicleList = charobj.vehicle.filter(equipped=True)
  unEqVehicleList = charobj.vehicle.filter(equipped=False)
  eqCyberBioList = charobj.cyber_bio.filter(equipped=True)
  unEqCyberBioList = charobj.cyber_bio.filter(equipped=False)
  benefits = charobj.effects.filter(Category='benefit')
  penalties = charobj.effects.filter(Category='penalty')
  specials = charobj.skills.filter(Category='special')
  attrs = charobj.skills.filter(Category='attr')
  bodies = charobj.skills.filter(Category='body')
  cools = charobj.skills.filter(Category='cool')
  empathies = charobj.skills.filter(Category='empathy')
  ints = charobj.skills.filter(Category='int')
  techs = charobj.skills.filter(Category='tech')
  refs = charobj.skills.filter(Category='ref')

  variables = {
      'chardata' : chardata,
      'charobj'  : charobj,
      'eqweapons': eqWeaponList,
      'unEqweapons': unEqWeaponList,
      'unEqarmors': unEqArmorList,
      'eqhead'   : eqArmorHead,
      'eqtorso'  : eqArmorTorso,
      'eqLA'     : eqArmorLA,
      'eqRA'     : eqArmorRA,
      'eqLL'     : eqArmorLL,
      'eqRL'     : eqArmorRL,
      'eqvehicle': eqVehicleList,
      'unEqvehicle': unEqVehicleList,
      'eqcyberbio':eqCyberBioList,
      'unEqcyberbio':unEqCyberBioList,
      'benefits' : benefits,
      'penalties': penalties,
      'specials' : specials,
      'attrs'    : attrs,
      'bodies'   : bodies,
      'cools'    : cools,
      'empathies': empathies,
      'ints'     : ints,
      'techs'    : techs,
      'refs'     : refs,
      }
  return render(request, 'character_page.djhtml', variables)

# function for conducting mailing message
def sendmsg(form, char, mail, request, category=None):
  if category:
    obj = category
  else:
    obj = 'stats'
  message = 'Please edit '+obj+' of '+char.name+' as below: \n\n'
  for key, value in request.POST.iteritems():
    if not 'csrf' in key and key in form.changed_data:
      if obj == "lifepath" and not 'age' in form.changed_data:
        message += 'Age: 16,\n'
      message += key.title()+': '+value+',\n'
  message += '\nThank you!\n\nTo go to the admin site, click this: http://cyberpunkadminpage/character/'+str(char.id)
  msg =  mail.EmailMessage(sender='admin@email',  #sender
                           subject='Cyberpunk '+obj.title()+' Edit Request from '+char.name) #subject
  msg.to='admin@email' #recipient
  msg.body=message #message                                
  msg.send()

@login_required
def charedit(request, id=None):  

  if id:
    char = get_object_or_404(Character, pk=id)  
    if char.user != request.user:
      raise PermissionDenied() 
  else:
    char = Character(user=request.user)              

  if request.method == 'POST':   
    # request.POST to each form
    charform = CharacterForm(request.POST, instance=char)        
    statform = StatFormSet(request.POST, instance=char, prefix='stat')
    moneyform = MoneyFormSet(request.POST, instance=char, prefix='money')
    resform = ResFormSet(request.POST, instance=char, prefix='res')
    
    if charform.is_valid():
      instance = charform.save(commit=False)      
      #      est = pytz.timezone('US/Eastern')
      if id:                        
        # modified time saving
        instance.modified = datetime.now().strftime('%Y-%m-%d %H:%M')
        instance.save()
      else:
        # created time saving
        instance.created = datetime.now().strftime('%Y-%m-%d %H:%M')
        instance.save() # save char          
            
      # saving forms
      if statform.is_valid() and moneyform.is_valid() and resform.is_valid():
        if char.locked and statform.has_changed(): #only if statform is being edited
          # send email to admin 
          sendmsg(statform, char, mail, request)    
          messages.success(request, 'Stats Edit Request Email has been sent to Admin.', extra_tags='stat')
          # save other forms anyway
          moneyform.save()
          resform.save()
        else:
          statform.save()
          moneyform.save()
          resform.save()
                  
        return HttpResponseRedirect('/character/'+instance.name)
  else:    
    charform = CharacterForm(instance=char)      
    statform = StatFormSet(instance=char, prefix='stat')
    moneyform = MoneyFormSet(instance=char, prefix='money')
    resform = ResFormSet(instance=char, prefix='res')    

  variables = {
      'charform' : charform,      
      'statform' : statform,
      'moneyform' : moneyform,
      'resform' : resform,
      }
  return render(request,
    'registration/character_registration.djhtml', variables
    )

def chardelete(request, id):
  char = get_object_or_404(Character, pk=id)
  if char.user != request.user:
    raise PermissionDenied()
  char.delete()
  return HttpResponseRedirect('/user')

category_dict = {"skill": (Skill, SkillForm), "effect": (Effect, EffectForm), "lifepath": (LifePath, LifePathForm), "cyber_bio":  (Cyber_Bio, Cyber_BioForm), "equipment": (Equipment, EquipmentForm), "wound": (Wound, WoundForm), "contact": (Contact, ContactForm), "weapon": (Weapon, WeaponForm), "armor": (Armor, ArmorForm), "vehicle": (Vehicle, VehicleForm)}

@login_required
def editobj(request, charname, category, id=None, cat_dict=category_dict):  
  try:
    char = Character.objects.get(name=charname)
  except Character.DoesNotExist:
    raise Http404(u'Character not found')
  #get the index digit for objects or forms from the input category
  if category in cat_dict:
    if char.locked and category in ["skill", "effect", "lifepath"]:
      lockmsg = True
    else:
      lockmsg = False

  if id:
    obj = get_object_or_404(cat_dict[category][0], pk=id)
  else:
    obj = cat_dict[category][0](char=char)

  if request.method == 'POST':
    form = cat_dict[category][1](request.POST, instance=obj)    
    #form validity  
    if form.is_valid():
      if lockmsg:
        sendmsg(form, char, mail, request, category)
        messages.success(request, category.title()+' Edit Request Email has been sent to Admin.', extra_tags=category)
      else:        
        form.save()      

      # if equipping an armor
      # if index == 8 and form.fields['equipped']:
      #   armorcat = obj.Category
      #   eqArmor = char.armor.filter(Category=armorcat, equipped=True)
      #   if len(eqArmor) > 0:
      #     for armor in eqArmor:
      #       if armor != obj: 
      #         armor.equipped = False
      #         armor.save()

      # if equipping a vehicle
      if category == "vehicle" and form.fields['equipped']:
        eqVehicle = char.vehicle.filter(equipped=True)
        if len(eqVehicle) > 0:
          for vehicle in eqVehicle:
            if vehicle != obj:
              vehicle.equipped = False
              vehicle.save()
      return HttpResponseRedirect('/character/'+charname)
  else:
    form = cat_dict[category][1](instance=obj)
  variables = {
      'form' : form,
      'obj'  : obj,
      'charname'  : charname,
      'charlock' : lockmsg,
      }
  return render(request,
    'registration/object_registration.djhtml', variables
    )          

@login_required
def deleteobj(request, charname, category, id, cat_dict=category_dict):
  try:
    char = Character.objects.get(name=charname)
  except Character.DoesNotExist:
    raise Http404(u'Character not found')
  if category in cat_dict:
    obj = get_object_or_404(cat_dict[category][0], pk=id)
    obj.delete()
  return HttpResponseRedirect('/character/'+charname)

@login_required
def equipobj(request, charname, category, id, cat_dict=category_dict):
  try:
    char = Character.objects.get(name=charname)
  except Character.DoesNotExist:
    raise Http404(u'Character not found')  
  
    # paramArmor = get_object_or_404(Armor, pk=id)
    # paramCat = paramArmor.Category
    # eqArmor = char.armor.filter(equipped=True)
    # for armor in eqArmor:
    #   if armor.Category == paramCat:
    #     armor.equipped = False
    #     armor.save()
  if category == 'vehicle':
    eqVehicle = char.vehicle.filter(equipped=True)
    if len(eqVehicle) >= 1:
      for vehicle in eqVehicle:
        vehicle.equipped = False  
        vehicle.save()

  obj = get_object_or_404(cat_dict[category][0], pk=id)
  obj.equipped = True
  obj.save()
  return HttpResponseRedirect('/character/'+charname)

@login_required
def unequipobj(request, charname, category, id, cat_dict=category_dict):  
  obj = get_object_or_404(cat_dict[category][0], pk=id)
  obj.equipped = False
  obj.save()
  return HttpResponseRedirect('/character/'+charname)

def logout_page(request):
  logout(request)
  return HttpResponseRedirect('/')
