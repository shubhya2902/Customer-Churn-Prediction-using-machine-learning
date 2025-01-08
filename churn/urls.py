from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('',views.index, name='index'),

    path('signup/', views.signupuser, name="signup"),
    path('login/', views.loginuser, name="login"),
    path('logout/', views.logoutuser, name="logout"),

    path('home/',views.home,name='home'),
    path('users/',views.users,name='users'),
    path('about/', views.about, name='about'),

    path('predict/',views.predict,name="predict"),
    ]


from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
