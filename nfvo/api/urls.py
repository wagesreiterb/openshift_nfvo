from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateView, DetailsView

urlpatterns = {
    # SOL005v020408; A.6	VNF Package Management interface
    url(r'^vnfpkgm/v1/vnf_packages/$', CreateView.as_view(), name="create"),
    url(r'^vnfpkgm/v1/vnf_packages/(?P<pk>[0-9]+)$', DetailsView.as_view(), name="details"),

}

urlpatterns = format_suffix_patterns(urlpatterns)