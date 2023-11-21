from django.urls import path
from . import views

urlpatterns = [
    path('ship/', views.ShipView.as_view()),
    # path('ship/engines/', views.ShipView.as_view),
    # path('ship/thrusters/', views.ShipView.as_view),
    # path('ship/weapons/', views.ShipView.as_view),
    # path('ship/shields/', views.ShipView.as_view)
  
]
