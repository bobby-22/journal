from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from .models import TopicModel, EntryModel
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db.models import Count
 
# Create your views here.
def index(request):
    return render(request, "boards/index.html")

@login_required
def topics(request):
    topics = TopicModel.objects.filter(owner=request.user).all()
    topic_contents = TopicModel.objects.filter(owner=request.user).annotate(number_of_entries=Count('entrymodel'))

    context = {"topics": topics, "topic_contents": topic_contents}
    return render(request, "boards/topics.html", context)

@login_required
def topic(request, topic_id):
    topic = TopicModel.objects.get(id=topic_id)
    entries = topic.entrymodel_set.order_by("-date_added")

    if topic.owner != request.user:
        raise Http404

    context = {"topic": topic, "entries": entries}
    return render(request, "boards/topic.html", context)

@login_required
def new_topic(request):
    if request.method != "POST":
        form = TopicForm()

    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect("boards:topics")

    context = {"form": form}
    return render(request, "boards/new_topic.html", context)

@login_required
def delete_topic(request, topic_id):
    if request.method == "GET":
        topic = TopicModel.objects.get(id=topic_id)
        topic.delete()
        return redirect("boards:topics")

    return render(request, "boards/topics.html")

@login_required
def new_entry(request, topic_id):
    topic = TopicModel.objects.get(id=topic_id)

    if request.method != "POST":
        form = EntryForm()

    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect("boards:topic", topic_id=topic.id)

    context = {"topic": topic, "form": form}
    return render(request, "boards/new_entry.html", context)

@login_required
def delete_entry(request, entry_id):
    if request.method == "GET":
        entries = EntryModel.objects.get(id=entry_id)
        entries.delete()
        return redirect("boards:topic", topic_id=entries.topic.id)
    
    return redirect(request, "boards/topic.html")

@login_required
def edit_entry(request, entry_id):
    entry = EntryModel.objects.get(id=entry_id)
    topic = entry.topic

    if topic.owner != request.user:
        raise Http404

    if request.method != "POST":
        form = EntryForm(instance=entry)
    
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("boards:topic", topic_id=topic.id)
    
    context = {"entry": entry, "form": form}
    return render(request, "boards/edit_entry.html", context)
