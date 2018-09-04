from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateView, DetailsView

urlpatterns = {
    url(r'^vnfpkgm/v1/vnf_packages/$', CreateView.as_view(), name="create"),
    # Todo: there might be another simpler way to resolve uuid?!
    url(r'^vnfpkgm/v1/vnf_packages/(?P<pk>\b[0-9A-Fa-f]{8}\b(-\b[0-9A-Fa-f]{4}\b){3}-\b[0-9A-Fa-f]{12}\b)$', DetailsView.as_view(), name="details"),

}


# Todo: is that required anymore?!
urlpatterns = format_suffix_patterns(urlpatterns)