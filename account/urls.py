from django.urls import path
from .views import *


urlpatterns = [
    path('registration', signup, name="SIGNUP"),
    path('signin', signin, name="SIGNIN"),
    path('otp/<int:id>', otp, name="otp"),
    path('success', success, name="success"),
    path('signout', signout, name="signout"),
]
