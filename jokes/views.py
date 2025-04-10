from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from .models import Joke


# Create your views here.
class JokeCreateView(CreateView):
    model = Joke
    fields = ["question", "answer"]


class JokeDeleteView(DeleteView):
    model = Joke
    success_url = reverse_lazy("jokes:list")


class JokeDetailView(DetailView):
    ## Just like a ListView, a minimal DetailView only requires the model to query.
    model = Joke
    ## Default name of the template used by the JokeDetailView: 
    ## `<app_name>/<model>_detail.html`
    # e.g.: `jokes/joke_detail.html`


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


class JokeUpdateView(UpdateView):
    model = Joke
    fields = ["question", "answer"]