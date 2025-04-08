from django.views.generic import ListView
from .models import Joke


# Create your views here.
class JokeListView(ListView):
    ## A minimal ListView is incredibly simple. 
    ## It just requires the model to query (ex. below):
    model = Joke
    ## Notice, above, you do not define a template_name attribute as you did with HomePageView. 
    ## When no template_name is defined for a ListView, Django infers a template_name as: 
    #### `<app_name>/<model>_list.html`
    ## ...Where <app_name> is the name of the app (i.e., jokes). 
    ## And, <model> is the lowercase name of the model. 
    ## So, for JokeListView, Django is looking for the template at: 
    #### `jokes/joke_list.html`