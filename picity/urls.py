from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    url(r'^accounts/profile',views.profile,name='profile'),
    url(r'^new/posts$', views.profile,name='new-post'),
    url(r'^comment/(\d+)',views.comment,name='comment'),
    url(r'^search',views.search_user,name="search_user"),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)