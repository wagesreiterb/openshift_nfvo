from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import VnfPkgInfoSerializer, VnfPackageSerializer
from .models import VnfPkgInfoModel, VnfPkgModel
from rest_framework import mixins
from zipfile import ZipFile
import logging
from django.conf import settings


# https://lincolnloop.com/blog/django-logging-right-way/
logger = logging.getLogger(__name__)


class VnfPkgInfoView(generics.ListCreateAPIView):
    # CreateView
    """
    get:
        Query VNF Package Info

    post:
        Create VNF Package Info
    """
    queryset = VnfPkgInfoModel.objects.all()
    serializer_class = VnfPkgInfoSerializer

    def perform_create(self, serializer):
        serializer.save()


class VnfPkgInfoIdView(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            generics.GenericAPIView):
    # GetPatchDeleteAPIView
    """
    get:
        Query VNF Package Info

    patch:
        Update VNF Package Info

    delete:
        Delete VNF Package
    """
    queryset = VnfPkgInfoModel.objects.all()
    serializer_class = VnfPkgInfoSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # http: // www.django - rest - framework.org / api - guide / status - codes /
        instance = self.get_object()
        if instance.usageState != 'NOT_IN_USE':                       # SOL005v020408 9.3.6
            error_string="ERROR: VnfPkgInfo is in use, usageState = " + instance.usageState
            print(error_string)      # Todo: shall be logged
            return Response(error_string, status=status.HTTP_422_UNPROCESSABLE_ENTITY)  # Todo: might be wrong, not specified in SOL005v020408 9.3.6
        elif instance.operationalState != 'DISABLED':                 # SOL005v020408 9.3.6
            error_string="ERROR: VnfPkgInfo is enabled, operationalState = " + instance.operationalState
            print(error_string)      # Todo: shall be logged
            return Response(error_string,
                            # headers={"Location": "http://127.0.0.1/vnfpkgm/v1/vnf_packages/"},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)  # Todo: might be wrong, not specified in SOL005v020408 9.3.6
        else:
            return self.destroy(request, *args, **kwargs)

    # SOL005v020408, 9.3.2	Flow of the uploading of VNF package content
    # def put(self, request, *args, **kwargs):
    #    instance = self.get_object()
    #    if instance.is_valid():
    #        instance.save()
    #        return Response(status=status.HTTP_202_ACCEPTED)
    #    else:
    #        return Response(instance.errors, status=status.HTTP_400_BAD_REQUEST)


class VnfPackageContentView(generics.GenericAPIView,
                            mixins.RetrieveModelMixin):

    parser_classes = (MultiPartParser, FormParser)
    queryset = VnfPkgModel.objects.all()
    serializer_class = VnfPackageSerializer

    # SOL005v020408, 9.3.2	Flow of the uploading of VNF package content
    def put(self, request, *args, **kwargs):
        # Todo: change VNF_PACKAGE_ONBOARDING_STATE_CHOICES to UPLOADING
        file_serializer = VnfPackageSerializer(data=request.data)
        vnf_pkg_info_id = kwargs.get('pk')
        vnf_pkg_info_instance = VnfPkgInfoModel.objects.get(pk=vnf_pkg_info_id)
        # Todo: check if STATES of VnfPkgInfo are correct, otherwhise respond with an error

        if file_serializer.is_valid():
            # https://medium.com/profil-software-blog/10-things-you-need-to-know-to-effectively-use-django-rest-framework-7db7728910e0
            file_serializer.save(vnfPkgInfo=vnf_pkg_info_instance)
            vnf_pkg_instance = VnfPkgModel.objects.get(pk=vnf_pkg_info_id)
            vnf_pkg_filename = vnf_pkg_instance.file
            vnf_pkg_path = getattr(settings, "MEDIA_ROOT", None)
            try:
                extract_zipfile(vnf_pkg_path, vnf_pkg_filename)
            except Exception as e:
                print(e)

            return Response(file_serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            # Todo: change VNF_PACKAGE_ONBOARDING_STATE_CHOICES to CREATED
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    #def put(self, request, *args, **kwargs):
    #    file_serializer = FileSerializer(data=request.data)
    #    if file_serializer.is_valid():
    #        file_serializer.save()
    #        return Response(file_serializer.data, status=status.HTTP_202_ACCEPTED)
    #    else:
    #        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # post for indirect mode via URI
    # Todo: not finished
    def post(self, request, *args, **kwargs):
        file_serializer = VnfPackageSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


# class based openAPI
# https://django-rest-swagger.readthedocs.io/en/latest/schema/
class SwaggerSchemaView(APIView):
    exclude_from_schema = True      # https://github.com/m-haziq/django-rest-swagger-docs#swagger-login-methods
    permission_classes = [AllowAny]
    renderer_classes = [
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]

    def get(self, request):
        generator = SchemaGenerator()
        schema = generator.get_schema(request=request)

        return Response(schema)


def extract_zipfile(vnf_pkg_path, vnf_pkg_filename):
    # extract zipfile
    # https: // www.geeksforgeeks.org / working - zip - files - python /
    # Todo: shall run in its own thread in order not to block the api
    #
    fully_qualified_file_name = str(vnf_pkg_path) + '/' + str(vnf_pkg_filename) + "bled"
    print("path_file:", fully_qualified_file_name)
    vnf_pkg_directory = fully_qualified_file_name[:-4]  # Todo: check if file has the extension .zip
    print("vnf_pkg_directory:", vnf_pkg_directory)

    # opening the zip file in READ mode
    with ZipFile(fully_qualified_file_name, 'r') as zip:
        # printing all the contents of the zip file
        zip.printdir()

        # extracting all the files
        print('Extracting all the files now...')
        x = zip.extractall(path=vnf_pkg_directory)
        print("xxx:", x)
        print('Done!')

