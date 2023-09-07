from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.
def index(request):
    '''The home page'''
    return render(request, 'learning_logs/index.html')

def topics(request):
    '''Show all topics page'''
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context=context)

def topic(request, topic_id):
    '''Show a single topic page'''
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'entries': entries, 'topic': topic}
    return render(request, 'learning_logs/topic.html', context=context)

def new_topic(request):
    '''New topic page'''
    if request.method != 'POST':
        # No data submitted; Create a blank form
        form = TopicForm()
    else:
        # POST data submitted; process data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')
    
    # Display a blank or invalid form
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context=context)

def new_entry(request, topic_id):
    '''New entry page for one topic'''
    topic = Topic.objects.get(id=topic_id)

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

def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topics

    if request.method !='POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(data=request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id = topic.id)
    context = {'topic': topic, 'entry': entry, 'form':form}
    return render(request, 'learning_logs/edit_entry.html', context=context)


