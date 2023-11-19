from django.contrib.auth.models import User, Group 
from rest_framework import viewsets, permissions, generics
from .serializers import UserSerializer, GroupSerializer, QuestionCardSerializer, UserProfileSerializer, CategoryCardSerializer, QuestionSerializer
from django.http import HttpResponse, JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate, logout
from .models import QuestionCard, UserProfile, Category, Planet, Question
from rest_framework.authtoken.views import ObtainAuthToken

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class= UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class= GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

##!USER REGISTER AND LOGIN

class SignupView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        data = self.request.data 

        username = data['username']
        password = data['password']
        re_password = data['re_password']

        if password == re_password:
            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'})
            else:
                if len(password) < 6:
                    return JsonResponse({'error': 'Password must be atleas 6 characters'})
                else:
                    user = User.objects.create_user(username=username, password=password)
                    user.save()

                    user = User.objects.get(id=user.id)
                    print(user.id)
                    user_profile = UserProfile(user=user, first_name='', last_name='', experience=0, credits=0, prestige=0)
                    user_profile.save()

                    return JsonResponse({'success': 'User created succesfully'})
        else:
            return JsonResponse({'error': 'Passwords do not match'})

class UserLoginView(ObtainAuthToken):
    def post(self, request):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_superuser': user.is_superuser,

        })
        else:
            return Response({'error': 'Invalid credentials'}, status=401)
        
# class CheckAuthenticatedView(APIView):
#     def get(self, request, format=None):
#         isAuthenticated = User.is_authenticated

#         if isAuthenticated:
#             return JsonResponse({ 'isAuthenticated': 'success'})
#         else:
#             return JsonResponse({'isAuthenticated': 'error'})
        
class UserLogoutView(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return JsonResponse({'success': 'Token deleted'})
    
##! USER PROFILE

class GetUserProfileView(APIView):
    def get(self, request, format=None):
        user = self.request.user
        username = user.username
        user = User.objects.get(id=user.id)

        user_profile = UserProfile.objects.get(user=user)
        user_profile = UserProfileSerializer(user_profile)

        return JsonResponse({'profile': user_profile.data, 'username': str(username) })
    
class UpdateUserProfileView(APIView):
    def put(self, request, format=None):
        user = self.request.user
        username = user.username
        user = User.objects.get(id=user.id)

        data = self.request.data
        experience = data['experience']
        credits = data['credits']
        prestige = data['prestige']

        UserProfile.objects.filter(user=user).update(experience=experience, credits=credits, prestige=prestige)
        
        user_profile = UserProfile.objects.get(user=user)
        user_profile = UserProfileSerializer(user_profile)

        return JsonResponse({'profile': user_profile.data, 'username': str(username) })
    

class CategoryView(generics.ListAPIView):
    def get(self, request, name, format=None):
        planet_name = Planet.objects.get(name=name)
        print(f"planet name: {planet_name}")

        categories = Category.objects.filter(planet_id=planet_name)
        print(categories)

        data = CategoryCardSerializer(categories, many=True)

        return JsonResponse({'data': data.data })

class QuestionCardView(APIView):
    def get(self, request, pk, format=None):
        data = QuestionCard.objects.filter(category_id=pk)
        print(data)

        data = QuestionCardSerializer(data, many=True)

        return JsonResponse({'data': data.data })
        
class QuestionView(APIView):
    def get(self, request, pk, question_card_id, format=None):
        data = Question.objects.filter(question_card_id=question_card_id)
        print(data)

        data = QuestionSerializer(data, many=True)

        return JsonResponse({'data': data.data })

