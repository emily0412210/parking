# from django.db.models import BaseManager
from django.contrib.auth.models import BaseUserManager



class AdminManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role="admin")

class DriverManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role="driver")

class OwnerManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role="owner")