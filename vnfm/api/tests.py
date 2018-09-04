from django.test import TestCase
import uuid
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import VnfModel


class ModelTestCase(TestCase):
    def setUp(self):
        self.vnfInstanceId = uuid.uuid4()
        self.vnfInstanceName = "myFirstVNFInstace"
        self.vnfInstanceDescription = "this ist my first VNF instance"
        self.vnfdId = uuid.uuid4()
        self.vnfProvider = "Wagesreiter Inc."
        self.vnfProductName = "UGW"
        self.vnfSoftwareVersion = "0.1 Beta"
        self.vnfdVersion = "0.2 Alpha"

        self.vnf = VnfModel(vnfInstanceId=self.vnfInstanceId)

    def test_model_can_create_a_vnf(self):
        old_count = VnfModel.objects.count()
        self.vnf.save()
        new_count = VnfModel.objects.count()
        self.assertNotEqual(old_count, new_count)


class ViewTestCase(TestCase):
    """Test suite for the api views."""
    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.vnf_data = {'vnfInstanceId': uuid.uuid4(),
                         'vnfInstanceName': "myFirstVNFInstace",
                         'vnfInstanceDescription': "this ist my first VNF instance",
                         'vnfdId': uuid.uuid4(),
                         'vnfProvider': "Wagesreiter Inc.",
                         'vnfProductName': "UGW",
                         'vnfSoftwareVersion': "0.1 Beta",
                         'vnfdVersion': "0.2 Alpha"}

        self.response = self.client.post(
            reverse('create'),
            self.vnf_data,
            format="json")

    def test_api_can_create_a_vnf(self):
        """Test the api has vnf creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_get_a_vnf(self):
        """Test the api can get a given vnf."""
        vnf = VnfModel.objects.get()
        response = self.client.get(
            reverse('details',
            kwargs={'pk': vnf.vnfInstanceId}), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, vnf)

    def test_api_can_update_vnf(self):
        """Test the api can update a given vnf."""
        change_vnf = {'vnfInstanceName': 'Something new'}
        res = self.client.put(
            reverse('details', kwargs={'pk': vnf.vnfInstanceId}),
            change_vnf, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_can_delete_vnf(self):
        """Test the api can delete a bucketlist."""
        vnf = VnfModel.objects.get()
        response = self.client.delete(
            reverse('details', kwargs={'pk': vnf.vnfInstanceId}),
            format='json',
            follow=True)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)