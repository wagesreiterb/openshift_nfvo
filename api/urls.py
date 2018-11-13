from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import VnfPkgInfoView, SwaggerSchemaView, VnfPkgInfoIdView, VnfPackageContentView


urlpatterns = {
    # SOL005v020408; A.6	VNF Package Management interface
    url(r'^vnfpkgm/v1/vnf_packages/$', VnfPkgInfoView.as_view(), name="create"),
    url(r'^vnfpkgm/v1/vnf_packages/(?P<pk>[0-9]+)$', VnfPkgInfoIdView.as_view(), name="details"),
    # Upload VNF Package, SOL005v020508 A.6
    url(r'^vnfpkgm/v1/vnf_packages/(?P<pk>[0-9]+)/package_content/$', VnfPackageContentView.as_view(), name='vnfPackageContent'),
    #url(r'^vnfpkgm/v1/vnf_packages/(?P<pk>[0-9]+)/package_content/$', GetPatchDeleteAPIView.as_view(), name='file-upload'),

    url(r'^openapi/$', SwaggerSchemaView.as_view(), name="vnfpkgm"),  # openAPI
}

urlpatterns = format_suffix_patterns(urlpatterns)