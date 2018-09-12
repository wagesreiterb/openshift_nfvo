from django.test import TestCase
import uuid
from .models import VnfPkgInfoModel


class ModelTestCase(TestCase):
    def setUp(self):
        self.valid_VnfPkgInfo = {
            'id': uuid.uuid4(),
            'vnfdId': uuid.uuid4(),
            'vnfProvider': 'Wagesreiter Inc.',
            'vnfProductName': 'my First VNF Package',
            'vnfSoftwareVersion' : '1.0',
            'vnfdVersion' : '1.0',
            'checksum' : '',
            'softwareImages' : ["softwareImage One", "softwareImages Two", "softwareImage Three"],
        }

    def test_model_can_create_a_VnfPkgInfoModel(self):
        old_count = VnfPkgInfoModel.objects.count()
        self.valid_VnfPkgInfo.save()
        new_count = VnfPkgInfoModel.objects.count()
        self.assertNotEqual(old_count, new_count)