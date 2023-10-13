from django.urls import path
# from .views import perform_backend_action
from .views import (
    # news_list,
    news_detail,
    home_page,
    categoryView,
    contactView,
    AboutView,
    LatestNewsView,
    NewsCreateView,
    NewsUpdateView,
    NewsDeleteView,
    SearchResultView,
    MediaNewsView,
    # NewsListView,
    # NewsDetailView,
)

urlpatterns = [
    path('', home_page, name = 'home'), 
    path('about/', AboutView.as_view(), name = 'about'),
    path('latest_news/', LatestNewsView.as_view(), name = 'latest_news'),
    path('category/', categoryView, name = 'category'),
    path('contact/', contactView, name = 'contact'),
    path('create/<str:form>/', NewsCreateView.as_view(), name= 'create'),
    path('media/', MediaNewsView.as_view(), name='media_news'),
    path('news/<slug:news>/', news_detail, name = 'news_detail'),
    path('edit/<str:form>/<slug>/', NewsUpdateView.as_view(), name= 'edit'),
    path('news/<slug>/delete/', NewsDeleteView.as_view(), name= 'delete'),
    path('search/', SearchResultView.as_view(), name='search_result'),
]