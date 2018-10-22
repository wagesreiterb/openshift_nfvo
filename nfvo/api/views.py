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
from rest_framework.reverse import reverse


class CreateView(generics.ListCreateAPIView):
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


class GetPatchDeleteAPIView(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            generics.GenericAPIView):
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
    #def put(self, request, *args, **kwargs):
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
        vnf_pkg_info_instance = VnfPkgInfoModel.objects.get(pk=kwargs.get('pk'))
        # Todo: check if STATES of VnfPkgInfo are correct, otherwhise respond with an error
        print("vnfPkgInfoInstance", vnf_pkg_info_instance)

        if file_serializer.is_valid():
            # https://medium.com/profil-software-blog/10-things-you-need-to-know-to-effectively-use-django-rest-framework-7db7728910e0
            file_serializer.save(vnfPkgInfo=vnf_pkg_info_instance)
            # Todo: Package Processing
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


# class DetailsView(generics.RetrieveUpdateDestroyAPIView):
#     """
#     get:
#         Query VNF Package Info
#
#     patch:
#         Update VNF Package Info
#
#     delete:
#         Delete VNF Package
#     """
#     # https://docs.djangoproject.com/en/2.1/ref/class-based-views/base/
#     # ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
#     allowd_methods = ['get', 'post', 'patch', 'delete', 'head', 'options', 'trace']
#     queryset = VnfPkgInfoModel.objects.all()
#     serializer_class = VnfPkgInfoSerializer
#
# http://www.cdrf.co/3.1/rest_framework.views/APIView.html
