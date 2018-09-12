from django.db import models
import uuid
from enum import Enum


####################### helpers for enum #######################
# SOL005v020408, 9.5.4.3	Enumeration: PackageOnboardingStateType
#
# http://anthonyfox.io/2017/02/choices-for-choices-in-django-charfields/
#
class PackageOnboardingStateTypeEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((x.name, x.value) for x in cls)


class PackageOnboardingStateType(PackageOnboardingStateTypeEnum):
    INVALID = 'INVALID'         # Todo: Invented this state myself as I have to set a default value and none of the others match imho
    CREATED = 'CREATED'         # The VNF package resource has been created.
    UPLOADING = 'UPLOADING'     # The associated VNF package content is being uploaded.
    PROCESSING = 'PROCESSING'   # The associated VNF package content is being processed, e.g. validation.
    ONBOARDED = 'ONBOARDED'     # The associated VNF package content is successfully on-boarded.
#
####################### helpers for enum #######################


# SOL005v020408, 9.5.2.5    Type: VnfPkgInfo
class VnfPkgInfoModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vnfdId = models.CharField(max_length=255, blank=True)
    vnfProvider = models.CharField(max_length=255, blank=True)
    vnfProductName = models.CharField(max_length=255, blank=True)
    vnfSoftwareVersion = models.CharField(max_length=255, blank=True)
    vnfdVersion = models.CharField(max_length=255, blank=True)
    checksum = models.CharField(max_length=255, blank=True)
    softwareImages = models.ManyToManyField('self')
    additionalArtifacts = models.ManyToManyField('self')
    onboardingState = models.CharField(max_length=20, choices=PackageOnboardingStateTypeEnum.choices(),
                                       default=PackageOnboardingStateType.INVALID)
    # operationalState
    # usageState
    # userDefinedData
    # _links
    # > self
    # > vnfd
    # > packageContent

