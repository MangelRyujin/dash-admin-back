from dj_rest_auth.views import LogoutView, PasswordChangeView,UserDetailsView, PasswordResetConfirmView, PasswordResetView
from django.urls import path
from apps.accounts.api.views.admin_view import AdminIdChangePasswordView, AdminListView, AdminRegisterAPIView, AdminToggleStatusAPIView, AdminUpdateAPIView
from apps.accounts.api.views.auth_views import CustomTokenObtainPairView, CustomTokenRefreshView, CustomTokenVerifyView
from apps.accounts.api.views.user_views import  UserRegisterAPIView

urlpatterns = [
    # Base Auth
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password/change/", PasswordChangeView.as_view(), name="password_change"),
    path("user/profile/",UserDetailsView.as_view(),name="user_datail"),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
    path("register/", UserRegisterAPIView.as_view(), name="user-register"),
    path("password/reset/", PasswordResetView.as_view(), name="password_reset"),
    path("password/reset/confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    
    # Admin
    path("admin/", AdminListView.as_view(), name="admin-list"),
    path("admin/register/", AdminRegisterAPIView.as_view(), name="admin-register"),
    path("admin/<int:pk>/change-status/", AdminToggleStatusAPIView.as_view(), name="admin-change-status-by-id"),
    path("admin/<int:pk>/change-password/", AdminIdChangePasswordView.as_view(), name="admin-change-password-by-id"),
    path("admin/<int:pk>/update/", AdminUpdateAPIView.as_view(), name="admin-update-by-id"),
]
