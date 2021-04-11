from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.views.static import serve


urlpatterns = [
    path('', views.FileFieldView.as_view(), name='index'),
    path('<str:key>', views.FileFieldView.as_view(), name='index_listgeojson'),
    path('open/<str:path>/', views.download, name='open-file'),
]