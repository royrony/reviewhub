"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from formapp.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/',login,name='login'),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^post/new/$',post_new, name='post_new'),
    url(r'^$',index,name='index'),
    url(r'^delete/(\d+)/$',delete,name='delete'),
    url(r'^search/$',search),
    url(r'^detail/(\d+)/$',detail,name='detail'),
    url(r'^edit/(\d+)/$',edit,name='edit'),
    url(r'^register/$',register,name='register'),
    url(r'^auth_check/$',auth_view,name='check'),
    url(r'^logged_in/$',loggedin),
    url(r'^invalid/$',invalid),
    url(r'^logout/$',logout),
    url(r'^profile/$',profile,name='profile'),
    url(r'^password/$',password,name='password'),
    url(r'^post/$',post,name='post'),
    url(r'^profiledisp/$',profiledisp,name='profiledisp'),
    url(r'^about/$',about,name='about'),
    url(r'^contact/$',contact,name='contact'),
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^orders/', include('orders.urls', namespace='orders')),
    url(r'^shop/', include('shop.urls', namespace='shop')),
    url(r'^ratings/', include('star_ratings.urls', namespace='ratings', app_name='ratings')),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$',post, name='post_list_by_tag'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),  # <--
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^category/(?P<category_slug>[-\w]+)/$',post, name='list_of_post_by_category')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
