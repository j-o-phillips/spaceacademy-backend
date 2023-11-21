from django.urls import path
from . import views

urlpatterns = [
    path('ship/', views.ShipView.as_view()),
    path('hangars/', views.HangarView.as_view()),
    path('hangars/<int:hangar_id>/', views.HangarDetailView.as_view()),
    path('posts/<int:hangar_id>/', views.PostView.as_view()),
    # path('ship/thrusters/', views.ShipView.as_view),
    # path('ship/weapons/', views.ShipView.as_view),
    # path('ship/shields/', views.ShipView.as_view)
  
]
