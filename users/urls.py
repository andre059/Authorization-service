from django.urls import path
from rest_framework.routers import DefaultRouter

from users.apps import UsersConfig
from users.views import UserViewSet, UserProfile, CheckReferralCode, \
    UsersReferredByCurrentUser, PhoneAuthorizationView

app_name = UsersConfig.name


router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('phone-authorization/', PhoneAuthorizationView.as_view(), name='phone-authorization'),
    # path('request-authorization/', RequestAuthorizationCode.as_view(), name='request-authorization'),
    path('user-profile/', UserProfile.as_view(), name='user-profile'),
    path('check-referral/', CheckReferralCode.as_view(), name='check-referral'),
    path('referred-users/', UsersReferredByCurrentUser.as_view(), name='referred-users')
] + router.urls
