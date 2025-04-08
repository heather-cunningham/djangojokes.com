from django.urls import path
from .views import JokeListView


app_name = "jokes"


urlpatterns = [
    ## Remember only URL paths beginning with '/jokes/' will be handed off to the URLConf 
    ## of the jokes app, so "" will actually be "/jokes/".
    path("", JokeListView.as_view(), name="list"),
]