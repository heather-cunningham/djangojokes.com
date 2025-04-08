from django.urls import path
from pages.views import HomePageView, AboutPageView


app_name = "pages"


urlpatterns = [
    path("", HomePageView.as_view(), name="homepage"),
    path("about/", AboutPageView.as_view(), name="about")
]