from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
# Create your models here.



class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status = News.Status.Published)


class Category(models.Model):
    name = models.CharField(max_length = 150) 
    def __str__(self):
        return self.name
       
       
       
class News(models.Model):

    class Status(models.TextChoices):
        Draft = 'DF', 'Draft'
        Published = 'PB', 'Published'
    title = models.CharField(max_length = 350)
    slug = models.SlugField(unique=True, blank=True)
    author = models.CharField(max_length=150)
    body = models.TextField(blank=True)
    image = models.ImageField(upload_to = 'news/image', blank=True, null=True)
    video_file = models.FileField(upload_to='news/videos', blank=True, null=True)
    audio_file = models.FileField(upload_to='news/audios', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    publish_time = models.DateTimeField(default = timezone.now)
    created_time = models.DateTimeField(auto_now_add = True)
    updated_time = models.DateTimeField(auto_now = True)
    status = models.CharField(
        max_length = 2,
        choices = Status.choices,
        default = Status.Draft
    )
    view_count = models.IntegerField(default = 0)
    published = PublishedManager()
    audio = models.BooleanField(default=False)
    video = models.BooleanField(default=False)
    img = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(News, self).save(*args, **kwargs)
        
    def __str__(self): 
        return self.title
    
    class Meta:
        ordering = ['-publish_time']

    def get_absolute_url(self):
        return reverse('news_detail', args=[self.slug])
    
    def get_previous_news(self):
        return News.published.filter(publish_time__lt=self.publish_time).order_by('-publish_time').first()

    def get_next_news(self):
        return News.published.filter(publish_time__gt=self.publish_time).order_by('publish_time').first()
    
    
@receiver(pre_save, sender=News)
def generate_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)
    if instance.audio_file:
        instance.audio = True
    else:
        instance.audio = False
        
    if instance.video_file:
        instance.video = True
    else:
        instance.video = False
        
    if instance.image:
        instance.img = True
    else:
        instance.img = False
        


class Contact(models.Model):
    name = models.CharField(max_length = 150)
    email = models.EmailField(max_length = 150)
    message = models.TextField()
    subject = models.CharField(max_length = 150, default="Mavzu nomi")
    
    def __str__(self):
        return self.subject
    
    
class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['created_time']
        
    def __str__(self):
        return f"Comment - {self.body} by {self.user}" 
    

