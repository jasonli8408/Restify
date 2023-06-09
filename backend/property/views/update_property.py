from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from property.models import Property
from property.serializers import PropertySerializer


class UpdatePropertyView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PropertySerializer
    lookup_field = 'pk'

    def get_object(self):
        return get_object_or_404(Property, pk=self.kwargs['pk'])

    def perform_update(self, serializer):
        if self.request.user == self.get_object().user:
            serializer.save()
        else:
            raise PermissionDenied('You do not have permission to edit this property.')
