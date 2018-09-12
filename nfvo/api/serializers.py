from rest_framework import serializers
from .models import VnfPkgInfoModel


class VnfPkgInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VnfPkgInfoModel
        fields = ('id',
                  'vnfdId',
                  'vnfProvider',
                  'vnfProductName',
                  'vnfSoftwareVersion',
                  'vnfdVersion',
                  'checksum',
                  #'softwareImages',
                  #'additionalArtifacts',
                  'onboardingState'
                  )


