try:
    from urllib import quote_plus #python 2
except:
    pass

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.models import User
from .forms import PropertyForm,ImageForm,UchoiceForm,LikeForm,Mesajform
from .models import Property,Images,UserProperty,Like,Mesaj

def property_create(request):
	if not request.user.is_authenticated:
		raise Http404
		
	form = PropertyForm(request.POST or None, request.FILES or None)
	form2 = ImageForm(request.POST or None,request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		instance2 = form2.save(commit=False)
		instance2.prop1_id = instance.id
		instance2.save()
		# message success
		messages.success(request, "Successfully Created")
		return HttpResponseRedirect(instance.get_url())
	context = {
		"form": form,
		"form2":form2
	}
	return render(request, "property_add.html", context)

def property_detail(request, id=None):
	instance = get_object_or_404(Property,id=id)
	instance1 = Images.objects.filter(prop1_id=id)
	userid=request.user.id
	instance2 = Like.objects.filter(prop_id=id,vote=1,user_id=userid)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_authenticated:
			raise Http404
    #commentli kisimlar like i denemek icindir
	#if form.is_valid():
		#instance2=form.save(commit=False)
		#instance2.user=request.user
	#	instance2.save()		
	share_string = quote_plus(instance.prop_desc.encode('utf-8'))
	context = {
		"title": instance.title,
		"instance": instance,
		"share_string": share_string,
		"instance1":instance1,
		"instance2":instance2,
		#"form":form,
	}

	return render(request, "property_detail.html", context)

def property_list(request):
	today = timezone.now().date()
	queryset_list = Property.objects.active() #.order_by("-timestamp")
	if not request.user.is_authenticated:
		queryset_list = Property.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(prop_desc__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	


	context = {
		"object_list": queryset_list, 
		"title": "List",
		"today": today,

	}

	return render(request, "index.html", context)





def property_update(request, id=None):
	if not request.user.is_authenticated:
		raise Http404
	instance = get_object_or_404(Property, id=id)
	form = PropertyForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
		return HttpResponseRedirect(instance.get_url())

	context = {
		"title": instance.title,
		"instance": instance,
		"form":form,
	}

	return render(request, "property_edit.html", context)



def property_delete(request, id=None):
	if not request.user.is_authenticated:
		raise Http404
	instance = get_object_or_404(Property, id=id)
	instance.delete()
	messages.success(request, "Successfully deleted")
	return redirect("list")


def user_preferences(request):
	id=request.user.id
	instance = get_object_or_404(UserProperty,user_id=id)
	form = UchoiceForm(request.POST or None,request.FILES or None,instance=instance)
	
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		# message success
		messages.success(request, "Successfully Saved")
		return HttpResponseRedirect("usersee.html")
	context = {
		"form": form,
	
	}
	return render(request, "userpreference.html", context)

def user_preferences2(request):#ilk kayit olan user icin
	id=request.user.id
	form = UchoiceForm(request.POST or None,request.FILES or None)
	
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user_id=id
		instance.save()
		# message success
		messages.success(request, "Successfully Saved")
		return redirect("usersee")
	context = {
		"form": form,
	
	}
	return render(request, "userpreference.html", context)

def user_see(request):
	id=request.user.id
	try:
		instance = UserProperty.objects.get(user_id=id)
		context = {"instance":instance,}
		return render(request,"user_see.html",context)
	except:
		return HttpResponseRedirect("userpre2")
	


def favorites(request):
	id=request.user.id
	instance  = Like.objects.filter(user_id=id,vote=1)
	likes = list()

	for e in instance:

		instance2 = Property.objects.get(id=e.prop_id)
		likes.append(instance2)

	
	context = {
			   "object_list":likes,



	}
	return render(request,"favorites.html",context)	



def likepage(request):
	id = request.user.id
	instanceuser = get_object_or_404(UserProperty,user_id=id)
	instanceprop = Property.objects.all()
	score = 0
	likes = list()
	for e in instanceprop:
		score = 0
		if instanceuser.umetrekaremin<e.metrekare and e.metrekare<instanceuser.umetrekaremax:
			score = score+1
		else:
			score = score - 1	

			
		if instanceuser.upricemin<e.price and e.price<instanceuser.upricemax:
			score = score +1	

		else:
			score = score - 1	


		if instanceuser.ufloornumber == e.floornumber+1 or instanceuser.ufloornumber == e.floornumber-1 or instanceuser.ufloornumber == e.floornumber: 
			score = score +1	

		else:
			score = score - 1		

		if instanceuser.ubuildingage>=e.buildingage :
			score = score +1	

		else:
			score = score - 1		
			
		if instanceuser.uheating_choice==e.heating_choice :
			score = score +1	

		else:
			score = score - 1		

		if instanceuser.usale_choice==e.sale_choice :
			score = score +1	

		else:
			score = score - 1	

		if instanceuser.uroomnumber==e.roomnumber or instanceuser.uroomnumber<e.roomnumber :
			score = score +1	

		else:
			score = score - 1		
		
				
		print score
		if score>4 :
			instance2 = Property.objects.get(id=e.id)
			likes.append(instance2)
			try:
				instancelike=Like.objects.get(prop_id=e.id,user_id=id,vote=1)
				if instancelike:
					likes.remove(instance2)
					
			except:
				pass
					

			

			

	context={"object_list":likes,}
	print context			
	return render(request,"likepage.html",context)		



def mesaj(request,id=None):
	idsender=request.user.id
	form = Mesajform(request.POST)

	if form.is_valid():
		instance = form.save(commit=False)
		instance.sender_id = idsender
		instance.reciever_id=id
		instance.time= timezone.now().date()
		instance.save()

	context = {
		"form": form,
		
	}
	return render(request, "sendmessage.html", context)	


def mesajinbox(request):
	instance = Mesaj.objects.filter(reciever=request.user)
	context={"instance":instance,}
	return render(request,"mymessage.html",context)	

def mesajdelete(request,id=None):
	instance = get_object_or_404(Mesaj,id=id)
	instance.delete()
	#messages.succcess(request,"Successfully Deleted")
	return redirect("/property/message/")	

def reply(request,id=None):
	idsender=request.user.id
	form = Mesajform(request.POST)
	

	if form.is_valid():
		instance=form.save(commit=False)
		instance.sender_id=idsender
		instance.reciever_id=id	
		instance.time= timezone.now().date()
		instance.save()

	context = {
		"form": form,
		
	}
	return render(request, "sendmessage.html", context)	

@login_required
def Likeadd(request,id=None):
	instancep = get_object_or_404(Property,id=id)
	userid=request.user.id
	try:
		instance = Like.objects.get(user_id=userid,prop_id=id,vote=0)
		if instance:
			form = LikeForm(request.POST or None, request.FILES or None,instance = instance)
			print userid,id
			print instance.vote
			instance=form.save(commit=False)
			instance.user_id=userid
			instance.prop_id=id
			instance.vote=1
			print instance.vote
			instance.save()
			return redirect("/property/"+id+"/")

	except:
		form = LikeForm(request.POST)
		print userid,id
		if form.is_valid():
			instance2=form.save(commit=False)
			instance2.user=request.user
			instance2.prop=instancep
			instance2.user_id=userid
			instance2.prop_id=id
			instance2.vote=1
			instance2.save()
			return redirect("/property/"+id+"/")
		context = {
		"instancep":instancep,
		"form":form,
		}
	
	

		return render(request, "liked.html", context)
		
	

		

def dislike(request,id=None):
	instance2 = get_object_or_404(Property,id=id)
	instance1 = Images.objects.filter(prop1_id=id)
	userid=request.user.id
	instance = get_object_or_404(Like,prop_id=id,user_id=userid,vote=1)
	print instance
	form = LikeForm(request.POST or None, request.FILES or None,instance = instance)
	print userid,id
	print instance.vote
	instance=form.save(commit=False)
	instance.user_id=userid
	instance.prop_id=id
	instance.vote=0
	print instance.vote
	instance.save()
	
	return redirect("/property/"+id+"/")			


def likepage2(request):
	instanceuser=UserProperty.objects.all()
	instancelike = Like.objects.all()
	userid=request.user.id
	instanceuser1 = get_object_or_404(UserProperty,user_id=userid)
	mylist=list()
	myprop = list()
	for e in instanceuser:
	    if e.user_id==userid:
	    	pass
	    else:
			mylist.append(e.user_id)

	
	print mylist		
	
	i=0
	while i<len(mylist):
		instance =	Like.objects.filter(user_id=mylist[i],vote=1)
		for e in instance:
				instance2 = Property.objects.get(id = e.prop_id)
				try:
					instance3=Like.objects.get(user_id=request.user.id,prop_id=e.prop_id)
					print "a"
				except:
					if instance2 not in myprop:
						myprop.append(instance2)
						print "b"
				
		i=i+1
		

	print myprop	

	context={"object_list":myprop,}
	print context			
	return render(request,"likepage.html",context)		


def myproperty(request):
	myproperty=list()
	instance = Property.objects.all()
	id=request.user.id
	for e in instance:
		try:
			if Property.objects.get(id=e.id,user_id=id):
				instance2=Property.objects.get(id=e.id,user_id=id)
				myproperty.append(instance2)
		except :
			pass
		
			 
		
	context={"object_list":myproperty,}
	print context			
	return render(request,"index.html",context)	


def filtering(request):#methodlari denemek icindir baska herhangi bi yerde kullanilmaz
	id = request.user.id 
	x=Like.objects.filter(user_id=id)
	v=Like.objects.filter(prop_id=4)
	b=UserProperty.objects.get(user_id=id)
	z=0
	if x:
		for e in x:
			y=e.getlikerate()
	if v:
		for e in v:
			z=e.likeproprate()		
	
	print z
	print y
	c=float(b.similarity())/10
	print c
	return HttpResponse(z)
	
def colfilter(request):
	id = request.user.id
	userinbegendikleri=Like.objects.filter(user_id=id)
	digeruserlar=UserProperty.objects.all()
	digeruserlist=list()
	sonuc=0
	for e in digeruserlar:
		if e.user_id==id:
			pass
		else:
			digeruserlist.append(e.user_id)		
	print digeruserlist	
	if userinbegendikleri:
		for e in userinbegendikleri:
			benimortalamabegenmerate=e.getlikerate()
	print benimortalamabegenmerate		
	mylist = list()
	instance = Property.objects.all()
	for e in instance:
		try:
			like=Like.objects.get(prop_id=e.id,user_id=id)
		except:

			i=0
			while i<len(digeruserlist):
					digeruserinevibegenmeratei=0
					try:
						digeruserinevibegenmeratei=Like.objects.get(prop_id=e.id,user_id=digeruserlist[i]).vote
					except:
						pass	
					print digeruserinevibegenmeratei,"digeruserinevibegenmeratei"
					digeruserinbegenmerate=Like.objects.filter(user_id=digeruserlist[i])
					a=0
					for j in digeruserinbegenmerate:
							a=j.getlikerate()
					
					print a,"digeruserinbegenmerate2"		
					birinci = digeruserinevibegenmeratei - a
					print birinci,"birinci1"
					ikinci = UserProperty.objects.get(user_id= digeruserlist[i]).similarity()
					ikinci2 = float(ikinci)/10
					print ikinci2,"ikinci2"
					sonuc = float(birinci * ikinci2)+float(benimortalamabegenmerate)
					print sonuc,"sonuccccc"
					print e.id,"ILAN IDSI ***************************** "
					print digeruserlist[i],"user id *******************************"
					c = 0.6
					if sonuc>c:
						instance=Property.objects.get(id=e.id)
						if instance not in mylist:
							mylist.append(Property.objects.get(id=e.id))
					
					i=i+1							

	print sonuc
	context={"object_list":mylist,}			
	return render(request,"index.html",context)	