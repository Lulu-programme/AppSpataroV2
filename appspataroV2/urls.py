"""
URL configuration for appspataroV2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import authentication.views
import factory.views
import adr.views
import daytime.views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # home page
    path('admin/', admin.site.urls),
    path('', authentication.views.profil, name='profil'),
    # authentication page
    path('login/', authentication.views.login_page, name='login'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('truck/', authentication.views.add_truck, name='truck'),
    path('modify-user/<int:id>/', authentication.views.modify_user, name='modify-user'),
    path('modify-truck/<int:id>/', authentication.views.modify_truck, name='modify-truck'),
    path('delete-restore/<int:id>/<str:gender>/', authentication.views.delete_restore, name='delete-restore'),
    # factory page
    path('factory-station/', factory.views.factory_station, name='factory-station'),
    path('detail/<str:slug>/', factory.views.detail, name='detail'),
    path('create-factory/', factory.views.create_factory, name='create-factory'),
    path('modify-factory/<int:id>/', factory.views.modify_factory, name='modify-factory'),
    path('create-station/', factory.views.create_station, name='create-station'),
    path('modify-station/<int:id>/', factory.views.modify_station, name='modify-station'),
    path('delete-restore/<int:id>/<str:gender>/', factory.views.delete_restore, name='delete-restore'),
    # adr page
    path('adr/', adr.views.adr, name='adr'),
    path('create-product/', adr.views.create_product, name='create-product'),
    path('modify-product/<int:id>/', adr.views.modify_product, name='modify-product'),
    path('delete-restore/<int:id>/', adr.views.delete_restore, name='delete-restore'),
    # daytime page
    path('daytime/', daytime.views.daytime, name='daytime'),
    path('create-work/<str:gender>/', daytime.views.create_work, name='create-work'),
    path('modify-work/<str:gender>/<int:id>/', daytime.views.modify_work, name='modify-work'),
    path('completed-work/<str:gender>/<int:id>/', daytime.views.completed_work, name='completed-work'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
