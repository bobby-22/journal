from django.contrib import admin
from .models import TopicModel, EntryModel

# Register your models here.
admin.site.register(TopicModel)
admin.site.register(EntryModel)