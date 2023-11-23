from django.urls import path
from . import views

urlpatterns = [
    path('ship/', views.ShipView.as_view()),
    path('hangars/', views.HangarView.as_view()),
    path('hangars/<int:hangar_id>/', views.HangarDetailView.as_view()),
    path('posts/<int:hangar_id>/', views.PostView.as_view()),
    path('posts/delete/<int:post_id>/', views.DeletePostView.as_view()),
    path('ship/thrusters/', views.ThrusterView.as_view()),
    path('ship/weapons/', views.WeaponView.as_view()),
    path('ship/shields/', views.ShieldView.as_view()),
    path('ship/engines/', views.EngineView.as_view()),
  
]
