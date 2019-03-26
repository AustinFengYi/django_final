from django.contrib import admin
# Register your models here.
from .models import Singer,Album,Category,Song


admin.site.register(Category)
admin.site.register(Singer)
admin.site.register(Album)
admin.site.register(Song)