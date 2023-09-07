from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404

# Create your views here.
def index(request):
    '''The home page'''
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    '''Show all topics page'''
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context=context)

@login_required
def topic(request, topic_id):
    '''Show a single topic page'''
    topic = Topic.objects.get(id=topic_id)
    # Make sure the topic belongs to the current user
    if topic.owner != request.user:
        raise Http404
    
    entries = topic.entry_set.order_by('-date_added')
    context = {'entries': entries, 'topic': topic}
    return render(request, 'learning_logs/topic.html', context=context)

@login_required
def new_topic(request):
    '''New topic page'''
    if request.method != 'POST':
        # No data submitted; Create a blank form
        form = TopicForm()
    else:
        # POST data submitted; process data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
    
    # Display a blank or invalid form
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context=context)

@login_required
def new_entry(request, topic_id):
    '''New entry page for one topic'''
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # No data submitted; Create a blank form
        form = EntryForm()
    else:
        # POST data submitted; process data
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topics = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
        
    # Display a blank or invalid form
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context=context)

@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topics
    if topic.owner != request.user:
        raise Http404

    if request.method !='POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(data=request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id = topic.id)
    context = {'topic': topic, 'entry': entry, 'form':form}
    return render(request, 'learning_logs/edit_entry.html', context=context)


