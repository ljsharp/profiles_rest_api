from django.urls import path, include
from rest_framework.routers import DefaultRouter


from profiles_api import views

router = DefaultRouter()
router.register('profile', views.UserProfileViewset, basename="profile")

urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),
    path('login/', views.UserLoginView.as_view(), name="login"),
    path('', include(router.urls))
]