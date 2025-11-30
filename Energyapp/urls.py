from django.urls import path
from .views import Index
from . import views
urlpatterns = [
    path("", Index.as_view(), name="index"),
    path('analyze/', views.analyze_image, name='analyze_image')

]