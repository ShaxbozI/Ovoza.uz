from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.db.models.query import QuerySet
from django.db.models import Q
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.views import View
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.views.generic import ListView, DetailView, TemplateView

from newsapp.forms import ContactForm, CommentForm, CustomAdminAddNewsForm, CustomAdminAddNewsAudioForm, CustomAdminAddNewsVideoForm
from newsapp.models import Category, News
from ovoza.custom_permissions import OnlyLoogedSuperUser


from hitcount.views import HitCountMixin
from hitcount.utils import get_hitcount_model
from django.db.models import Count
from django.db.models import ExpressionWrapper, F, IntegerField



#  Function View 
def home_page(request):
    categories = Category.objects.all()
    news_list = News.published.all().filter(img = True).order_by('-publish_time')
    local_news = News.published.all().filter(category__name_uz = 'Mahalliy', img = True)[:5]
    global_news = News.published.all().filter(category__name_uz = 'Xorijiy', img = True)[:5]
    sport_news = News.published.all().filter(category__name_uz = 'Sport', img = True)[:5]
    technical_news = News.published.all().filter(category__name_uz = 'Fan-Texnika', img = True)[:5]
    
    context = {
        'news_list': news_list, 
        'categories': categories,
        'local_news': local_news,
        'global_news': global_news,
        'sport_news': sport_news,
        'technical_news': technical_news,
        }
    return render(request, 'home.html', context)



def categoryView(request):
    category = Category.objects.all()
    news_list = News.published.filter (img = True).order_by('-publish_time')
    local_news = News.published.all().filter(category__name_uz = 'Mahalliy', img = True)[:6]
    global_news = News.published.all().filter(category__name_uz = 'Xorijiy', img = True)[:6]
    sport_news = News.published.all().filter(category__name_uz = 'Sport', img = True)[:6]
    technical_news = News.published.all().filter(category__name_uz= 'Fan-Texnika', img = True)[:6]
    context = {
        'categories': category,
        'news_list': news_list,
        'local_news': local_news,
        'global_news': global_news,
        'sport_news': sport_news,
        'technical_news': technical_news
        }
    return render(request, 'category.html', context)



def contactView(request):
    news_list = News.published.all().filter( img = True)
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return HttpResponse('<h2> Xabaringiz yuborildi </h2>')
    
    context = { 'form': form, 'news_list': news_list}
    return render(request, 'contact.html', context)



def news_detail(request, news):
    news_list = News.published.all().filter( img = True)
    news = get_object_or_404(News, slug = news, status = News.Status.Published)
    context = {}
    # hitcount 
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    
    
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits
        news.view_count = hits
        news.save()
    comments = news.comments.filter(active = True)
    new_comment = None
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # yangi comment hosil qilamiz ammo DB ga saqlamaymiz
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            # izoh egasini so'rov yuborgan userga bog'laymiz
            new_comment.user = request.user
            # yangi izohni DBga saqlaymiz
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    context = {
        'news':news, 
        'news_list':news_list,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        }
    return render(request, 'news/news_detail.html', context)



# Cass View
class AboutView(TemplateView):
    model = News
    template_name = 'about.html'
    
    def get_context_data(self):
        news_list = News.published.all().filter( img = True)
        context = {'news_list': news_list}
        return context
    
    
    
class LatestNewsView(ListView):
    model = News
    template_name = 'latest_news.html'
    
    def get_context_data(self, **kwargs):
        news_list = News.published.all().filter( img = True)[:10]
        context = {'news_list': news_list}
        return context
    
    
    
class MediaNewsView(ListView):
    model = News
    template_name = 'media_news.html'
    
    def get_context_data(self, **kwargs):
        video_news = News.published.all().filter(video = True).order_by('-publish_time')[:10]
        audio_news = News.published.all().filter(audio = True).order_by('-publish_time')[:10]
        news_list = News.published.all().filter( img = True)
        context = {'video_news': video_news, 'audio_news': audio_news, 'news_list': news_list}
        return context     


    
class NewsCreateView(OnlyLoogedSuperUser, View):
    def get(self, request, form):
        nesw_form = CustomAdminAddNewsForm()
        audio_form = CustomAdminAddNewsAudioForm()
        video_form = CustomAdminAddNewsVideoForm()
        context = {'nesw_form': nesw_form, 'audio_form': audio_form, 'video_form': video_form}
        return render(request, 'news/news_create.html', context)
    
    def post(self, request, form):
        nesw_form = CustomAdminAddNewsForm()
        audio_form = CustomAdminAddNewsAudioForm()
        video_form = CustomAdminAddNewsVideoForm()
        
        if form == 'news':
            nesw_form = CustomAdminAddNewsForm(data = request.POST, files=request.FILES)
            if nesw_form.is_valid():
                nesw_form.save()
        if form == 'audio':
            audio_form = CustomAdminAddNewsAudioForm(data = request.POST, files=request.FILES)
            if audio_form.is_valid():
                audio_form.save()
        if form == 'video':
            video_form = CustomAdminAddNewsVideoForm(data = request.POST, files=request.FILES)
            if video_form.is_valid():
                video_form.save()
        
        context = {'nesw_form': nesw_form, 'audio_form': audio_form, 'video_form': video_form}
        return render(request, 'news/news_create.html', context)
    
    
    
class NewsUpdateView(OnlyLoogedSuperUser, View):
    def get(self, request, form, slug):
        news = News.published.all().get(slug = slug)
        if form == 'news':
            forms = CustomAdminAddNewsForm(instance = news)
            wich_news = 'news'
        if form == 'audio':
            forms = CustomAdminAddNewsAudioForm(instance = news)
            wich_news = 'audio'
        if form == 'video':
            forms = CustomAdminAddNewsVideoForm(instance = news)
            wich_news = 'video'
        context = {'forms': forms, 'news': news, "wich_news": wich_news}
        return render(request, 'news/news_edit.html', context)
    
    def post(self, request, form, slug):
        news = News.published.all().get(slug = slug)
        if form == 'news':
            nesw_form = CustomAdminAddNewsForm(instance = news, data = request.POST, files=request.FILES)
            if nesw_form.is_valid():
                forms = nesw_form.save()
                
            news_list = News.published.all().filter( img = True)
            context = {'news_list': news_list}
            return render(request, 'home.html', context)
        
        if form == 'audio':
            audio_form = CustomAdminAddNewsAudioForm(instance = news, data = request.POST, files=request.FILES)
            if audio_form.is_valid():
                forms = audio_form.save()
                
            video_news = News.published.all().filter(video = True).order_by('-publish_time')[:10]
            audio_news = News.published.all().filter(audio = True).order_by('-publish_time')[:10]
            context = {'video_news': video_news, 'audio_news': audio_news,}
            return render(request, 'media_news.html', context)
        
        if form == 'video':
            video_form = CustomAdminAddNewsVideoForm(instance = news, data = request.POST, files=request.FILES)
            if video_form.is_valid():
                forms = video_form.save()
            video_news = News.published.all().filter(video = True).order_by('-publish_time')[:10]
            audio_news = News.published.all().filter(audio = True).order_by('-publish_time')[:10]
            context = {'video_news': video_news, 'audio_news': audio_news,}
            return render(request, 'media_news.html', context)
                
    
    
class NewsDeleteView(OnlyLoogedSuperUser, DeleteView):
    model = News
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('home')

    
    
class SearchResultView(ListView):
    model = News
    template_name = 'search_result.html'
    context_object_name = 'yangiliklar'
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.published.all().filter(
            Q(title__icontains = query) | Q(body__icontains = query)
        )
