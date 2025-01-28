# filepath: /Users/dairui/Desktop/epub-rosetta/epub-rosetta/backend/epubrosetta/epub_processor/urls.py
from django.urls import path
from .views import Wordwise

urlpatterns = [
    path('wordwise/', Wordwise.as_view(), name='wordwise'),
]