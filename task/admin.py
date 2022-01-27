from django.contrib import admin
from django.contrib.admin import register, ModelAdmin
from task.models import User, Checkpoint, Claim, SubscribedPoints

# Register your models here.

admin.site.site_header = 'Harri Task'
admin.site.index_title = 'Harri Task'
admin.site.site_title = 'Harri Task'


@register(Claim)
class ClaimAdmin(ModelAdmin):
    readonly_fields = ('timestamp',)


admin.site.register(User)
admin.site.register(Checkpoint)
admin.site.register(SubscribedPoints)

# @register(User)
# class UserAdmin(ModelAdmin):
