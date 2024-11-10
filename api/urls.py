from django.urls import path
from .views import word_frequency_view
from .views import index

urlpatterns = [
    path('word-frequency/', word_frequency_view, name='word-frequency'),
]
