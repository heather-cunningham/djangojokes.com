from django.urls import path
from .views import (JokeCreateView, JokeDetailView, JokeListView, 
                    JokeUpdateView)


app_name = "jokes"


urlpatterns = [
    ## Remember only URL paths beginning with '/jokes/' will be handed off to the URLConf 
    ## of the jokes app, so "" will actually be "/jokes/".
    path("", JokeListView.as_view(), name="list"),
    path("joke/create/", JokeCreateView.as_view(), name="create"),
    ## ID the specific joke to show using the joke object’s primary key 
    # (which is the same as the joke's auto-gen'd ID in the sqlite db).
    ## Look in .venv\Lib\site-packages\django\views\generic\detail.py 
    # at the get_object() method of the SingleObjectMixin class 
    # to see how this magic works behind the scenes.
    path("joke/<int:pk>", JokeDetailView.as_view(), name="detail"),
    path("joke/<int:pk>/update/", JokeUpdateView.as_view(), name="update"),
]