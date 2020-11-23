from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register('api/auth', views.AuthViewSet, basename='auth')

urlpatterns = [
    path('get_all/', views.get_all),
    path('get_all_disabled/', views.get_all_disabled),
    path('get_by_id/<int:pk>', views.get_by_id),
    path('create/', views.create),
    path('update/<int:pk>', views.update),
    path('delete/<int:pk>', views.delete),
    path('activate/<int:pk>', views.activate),
    path('login/', views.AuthViewSet.login)
]