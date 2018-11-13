from django.test import TestCase
import uuid
from .models import VnfPkgInfoModel


class VnfPkgInfoModelTestCase(TestCase):
    def setUp(self):
        self.valid_VnfPkgInfo = {
            'id': '123',
            'vnfdId': '234',
            'vnfProvider': 'Wagesreiter Inc.',
            'vnfProductName': 'my First VNF Package',
            'vnfSoftwareVersion' : '1.0',
            'vnfdVersion' : '1.0',
            'checksum' : '',
            'softwareImages' : ["softwareImage One", "softwareImages Two", "softwareImage Three"],
        }

        self.VnfPkgInfo = VnfPkgInfoModel(self.valid_VnfPkgInfo)

    def test_model_can_create_a_VnfPkgInfoModel(self):
        old_count = VnfPkgInfoModel.objects.count()
        self.VnfPkgInfo.save()
        print(self.VnfPkgInfo)
        new_count = VnfPkgInfoModel.objects.count()
        self.assertNotEqual(old_count, new_count)