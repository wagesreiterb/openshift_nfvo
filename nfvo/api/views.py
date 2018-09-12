from rest_framework import generics
from .serializers import VnfPkgInfoSerializer
from .models import VnfPkgInfoModel


class CreateView(generics.ListCreateAPIView):
    queryset = VnfPkgInfoModel.objects.all()
    serializer_class = VnfPkgInfoSerializer

    def perform_create(self, serializer):
        serializer.save()


class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = VnfPkgInfoModel.objects.all()
    serializer_class = VnfPkgInfoSerializer
