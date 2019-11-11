from django.contrib import admin

# Register your models here.

from .models import (Account, Pictures,
    SalesTerm, Attributes, PublicationData,
    Description, OrigintoCopy)

@admin.register(Account, Pictures, SalesTerm, 
        Attributes, PublicationData, Description,
        OrigintoCopy)
class AuthorAdmin(admin.ModelAdmin):
    pass    