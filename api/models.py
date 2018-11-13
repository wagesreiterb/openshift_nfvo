from django.db import models
import uuid
from enum import Enum


####################### helpers for enum #######################
# SOL005v020408, 9.5.4.3	Enumeration: PackageOnboardingStateType
#
# http://anthonyfox.io/2017/02/choices-for-choices-in-django-charfields/
#
#class PackageOnboardingStateTypeEnum(Enum):
#    @classmethod
#    def choices(cls):
#        return tuple((x.name, x.value) for x in cls)#
#
#
#class PackageOnboardingStateType(PackageOnboardingStateTypeEnum):
#    CREATED = 'CREATED'         # The VNF package resource has been created.
#    UPLOADING = 'UPLOADING'     # The associated VNF package content is being uploaded.
#    PROCESSING = 'PROCESSING'   # The associated VNF package content is being processed, e.g. validation.
#    ONBOARDED = 'ONBOARDED'     # The associated VNF package content is successfully on-boarded.
#
# Data type: PackageOnboardingStateType (SOL005v020408, 9.5.2.5)
VNF_PACKAGE_ONBOARDING_STATE_CHOICES = (
    (u'CREATED', u'Created'),          # The VNF package resource has been created.
    (u'UPLOADING', u'Uploading'),      # The associated VNF package content is being uploaded.
    (u'PROCESSING', u'Processing'),    # The associated VNF package content is being processed, e.g. validation.
    (u'ONBOARDED', u'Onboarded'),      # The associated VNF package content is successfully on-boarded.
)
####################### helpers for enum #######################

VNF_PACKAGE_OPERATIONAL_STATE_CHOICES = (
    (u'ENABLED', u'Enabled'),           # The VNF Package is enabled.
    (u'DISABLED', u'Disabled'),         # The VNF Package is disabled.
)

VNF_PACKAGE_USAGE_STATE_CHOICES = (
    (u'IN_USE', u'in use'),             # The VNF Package is in use.
    (u'NOT_IN_USE', u'not in use'),     # The VNF Package is not in use.
)

# Type: VnfPkgInfo (SOL005v020408, 9.5.2.5)
class VnfPkgInfoModel(models.Model):
    id = models.AutoField(primary_key=True, max_length=255, editable=False) # Todo: what type shall an id be?
    vnfdId = models.CharField(max_length=255, blank=True)
    vnfProvider = models.CharField(max_length=255, blank=True)
    vnfProductName = models.CharField(max_length=255, blank=True)
    vnfSoftwareVersion = models.CharField(max_length=255, blank=True)
    vnfdVersion = models.CharField(max_length=255, blank=True)
    checksum = models.CharField(max_length=255, blank=True)
    #softwareImages = models.ManyToManyField('self')     # Todo: doesn't work - at least with the GUI
    #additionalArtifacts = models.ManyToManyField('self') # Todo: doesn't work - at least with the GUI
    onboardingState = models.CharField(max_length=25, choices=VNF_PACKAGE_ONBOARDING_STATE_CHOICES, default='CREATED')
    operationalState = models.CharField(max_length=25, choices=VNF_PACKAGE_OPERATIONAL_STATE_CHOICES, default='DISABLED')
    usageState = models.CharField(max_length=25, choices=VNF_PACKAGE_USAGE_STATE_CHOICES, default='NOT_IN_USE')
    url = models.CharField(max_length=255, blank=True)

    # userDefinedData
    # _links
    # > self
    # > vnfd
    # > packageContent


# https://blog.vivekshukla.xyz/uploading-file-using-api-django-rest-framework/
class VnfPkgModel(models.Model):
    vnfPkgInfo = models.OneToOneField(
        VnfPkgInfoModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    file = models.FileField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
