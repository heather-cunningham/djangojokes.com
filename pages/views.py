from django.contrib import messages
## By default, render is imported from django.shortcuts. 
## But, it's a more common practice to use Django’s built-in generic views, which are class-based. 
## So, replace the import below:
##### from django.shortcuts import render
## With ...
from django.views.generic import TemplateView


# Create your views here.
class HomePageView(TemplateView):
    template_name = 'pages/home.html'


## BEGIN
class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

## EXAMPLE of using Msgs in a View.  You still need the HTML in a template, too.
    # def get(self, request, *args, **kwargs):
    #     messages.debug(request, 'Debug message.') ## The str is the msg output.
    #     messages.info(request, 'Info message.')
    #     messages.success(request, 'Success message.')
    #     messages.warning(request, 'Warning message.')
    #     messages.error(request, 'Error message.')
    #     return super().get(request, args, kwargs)
## END class