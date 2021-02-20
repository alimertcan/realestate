from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.shortcuts import render, get_object_or_404


# Create your models here.
class PropertyManager(models.Manager):
    def active(self, *args, **kwargs):
        # Property.objects.all() = super(PropertyManager, self).all()
        return super(PropertyManager, self).filter(draft=False).filter(publish__lte=timezone.now())

sale_choice = (('Re','Rent'),('Sa','Sale'))
prop_choice = (('Rs','Residance'),('Wp','Workplace'),('Bu','Building'),('Ld','Land'))
heating_choice = (('Do','Dogalgaz'),('So','Soba'),('El','Elektrik'))

usale_choice = (('Re','Rent'),('Sa','Sale'))
uprop_choice = (('Rs','Residance'),('Wp','Workplace'),('Bu','Building'),('Ld','Land'))
uheating_choice = (('Do','Dogalgaz'),('So','Soba'),('El','Elektrik'))

class Property(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=120)
    prop_desc = models.TextField()
    location_desc = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    furnished = models.NullBooleanField()
    roomnumber = models.IntegerField()
    buildingage = models.IntegerField()
    metrekare = models.IntegerField()
    price = models.FloatField()
    floornumber = models.IntegerField()
    DOGALGAZ='Do'
    SOBA ='So'
    ELEKTRIK='El'
    RENT = 'Re'
    SALE = 'Sa'
    RESIDANCE='Rs'
    WORKPLACE ='Wp'
    BUILDING ='Bu'
    LAND = 'Ld'
    heating_choice=models.CharField(max_length=4,choices=heating_choice,default=DOGALGAZ)
    sale_choice = models.CharField(max_length=4,choices=sale_choice,default=RENT)
    prop_choice = models.CharField(max_length=4,choices=prop_choice,default=RESIDANCE)






    objects = PropertyManager()

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_id(self):
        return self.id    

    def get_url(self):
		return reverse("detail",kwargs={"id":self.id})
   

    class Meta:
        ordering = ["-timestamp", "-updated"]

def get_image_filename(instance,filename):
    instance=get_object_or_404(Property,id=1)
    title=instance.title
    slug = slugify(title)
    return "property_images/%s-%s" %(slug ,filename)


class Images(models.Model):
    prop1 = models.ForeignKey('Property')
    image = models.ImageField(upload_to=get_image_filename,verbose_name='Image')



class UserProperty(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    ufurnished = models.NullBooleanField(blank=True, null=True)
    furwchoice=models.IntegerField(blank=True, null=True)
    uroomnumber = models.IntegerField(blank=True, null=True)
    roomwchoice=models.IntegerField(blank=True, null=True)
    ubuildingage = models.IntegerField(blank=True, null=True)
    roomwchoice=models.IntegerField(blank=True, null=True)
    umetrekaremin = models.IntegerField(blank=True, null=True)
    mminwchoice=models.IntegerField(blank=True, null=True)
    umetrekaremax = models.IntegerField(blank=True, null=True)
    mmaxwchoice=models.IntegerField(blank=True, null=True)
    upricemin = models.FloatField(blank=True, null=True)
    pminwchoice=models.IntegerField(blank=True, null=True)
    upricemax = models.FloatField(blank=True, null=True)
    pmaxwchoice=models.IntegerField(blank=True, null=True)
    ufloornumber = models.IntegerField(blank=True, null=True,default=1)
    floorwchoice=models.IntegerField(blank=True, null=True)
    DOGALGAZ='Do'
    SOBA ='So'
    ELEKTRIK='El'
    RENT = 'Re'
    SALE = 'Sa'
    RESIDANCE='Rs'
    WORKPLACE ='Wp'
    BUILDING ='Bu'
    LAND = 'Ld'
    uheating_choice=models.CharField(max_length=4,choices=heating_choice,default=DOGALGAZ)
    usale_choice = models.CharField(max_length=4,choices=sale_choice,default=RENT)
    uprop_choice = models.CharField(max_length=4,choices=prop_choice,default=RESIDANCE)


    def __unicode__(self):
        return unicode(self.user)

    def __str__(self):
        return self.upricemax
	
    def get_url(self):
        return reverse("detail",kwargs={"id":self.id})

    def similarity(self):
        userid=self.user.id
        instance=UserProperty.objects.all()
        instanceuser=UserProperty.objects.get(user_id=userid)
        mylist=list()
        rate=0
        for e in instance:
            if e.user_id==userid:
                pass
            else:
                if -20<(instanceuser.umetrekaremin-e.umetrekaremin)<20:
                    rate = rate+1
                else:
                    rate = rate - 1  
                if -20<(instanceuser.umetrekaremax-e.umetrekaremax)<20:
                    rate = rate+1
                else:
                    rate = rate-1  
                if -20000<(instanceuser.upricemin-e.upricemin)<20000:
                    rate = rate+1
                else:
                    rate = rate - 1   
                if -20000<(instanceuser.upricemax-e.upricemax)<20000:
                    rate = rate+1
                else:
                    rate = rate - 1  
                if -2<(instanceuser.ufloornumber-e.ufloornumber)<2:
                    rate = rate+1
                else:
                    rate = rate-1                                   
                if -2<(instanceuser.uroomnumber-e.uroomnumber)<2:
                    rate = rate+1
                else:
                    rate = rate-1     
                if -2<(instanceuser.ubuildingage-e.ubuildingage)<2:
                    rate = rate+1
                else:
                    rate = rate-1         
                if (instanceuser.usale_choice==e.usale_choice):
                    rate = rate+1
                else:
                    rate = rate-1   
                if (instanceuser.uheating_choice==e.uheating_choice):
                    rate = rate+1
                else:
                    rate = rate-1 

                   
        return rate            
		

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    prop = models.ForeignKey('Property',on_delete=models.CASCADE)
    vote = models.IntegerField(blank=True, null=True)

    def getpropid(self):
        return self.prop

    def getlikerate(self):
        id=self.user_id
        instancelike = Like.objects.filter(user_id=id,vote = 1)
        instancedislike = Like.objects.filter(user_id=id,vote = 0)
        mylike=list()
        mydislike=list()
        for e in instancelike:
            instance2 = Property.objects.get(id=e.prop_id)
            mylike.append(instance2)
        for e in instancedislike:
            instance3 = Property.objects.get(id=e.prop_id)
            mydislike.append(instance3)

        rate = float(len(mylike))/float(len(mylike)+len(mydislike)) 
        return rate

    def likeproprate(self):
        id=self.prop_id 
        instancelike=Like.objects.filter(prop_id=id,vote=1) 
        instancedislike = Like.objects.filter(prop_id=id,vote = 0) 
        mylike=list()
        mydislike=list()
        for e in instancelike:
            mylike.append(e)
        for e in instancedislike:
            mydislike.append(e)

    
        rate = float(len(mylike))/float(len(mylike)+len(mydislike)) 
        return rate    


            
 
class Mesaj(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,related_name = "sender")
    reciever = models.ForeignKey(settings.AUTH_USER_MODEL,related_name = "reciever")
    subject=models.CharField(max_length=140)
    msg_content = models.TextField(max_length = 350)
    time = models.DateTimeField(auto_now=False, auto_now_add=False)
