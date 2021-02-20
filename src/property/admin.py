from django.contrib import admin
from .models import Property,Images,UserProperty,Like,Mesaj
# Register your models here.

class InlineImage(admin.TabularInline):
    model = Images	
    
class Usermodeladmin(admin.ModelAdmin):
	class Meta:
		model = UserProperty
 
class PropertyModelAdmin(admin.ModelAdmin):
	list_display = ["title","timestamp"]
	list_display_links=["timestamp"]
	list_filter=["timestamp"]
	list_editable=["title"]
	search_fields=["title"]
	inlines = [InlineImage]
	class Meta:
		model = Property

class Likemodeladmin(admin.ModelAdmin):
	class Meta:
		model = Like		
	
class mesajmodeladmin(admin.ModelAdmin):
	class Meta:
		model = Mesaj

admin.site.register(Property,PropertyModelAdmin)
admin.site.register(UserProperty,Usermodeladmin)
admin.site.register(Like,Likemodeladmin)
admin.site.register(Mesaj,mesajmodeladmin)