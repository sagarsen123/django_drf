from home.views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# registering in the router
router = DefaultRouter()
router.register(r'people', PeopleViewSet, basename='people')
urlpatterns = router.urls


urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterAPI.as_view()),
    path('login-user/', LoginAPI.as_view()),
    path('index/', index),
    path('login/', login),
    path('person/', people),
    path('personapi/',  PersonApi.as_view())
]
