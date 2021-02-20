from django import forms
from .models import Property,Images,UserProperty,Like,Mesaj

class PropertyForm(forms.ModelForm):
	class Meta:
		model = Property
		fields ='__all__'
		exclude = ['user']
			
class ImageForm(forms.ModelForm):
	image = forms.ImageField(label='Image')
	class Meta:
		model = Images
		fields={'image',}


class UchoiceForm(forms.ModelForm):
	class Meta:
		model = UserProperty
		fields = {"ufurnished","uroomnumber","ubuildingage","umetrekaremin","umetrekaremax","upricemin","upricemax","uheating_choice","usale_choice","uprop_choice"}
		ufurnished = forms.NullBooleanField(required=False,label="Furnished")
    	uroomnumber = forms.IntegerField(required=False,label="RoomNumber")
    	ubuildingage = forms.IntegerField(required=False,label="BuildingAge")
    	umetrekaremin = forms.IntegerField(required=False,label="Square Meters Min")
    	umetrekaremax = forms.IntegerField(required=False,label="Square Meters Max")
    	upricemin = forms.FloatField(required=False,label="Price Min")
    	upricemax = forms.FloatField(required=False,label="Price Max")
    	ufloornumber = forms.IntegerField(required=False,label="FloorNumber")
    #	uheating_choice=forms.ModelChoiceField(queryset=Property.heating_choice.objects.all(),label="Heating")
    #	usale_choice = forms.CharField(required=False,label="Rent Or Sale")
    #	uprop_choice = forms.CharField(required=False,label="Type")


class LikeForm(forms.ModelForm):
	 class Meta:
	 	model=Like
	 	fields={"vote","prop","user"}
	 	vote=forms.IntegerField(required=False)

class Mesajform(forms.ModelForm):
	 class Meta:
	 	model = Mesaj
	 	fields={"subject","msg_content"}	 	