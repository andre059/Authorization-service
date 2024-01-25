from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from users.apps import UsersConfig
from users.views import UserProfile, CheckReferralCode, \
    UsersReferredByCurrentUser, PhoneAuthorizationView, CreateUserView

app_name = UsersConfig.name


# router = DefaultRouter()
# router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('phone-authorization/', PhoneAuthorizationView.as_view(), name='phone-authorization'),
    path('create-user/', CreateUserView.as_view(), name='create-user'),
    path('user-profile/', UserProfile.as_view(), name='user-profile'),
    path('check-referral/', CheckReferralCode.as_view(), name='check-referral'),
    path('referred-users/', UsersReferredByCurrentUser.as_view(), name='referred-users'),

    # JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]  # + router.urls
