import private_storage.urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),

    # User Management
    path('account/', include('users.urls')),
    path("account/", include("allauth.urls")),

    # Private media & files
    path('media/private/', include(private_storage.urls)),

    # Local Apps
    path("jobs/", include("jobs.urls")),
    path("jokes/", include("jokes.urls")),
    path("", include("pages.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
## The static() fcn, above, is a helper fcn that only works when settings.DEBUG is set to True. 
## So, you don’t have to worry about removing this code when deploying to production. 
## It'll be ignored.
## We are NOT deploying storage to AWS S3 buckets rt now, cuz NO WORKY the way class said it does.
## IN future, go thru free AWS S3 training on their site and see if you can figure it out.


if (settings.DEBUG):
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns


## I want to keep these notes.
"""
URL configuration for djangojokes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
