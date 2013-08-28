from django.db import models
from django.contrib import admin


class House(models.Model):
    address = models.TextField()
    owner = models.OneToOneField("Owner")
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.address

        
class Owner(models.Model):
    name = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

        
class HouseAdmin(admin.ModelAdmin):
    list_display = ["address", "owner", "date_created"]
    search_fields = ["address", "owner"]
    
    
class OwnerAdmin(admin.ModelAdmin):
    list_display = ["name", "date_created"]
    search_fields = ["name"]

    
admin.site.register(House, HouseAdmin)
admin.site.register(Owner, OwnerAdmin)
