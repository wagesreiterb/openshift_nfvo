from django.db import models
import uuid


class VnfModel(models.Model):
    # Todo: uuid shouldn't be a primary key
    # https://stackoverflow.com/questions/3936182/using-a-uuid-as-a-primary-key-in-django-models-generic-relations-impact
    vnfInstanceId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vnfInstanceName = models.CharField(max_length=255, blank=False)
    vnfInstanceDescription = models.CharField(max_length=255, blank=False)
    # Todo: vnfdId should be the foreign key from the vnfdId tabel
    vnfdId = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    vnfProvider = models.CharField(max_length=255, blank=False)
    vnfProductName = models.CharField(max_length=255, blank=False)
    vnfSoftwareVersion = models.CharField(max_length=255, blank=False)
    vnfdVersion = models.CharField(max_length=255, blank=False)

    # Todo: creation date and modification date might be a good idea
    # date_created = models.DateTimeField(auto_now_add=True)
    # date_modified = models.DateTimeField(auto_now=True)

    # Todo: is __str__ required at all?
    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)