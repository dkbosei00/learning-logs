from django.shortcuts import render
from .models import Topic, Entry

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