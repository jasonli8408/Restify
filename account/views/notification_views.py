from ..serializer import NotificationSerializer
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework import permissions
from ..models import Notification
from rest_framework.response import Response


class HostNotificationView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user, is_host=True)
    
    def get(self, request):
        # change all entries in the queryset to read = True once opened
        for notification in self.get_queryset():
            notification.read = True
            notification.save()
        return super().get(request)


class TenentNotificationView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user, is_host=False)
    
    def get(self, request):
        # change all entries in the queryset to read = True once opened
        for notification in self.get_queryset():
            notification.read = True
            notification.save()
        return super().get(request)
    

class HostNotificationDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer

    def delete(self, request):
        for notification in Notification.objects.filter(user=request.user, is_host=True):
            notification.delete()
        return Response(status=204)
    

class TenentNotificationDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer

    def delete(self, request):
        for notification in Notification.objects.filter(user=request.user, is_host=False):
            notification.delete()
        return Response(status=204)