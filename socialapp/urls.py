from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup', views.register, name='register'),
    path('register', views.createUser, name='createUser'),
    path('login', views.login, name='login'),
    path('auth', views.auth, name='auth'),
    path('dash', views.dash, name='Dash'),
    path('feed', views.feed, name='feed'),
    path('posts', views.posts, name='posts'),
    path('epost/<pk>', views.edit_post, name='Editposts'),
    path('cpost', views.create_post, name='Createposts'),
    path('vpost', views.view_post, name='viewposts'),
    path('upost', views.update_post, name='updatepost'),
    path('dpost/<pk>', views.delete_post, name='deletepost'),
    path('logout', views.logout, name='logout'),
    path('myprofile', views.myprofile, name='myprofile'),
    path('search', views.search, name='search'),

  
    
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)