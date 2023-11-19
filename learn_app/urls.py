from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.UserLoginView.as_view()),
    path('logout/', views.UserLogoutView.as_view()),
    path('register/', views.SignupView.as_view()),

    path('user/', views.GetUserProfileView.as_view()),

    path('<str:name>/categories/', views.CategoryView.as_view()),
    path('categories/<int:pk>/', views.QuestionCardView.as_view()),
    path('categories/<int:pk>/<int:question_card_id>', views.QuestionView.as_view()),
    #ids are category id/ question card id
  
]

