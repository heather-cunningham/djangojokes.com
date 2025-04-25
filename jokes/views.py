import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from .models import Joke, JokeVote
from .forms import JokeForm

## These are class based Views
## ------------------------------
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
## END class based Views
## ------------------------------------------------------------------------------


## Functional Views aka View fcns
## ------------------------------------------------------------------------------
## We are using a fcnl View here so we can use JS and AJAX
# to send data back and forth from the client side to the server-side
# w/o a web page refresh
## If you are handling non-authenticated users client-side, you no longer have to give them access to the vote method
#  at all. You can add the @login_required decorator to the vote function (or any view function) to make the view 
# only accessible to logged-in users:
@login_required
def vote(request, slug):
    """ Vote like or dislike on a Joke AJAX
     params: `request` (web HTTP request obj) - w/ the body property containing the stringified JSON data
             `slug` (str) - The joke slug, which is passed in from a URL pattern in the URLConf              
    """
    user = request.user # The logged-in user (or AnonymousUser).
    joke = Joke.objects.get(slug=slug) # The joke instance.
    data = json.loads(request.body) # Data from the JavaScript.
    # Set simple variables.
    vote = data['vote'] # The user's new vote.
    likes = data['likes'] # The number of likes currently displayed on page.
    dislikes = data['dislikes'] # The number of dislikes currently displayed.

    if (user.is_anonymous): # User not logged in. Can't vote.
        msg = 'Sorry, you have to be logged in to vote.'
    else: # User is logged in.
        if (JokeVote.objects.filter(user=user, joke=joke).exists()):
            # User already voted. Get user's past vote:
            joke_vote = JokeVote.objects.get(user=user, joke=joke)

            if (joke_vote.vote == vote): # User's new vote is the same as old vote.
                msg = 'Right. You told us already.'
            else: # User changed vote.
                joke_vote.vote = vote # Update JokeVote instance.
                joke_vote.save() # Save.

                # Set data to return to the browser.
                if (vote == -1):
                    likes -= 1
                    dislikes += 1
                    msg = "Don't like it after all, huh? OK. Noted."
                else:
                    likes += 1
                    dislikes -= 1
                    msg = 'Grown on you, has it? OK. Noted.'
        else: # First time user is voting on this joke.
            # Create and save new vote.
            joke_vote = JokeVote(user=user, joke=joke, vote=vote)
            joke_vote.save()

            # Set data to return to the browser.
            if (vote == -1):
                dislikes += 1
                msg = "Sorry you didn't like the joke."
            else:
                likes += 1
                msg = "Yeah, good one, right?"
    # Create a response object and send it back to the browser as JSON.
    response = {
        'msg': msg,
        'likes': likes,
        'dislikes': dislikes
    }
    return JsonResponse(response) # Return object as JSON back to the JS fcns as data response