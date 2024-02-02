from django.urls import path

from users.apps import UsersConfig
from users.views import (CheckReferralCode, UsersReferredByCurrentUser, PhoneAuthorizationView,
                         RefreshTokenView, PhoneNumberAndCodeTokenObtainPairView,
                         UserRetrieveAPIView, UserUpdateAPIView, UserDestroyAPIView, ChangePasswordView)

app_name = UsersConfig.name


urlpatterns = [
    path('phone-authorization/', PhoneAuthorizationView.as_view(), name='phone-authorization'),
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
]

