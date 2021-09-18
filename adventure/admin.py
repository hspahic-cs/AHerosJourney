from django.contrib import admin

from .models import Choice, Video, Chunk, ChoicePossibility

# Register your models here.
# Displays each model as its __str__ representation in local:8000/admin
admin.site.register(Choice)
admin.site.register(Video)
admin.site.register(Chunk)
#admin.site.register(ChoicePossibility)


'''
Hijacked ChoicePossibility display 
--> Choice references ChoicePossibility __str__
--> ChoicePossibility admin displays each ChoicePossibility path

**Easier to double check inputs**
'''
@admin.register(ChoicePossibility)
class ChoicePossibilityAdmin(admin.ModelAdmin):
    list_display = ['imgPath']
