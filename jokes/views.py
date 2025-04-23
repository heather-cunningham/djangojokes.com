from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from .models import Joke
from .forms import JokeForm


## BEGIN
class JokeCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Joke
    ## When using model form, means you can't use fields here.
    ## You wouldn't  want to anyway, b/c then you can't style these fields.
    # fields = ["question", "answer"]
    form_class = JokeForm ## Joke Model Form
    success_message = "Joke created successfully."


    ## @override
    def form_valid(self, form):
        """ Takes a form parameter, which has an instance property holding the data in the form object.  
        Here, adding another attribute, user, to that form object before saving."""
        form.instance.user = self.request.user
        ## After making the above change, call and return form_valid() on the superclass, 
        # which takes care of saving the form and redirecting to the success URL.
        return super().form_valid(form)
## END class


## BEGIN
class JokeDeleteView(UserPassesTestMixin, DeleteView):
    model = Joke
    ## reverse_lazy() works just like reverse(): 
    ## It returns the URL based on the passed-in URL pattern name. 
    # But unlike reverse(), it waits to get the URL until it is needed.
    success_url = reverse_lazy("jokes:list")
    ## We use reverse_lazy() here because the view is created before the URL configuration.
    ## So, if you try to use reverse(), you will likely get an error about a circular import. 
    ## The issue with using reverse() is the view needs the URLConf to have already been created, 
    # but the URLConf imports the view. So, it cannot be created until the view exists.


    """ UserPassesTestMixin requires a test_func() method, which returns True if the user passes the test
      and False otherwise."""
    ## @override
    def test_func(self):
        """ Returns True if and only if the logged-in user is the user who created the joke. """
        obj = self.get_object()
        return self.request.user == obj.user
    

    ## @override
    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        return result


    ## @override
    def form_valid(self, form):
        messages.success(self.request, 'Joke deleted.')
        return super().form_valid(form)
## END class


## BEGIN
class JokeDetailView(DetailView):
    ## Just like a ListView, a minimal DetailView only requires the model to query.
    model = Joke
    ## Default name of the template used by the JokeDetailView: 
    ## `<app_name>/<model>_detail.html`
    # e.g.: `jokes/joke_detail.html`
## END class


## BEGIN
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


    ## @override
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check if the user is authenticated:
        if (self.request.user.is_authenticated):
            # Add the first joke related to the current user
            context['joke'] = self.model.objects.filter(user=self.request.user).first()
        else:
            context['joke'] = None
        context['user'] = self.request.user
        return context
## END class


## BEGIN
class JokeUpdateView(SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Joke
    # fields = ["question", "answer"]
    form_class = JokeForm
    success_message = "Joke updated successfully."


    ## @override
    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.user
## END class