from django.db import models

# Create your models here.
class Topic(models.Model):
    '''Class for the topic the user is learning about'''
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Return a string representation of the model'''
        return self.text
    
class Entry(models.Model):
    '''Class for something specific learnt about the topic'''
    topics = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self) -> str:
        return f'{self.text[:50]}...'
