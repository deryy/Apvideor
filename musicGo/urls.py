from django.conf.urls import url
from django.conf.urls.static import static
from . import views

app_name = 'musicGo'

urlpatterns=[
    url(r'^$', views.index, name='index'),
    url(r'material$', views.material, name='material'),
    url(r'music$', views.music, name='music'),
    url(r'result$', views.result, name='result'),
    url(r'tutorial$', views.tutorial, name='tutorial'),
    url(r'imageSave$', views.imageSave, name='imageSave'),
    url(r'getVideo$', views.getVideo, name='getVideo'),
    url(r'getMusicStyle$', views.getMusicStyle, name='getMusicStyle'),
    url(r'getMusicName$', views.getMusicName, name='getMusicName'),
    url(r'ajax$', views.ajax, name='ajax'),
]