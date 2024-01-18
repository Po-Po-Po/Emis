from rest_framework import routers, serializers, viewsets
from .models import *
from django.contrib.auth.models import Group
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    class Meta:
        model = CustomUser
        fields = '__all__'

    def get_id_report_card(self, obj):
        return obj.report_card_id

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class ProfileViewSet(viewsets.views.APIView):

    def get(self, request):
        if request.user.pk:
            queryset = CustomUser.objects.get(pk=request.user.pk)
            serialize = UserSerializer(queryset).data
            return Response(serialize)

        return Response({})


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            tokens = OutstandingToken.objects.filter(user_id=request.user.id)
            for token in tokens:
                t, _ = BlacklistedToken.objects.get_or_create(token=token)

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
