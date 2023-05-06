from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from api.v1.permissions import IsAdmin
from api_yamdb.settings import FROM_EMAIL
from users.serializers import MyTokenObtainPairSerializer, \
    UserSignupSerializer, UserSerializer
from users.models import User


class MeAPIView(APIView):
    def get(self, request):
        user = User.objects.get(username=request.user.username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        data = request.data
        if data.get('role'):
            return Response('Forbidden to change role',
                            status=status.HTTP_403_FORBIDDEN)
        user = User.objects.get(username=request.user.username)
        serializer = UserSerializer(user, data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [IsAdmin]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'


class GetTokenView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserSignupAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSignupSerializer

    @staticmethod
    def send_code(user, email):
        code = default_token_generator.make_token(user)
        send_mail(
            subject=f'YaMDb: confirmation code for {email}',
            message=f'Dear Sir/Madam,\n\n'
                    f'Your confirmation code for YaMDb:\n{code}\n\n'
                    f'--\n'
                    f'Best regards,\n'
                    f'YaMDb Team',
            from_email=FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

    def post(self, request):
        serializer = UserSignupSerializer(data=self.request.data)
        email = serializer.initial_data.get('email')
        username = serializer.initial_data.get('username')

        if User.objects.filter(username=username, email=email).exists():
            user = User.objects.get(username=username, email=email)
            self.send_code(user, email)
            return Response(serializer.initial_data, status=status.HTTP_200_OK)

        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=username, email=email)
            self.send_code(user, email)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
