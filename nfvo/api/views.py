from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers
from .serializers import VnfPkgInfoSerializer
from .models import VnfPkgInfoModel
from rest_framework import mixins


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
        return self.destroy(request, *args, **kwargs)


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
