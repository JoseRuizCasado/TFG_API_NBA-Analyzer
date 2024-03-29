"""api_nba_analyzer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from rest_framework_swagger.views import get_swagger_view


schema_view = get_swagger_view(title='API Documentation')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view),
    re_path('dbmanager/', include('dataBaseManager.urls')),
    re_path('gameanalyzer/', include('gameAnalyzer.urls')),
    re_path('advancedStatisticsCalculator/', include('advancedStatisticsCalculator.urls')),
    re_path('modelPredictor/', include('modelPredictor.urls')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, })
]
