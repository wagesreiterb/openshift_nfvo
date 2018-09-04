from rest_framework import serializers
from .models import VnfModel


class VnfSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = VnfModel
        fields = ('vnfInstanceId', 'vnfInstanceName', 'vnfInstanceDescription', 'vnfdId', 'vnfProvider', 'vnfProductName',
                  'vnfSoftwareVersion', 'vnfdVersion')
        #read_only_fields = ('date_created', 'date_modified')
