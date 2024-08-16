
from django.contrib import admin
from django.urls import path
from music import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('signup',views.signup,name='signup'),
    path('login',views.login_page,name='login'),
    path('logout',views.logout_page,name='logout'),
    path('search',views.search,name='search'),
    path('music/<str:id>',views.music,name='music'),
    path('profile/<str:id>',views.profile,name='profile'),
    
]