from django import forms
from django.db.models import fields
from .models import TopicModel, EntryModel

class TopicForm(forms.ModelForm):
    class Meta:
        model = TopicModel
        fields = ["text"]
        labels = {"text": ""}

class EntryForm(forms.ModelForm):
    class Meta:
        model = EntryModel
        fields = ["text"]
        labels = {"text": ""}
        widgets = {"text": forms.Textarea(attrs={'cols': 80})}