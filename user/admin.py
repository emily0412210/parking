from django.contrib import admin
from .models import CustomUser,Card,Admin,Owner,Driver


admin.site.register(Card)
admin.site.register(CustomUser)
admin.site.register(Admin)
admin.site.register(Owner)
admin.site.register(Driver)