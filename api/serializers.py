from rest_framework import serializers
from .models import VnfPkgInfoModel, VnfPkgModel


class VnfPkgInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VnfPkgInfoModel
        fields = ( 'id',
                   'vnfdId',
                   'vnfProvider',
                   'vnfProductName',
                   'vnfSoftwareVersion',
                   'vnfdVersion',
                   'checksum',
                   #'softwareImages',
                   #'additionalArtifacts',
                   'onboardingState',
                   'operationalState',
                   'usageState',
                   #'url',
        )


# for file uploading set the following in the http-header: Content-Type: multipart/form-data
# example POST:
# request: curl -H 'Content-Type: multipart/form-data' -F 'file=@/home/que/test.txt' -F 'remark=2terTest' http://127.0.0.1:8000/upload/
# response: {"file":"/media/bled2.txt","remark":"Test001","timestamp":"2018-10-21T09:27:12.637911Z"}
# example PUT:
# request: curl -X PUT -H 'Content-Type: multipart/form-data' -F 'file=@/home/que/Bernhard/NFV/tosca_examples/myCSAR.zip' -F 'remark=2terTest' http://127.0.0.1:8000/upload/
# response: {"file":"/media/myCSAR_NSVL2fg.zip","remark":"Test001","timestamp":"2018-10-21T12:24:41.962032Z"}
class VnfPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VnfPkgModel
        fields = (#'vnfPkgInfo',    # id of vnfPkgInfo, will be parsed from the URL, eg http://127.0.0.1:8000/vnfpkgm/v1/vnf_packages/7/package_content/
                  'file',
                  'timestamp')
