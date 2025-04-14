import random
from django import template
from jokes.models import Joke


register = template.Library()

## `inclusion_tag` fcns must return a dict, which provides context for the associated template 
# (i.e., common/joke.html), which Django will search for in the same places it searches 
# for other templates.
@register.inclusion_tag("common/joke.html")
def random_joke():
    count = Joke.objects.count()
    if (count > 0): # In case we haven't added any jokes yet
        i = random.randint(0, count-1)
        joke = Joke.objects.all()[i]
        return {'joke': joke}
    else:
        return {
            'joke': {
                'question': 'You know what is funny?',
                'answer': 'There are no jokes in the database.'
            }
        }