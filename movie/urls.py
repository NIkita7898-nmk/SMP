from django.urls import path
from movie.views import MovieView
urlpatterns = [
    path('movie/', MovieView.as_view())
]
