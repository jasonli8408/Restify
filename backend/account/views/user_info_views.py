
from ..serializer import RegisterSerializer, ProfileEditSerializer
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status, permissions
from ..models import User

# class-based apiview for register user
class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(ProfileEditSerializer(request.user).data)


class ProfileEditView(UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def put(self, request):
        serializer = ProfileEditSerializer(request.user, data=request.data)
        if serializer.is_valid():
            # delete only when a new avatar is uploaded
            if 'avatar_url' in request.data:
                self.get_object().avatar_url.delete()
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsernameByIdView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        if not User.objects.filter(id=pk).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(User.objects.get(id=pk).username)
