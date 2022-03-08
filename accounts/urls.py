from django.urls import path
from .views import GetInformationUser, SignupView, GetCSRFToken, LoginView, LogoutView, CheckAuthenticatedView, DeleteAccountView

urlpatterns = [
    path('authenticated', CheckAuthenticatedView.as_view()),
    path('get_user', GetInformationUser.as_view()),
    path('register', SignupView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('delete', DeleteAccountView.as_view()),
    path('csrf_cookie', GetCSRFToken.as_view())
]