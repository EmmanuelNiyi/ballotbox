from django.urls import path, re_path

from accounts.views import CreateRoleView, GetAllRolesView, CreateUserView, ActivateView, UserLoginView, \
    SendActivationCodeView, UserProfileDetailView, GetAllUserProfilesView, GetUserAccountDetailsView

# urlpatterns = [
#     path('invite/', InviteClientView.as_view(), name='invite'),
#
# ]

urlpatterns = [
    path('role/create/', CreateRoleView.as_view()),
    path('role/get/all/', GetAllRolesView.as_view()),

    path('register/', CreateUserView.as_view()),
    path('activate/user/', ActivateView.as_view()),
    path('send/code/', SendActivationCodeView.as_view()),
    path('login/', UserLoginView.as_view()),

    path('user/details/', GetUserAccountDetailsView.as_view()),

    # path('profile/', UserProfileView.as_view()),
    path('user/profile/<int:user>/', UserProfileDetailView.as_view()),
    path('user/profile/all/', GetAllUserProfilesView.as_view()),

]
