from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index_default'),
    path('index/', views.index, name='index'),
    path('resume/', views.resume, name='resume'),
    path('projects/', views.projects, name='projects'),
    path('blog/', views.article_list, name='blog'),
    path('blog/article/<int:id>/', views.article_detail, name='article_detail'),
    path('contact/', views.contact, name='contact'),
    path('contact/send_message/', views.send_message, name='contact'),
    path('increase-likes/<int:id>/', views.IncreaseLikesView.as_view(), name='increase_likes'),

]