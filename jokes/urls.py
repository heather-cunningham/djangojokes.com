from django.urls import path
from .views import (JokeCreateView, JokeDeleteView, JokeDetailView, JokeListView, 
                    JokeUpdateView)
## Parens above are just to show how to split imports across multiple lines


app_name = "jokes"


urlpatterns = [
    ## Remember only URL paths beginning with '/jokes/' will be handed off to the URLConf 
    ## of the jokes app, so "" will actually be "/jokes/".
    path("", JokeListView.as_view(), name="list"),
    path("joke/create/", JokeCreateView.as_view(), name="create"),
    ## The default template_name for a DeleteView: `<app_name>/<model-name>_confirm_delete.html`
    path("joke/<slug>/delete/", JokeDeleteView.as_view(), name="delete"),
    path("joke/<slug>/update/", JokeUpdateView.as_view(), name="update"),
    path("joke/<slug>/", JokeDetailView.as_view(), name="detail"),
]