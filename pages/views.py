## By default, render is imported from django.shortcuts. 
## But, it's a more common practice to use Django’s built-in generic views, which are class-based. 
## So, replace the import below:
##### from django.shortcuts import render
## With ...
from django.views.generic import TemplateView

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class AboutPageView(TemplateView):
    template_name = 'pages/about.html'