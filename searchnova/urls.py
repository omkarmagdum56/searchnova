from django.contrib import admin
from django.urls import path
from search import views  

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("search/", views.results, name="results"),
    path('api/suggestions/', views.search_suggestions, name='search_suggestions'),
    path('analytics/', views.analytics_dashboard, name='analytics'),
]