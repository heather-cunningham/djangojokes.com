import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q  ## Allows compound queries using conditions, like AND or OR, etc.
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
    #
    # Adding in pagination:  It's this ez w/ Django!
    ## When you add the paginate_by attribute to the ListView, 
    # you get access to a new page_obj in the context.
    paginate_by = 10
    ## The page_obj object includes the following properties:
        ## page_obj.has_previous – True if the current page is not the first page.
        ## page_obj.previous_page_number – The number of the previous page.
        ## page_obj.has_next – True if the current page is not the last page.
        ## page_obj.next_page_number –The number of the next page.
        ## page_obj.number – The current page number.
        ## page_obj.paginator.num_pages – The total number of pages.
    #
    ## You can control the ordering of ListViews using the ordering attribute.
    ## Prepend w/ a minus sign for descending order.  Ascending order is the default.
    ## Works great if you always want to sort in the same way, but not if you want dynamic sorting.
    # ordering = ['-question']


    def get_order_fields(self):
        """ Returns a dictionary mapping friendly names to field names and lookups.
        """
        return {
            'joke': 'question',
            'category': 'category__category',
            'creator': 'user__username',
            'created': 'created',
            'updated': 'updated',
            'default_key': 'updated' ## the default field to order by if order_key is either unspecified or invalid
        }
    

    def get_order_settings(self):
        order_fields = self.get_order_fields()
        default_order_key = order_fields['default_key']
        order_key = self.request.GET.get('order', default_order_key)
        direction = self.request.GET.get('direction', 'desc')
        # If order_key is invalid, use default
        if (order_key not in order_fields):
            order_key = default_order_key
        return (order_fields, order_key, direction)
    

    ## For Dynamic Ordering: Use the get_ordering() method of ListViews
    # It makes it possible to change the ordering based on values passed in over the querystring.
    ## @override
    def get_ordering(self):
        ## Default ordering will be '-updated'
        # ordering = self.request.GET.get('order', '-updated')
        order_fields, order_key, direction = self.get_order_settings()
        order_by = order_fields[order_key]
        ## If direction is 'desc' or invalid, use descending order:
        if (direction != 'asc'):
            order_by = '-' + order_by
        return order_by
    

    ## @override
    def get_queryset(self):
        ordering_by = self.get_ordering()
        query_set = Joke.objects.all()
        if ("search_qry" in self.request.GET): # Filter by search query
            search_qry = self.request.GET.get("search_qry") 
            ## Q lib: Allows compound queries using conditions, like <AND> & or <OR> |, etc.
            query_set = query_set.filter(Q(question__icontains=search_qry) | Q(answer__icontains=search_qry))
        ## Check if the route name is "my_jokes" to filter just that user's created jokes.
        if (self.request.resolver_match.url_name == "my_jokes"):   
            query_set = query_set.filter(user=self.request.user)
        elif ("slug" in self.kwargs): ## Filter by category OR tag
            slug = self.kwargs["slug"]
            if ("/category" in self.request.path_info): ## Filter by category
                query_set = query_set.filter(category__slug=slug)
            if ("/tag" in self.request.path_info): ## Filter by tag
                query_set = query_set.filter(tags__slug=slug)
        elif ("username" in self.kwargs): # Filter by joke creator
            username = self.kwargs["username"]
            query_set = query_set.filter(user__username=username)
        ## Adding in prefetch for optimization and to reduce dupe hits to the db
        return query_set.prefetch_related('category', 'user').order_by(ordering_by)
        # return query_set.order_by(ordering_by)


    ## @override
    def get_context_data(self, **kwargs):
        # Access the default context object name `joke_list`
        context = super().get_context_data(**kwargs)
        ## Compute #rating-bar width dynamically b/c `widthratio` does not work
        for joke in context["joke_list"]:
            if(joke.rating):
                joke.rating_width = joke.rating * 10
        # Check if the user is authenticated:
        if (self.request.user.is_authenticated):
            # Add the first joke related to the current user
            context['joke'] = self.model.objects.filter(user=self.request.user).first()
        else:
            context['joke'] = None
        context['user'] = self.request.user
        ## Add Ordering into the Context:
        order_fields, order_key, direction = self.get_order_settings()
        context['order'] = order_key
        context['direction'] = direction
        ## Slice all but the last order key, which is 'default'
        context['order_fields'] = list(order_fields.keys())[:-1]
        return context
## END class JokeListView


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