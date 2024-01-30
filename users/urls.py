from django.urls import path
from rest_framework.routers import DefaultRouter

from users.apps import UsersConfig
from users.views import (CheckReferralCode, UsersReferredByCurrentUser, PhoneAuthorizationView,
                         RefreshTokenView, PhoneNumberAndCodeTokenObtainPairView,
                         UserRetrieveAPIView, UserUpdateAPIView, UserDestroyAPIView, ChangePasswordView)

app_name = UsersConfig.name


# router = DefaultRouter()
# router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('phone-authorization/', PhoneAuthorizationView.as_view(), name='phone-authorization'),
    # path('create-user/', CreateUserView.as_view(), name='create-user'),
    # path('user-profile/<int:pk>/', UserProfile.as_view(), name='user-profile'),
    path('check-referral/', CheckReferralCode.as_view(), name='check-referral'),
    path('referred-users/', UsersReferredByCurrentUser.as_view(), name='referred-users'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),

    # generics
    path('user/<int:pk>/', UserRetrieveAPIView.as_view(), name='user-retrieve'),
    path('user/update/<int:pk>/', UserUpdateAPIView.as_view(), name='user-update'),
    path('user/delete/<int:pk>/', UserDestroyAPIView.as_view(), name='user-delete'),

    # JWT
    path('phone-token/', PhoneNumberAndCodeTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
]  # + router.urls
