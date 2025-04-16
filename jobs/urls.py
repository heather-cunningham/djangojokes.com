from django.urls import path
from .views import JobApplicationView, JobApplicationThanksView


app_name = "jobs"


urlpatterns = [
    path("job-app/", JobApplicationView.as_view(), name="app"),
    path("job-app/thanks/", JobApplicationThanksView.as_view(), name="thanks")
]

