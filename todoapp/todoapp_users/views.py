from django.shortcuts import render, redirect
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
# Responses
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

# Models
from .models import User

# Serializers
from .serializers import UserSerializer, RegisterUserSerializer, LoginUserSerializer, UpdateUserSerializer

# Register and Authentication methods
from django.contrib.auth import password_validation, authenticate, login, logout

# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated


# Create your views here.
class RegisterUser(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterUserSerializer

    def get(self, request):

        return render(request, 'authentication/register.html')

    def post(self, request, *args, **kwargs):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        password_verification = data.get('password_verification')

        validate_user = User.objects.filter(email=email)

        if validate_user.exists():
            return Response({'error': f'Email {email} already in use.'}, status=HTTP_400_BAD_REQUEST)

        try:
            password_validation.validate_password(password)
        except Exception as err:
            return Response({'error': 'Bad request, verify body parameters.'}, HTTP_400_BAD_REQUEST)

        if password != password_verification:
            return Response({'error': 'Passwords don\'t match.'}, status=HTTP_400_BAD_REQUEST)

        User.objects.create(email=email)
        user = User.objects.filter(email=email)[0]
        user.set_password(password)
        user.save()

        user = authenticate(username=email,
                            password=password)  # If the given credentials are valid, return a User object.
        login(request, user)  # Persist a user id and a backend in the request. This way a user doesn't
        # have to reauthenticate on every request.

        return redirect('list_of_tasks')


class LogoutUser(GenericAPIView):
    serializer_class = RegisterUserSerializer

    def get(self, request):
        logout(request)
        # return redirect('login_user')
        return render(request, 'authentication/new_login.html', context={'logout': 'Just logged out successfully.'})


class LoginUser(GenericAPIView):
    serializer_class = LoginUserSerializer

    def get(self, request):

        if request.user.is_authenticated:
            return redirect('list_of_tasks')

        return render(request, 'authentication/new_login.html')

    def post(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect('list_of_tasks')

        data = request.data
        email = data.get('email')
        password = data.get('password')

        user = User.objects.filter(email=email)

        if not user.exists():
            return render(request, 'authentication/new_login.html', {'error': 'Email don\'t exist.'})
            # return Response({'error', 'Email don\'t exist.'}, status=HTTP_400_BAD_REQUEST)

        user = user[0]

        if not user.check_password(password):
            return render(request, 'authentication/new_login.html', {'error': 'Password isn\'t correct'})
            # return Response({'error': 'Password isn\'t correct.'}, status=HTTP_400_BAD_REQUEST)

        user = authenticate(username=email, password=password)
        login(request, user)

        return redirect('list_of_tasks')
        # return Response({'success': 'User logged in successfully.'}, status=HTTP_200_OK)


class UpdateProfileView(GenericAPIView):
    serializer_class = UpdateUserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def get(self, request):
        return render(request, 'user_example/user_profile.html')

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        mutable_data = data.copy()
        photo = request.FILES.get('photo', False)
        mutable_data.pop('csrfmiddlewaretoken')
        mutable_data.pop('photo')
        context = {}

        if photo is not False:
            user.photo = photo
            user.save()
            context['photo_update'] = 'Profile picture updated successfully.'

        updated_user = User.objects.filter(id=user.id)
        serializer = self.serializer_class(data=mutable_data)
        if serializer.is_valid():
            updated_user.update(**serializer.data)
        else:
            return render(request, 'user_example/user_profile.html',
                          context={'error': 'Something went wrong with the parameters.'}, status=HTTP_400_BAD_REQUEST)

        context['message'] = 'User updated successfully'
        context['user'] = updated_user[0]
        return render(request, 'user_example/user_profile.html',
                      context=context)


class UpdatePhotoView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        photo = request.data.get('photo')

        user.photo = photo
        user.save()

        return redirect('update_user')


def index(request):
    return render(request, 'user_example/index.html')
