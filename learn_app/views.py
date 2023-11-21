from django.contrib.auth.models import User, Group 
from rest_framework import viewsets, permissions, generics
from .serializers import UserSerializer, GroupSerializer, QuestionCardSerializer, UserProfileSerializer, CategoryCardSerializer, QuestionSerializer, AnswerSerializer
from django.http import HttpResponse, JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate, logout
from .models import QuestionCard, UserProfile, Category, Planet, Question, Answer, LockedCards
from rest_framework.authtoken.views import ObtainAuthToken
from game_app.models import Ship, Weapons, Thrusters, Shields, Engines

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
                    print(user.username)
                    user_profile = UserProfile(user=user, username=user.username, first_name='', last_name='', experience=0, credits=0, prestige=0)
                    user_profile.save()
                    #assign ship
                    engines = Engines.objects.get(id=1)
                    shields = Shields.objects.get(id=1)
                    weapons = Weapons.objects.get(id=1)
                    thrusters = Thrusters.objects.get(id=1)
                    
                    ship = Ship(user_profile=user_profile, name='Sirius', weapons=weapons, engines=engines, thrusters=thrusters, shields=shields)
                    ship.save()
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
        user = self.request.user
        user = User.objects.get(id=user.id)

        cards_in_category = QuestionCard.objects.filter(category_id=pk)
        print(cards_in_category)

        unlocked_cards = cards_in_category.exclude(
            id__in=LockedCards.objects.filter(user_id=user.id).values('question_card_id')
        )

        print(unlocked_cards)

        data = QuestionCardSerializer(unlocked_cards, many=True)

        return JsonResponse({'data': data.data })
        
class QuestionView(APIView):
    def get(self, request, pk, question_card_id, format=None):
        data = Question.objects.filter(question_card_id=question_card_id)
        print(data)

        data = QuestionSerializer(data, many=True)

        return JsonResponse({'data': data.data })

class AnswerView(APIView):
    #initial user answer
    def post(self, request, pk, question_card_id, question_id):
        user = self.request.user
        data = self.request.data
        choice = data['choice']

        #get correct question
        question = Question.objects.get(id=question_id)
        #check if user has already answered this question
        try:
            answer_present = Answer.objects.get(question_id=question_id, user=user) 
        
            return JsonResponse({'message': 'Answer already given'})
        except:
            #Save it to db
            answer = Answer.objects.create(user=user, question=question, user_answer=choice)
            answer.save()
            #check if answer is correct
            if str(question.correct_answer) == str(choice):
                return JsonResponse({'message': 'correct'})
            else:
                return JsonResponse({'message': 'incorrect'})

 
class checkCardAnswers(APIView):       
    def get(self, request, pk, question_card_id, format=None):
        user = self.request.user
        user = User.objects.get(id=user.id)

        #get all questions from question card
        question_card = QuestionCard.objects.get(id=question_card_id)
        questions = question_card.question_set.all()

        #for each question check if the user answer matches the correct answer
        reward_divider = 1
        try:
            for question in questions:
                
                userAnswer = Answer.objects.filter(user=user).get(question=question.id)
                if userAnswer:
                    print(question.correct_answer)
                    print(userAnswer)
                    if str(question.correct_answer) == str(userAnswer):
                        print('correct')
                    else:
                        reward_divider += 1
        except:
            return JsonResponse({'message': 'Answer all the questions'})

        #add credits and exp to profile
        profile = UserProfile.objects.get(user=user)
        credits_to_add = question_card.reward_credits / reward_divider
        profile.update_credits(credits_to_add)
        profile.update_experience(question_card.reward_exp)
        profile.save()
        #update locked cards
        new_locked_card = LockedCards.objects.create(user=user, question_card=question_card)
        new_locked_card.save()
     
        return JsonResponse({'reward divider': reward_divider,
                              'reward_experience' : question_card.reward_exp,
                              'reward_credits' : credits_to_add
                              })