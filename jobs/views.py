import html
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from common.utils.email import send_email
from .forms import JobApplicationForm


class JobApplicationView(FormView):
    template_name = "jobs/joke_writer.html"
    form_class = JobApplicationForm
    success_url = reverse_lazy("jobs:thanks")


    def is_form_valid(self, form):
        data = form.cleaned_data
        to = 'cunningham.heatherirene@gmail.com'
        subject = 'Application for Joke Writer'
        content = f'''<p>Hey HR Manager!</p>
            <p>Job application received:</p>
            <ol>'''
        for key, value in data.items():
            label = key.replace('_', ' ').title()
            entry = html.escape(str(value), quote=False)
            content += f'<li>{label}: {entry}</li>'
        content += '</ol>'
        send_email(to, subject, content)
        return super().is_form_valid(form)
## END JobApplicationView class


class JobApplicationThanksView(TemplateView):
     template_name = "jobs/thanks.html"


