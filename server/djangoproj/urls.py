from django.contrib import admin
from django.urls import path, include, re_path 
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')), 
    path('', TemplateView.as_view(template_name="Home.html")), 
    path('about/', TemplateView.as_view(template_name="About.html")),
    path('contact/', TemplateView.as_view(template_name="Contact.html")),
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]