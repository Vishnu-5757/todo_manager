


from django.urls import path
from . import views




app_name='Auth'


urlpatterns = [
    path('register',views.register,name="register"),
    path('',views.loginPage,name="login"),
    path('logout',views.LogoutPage,name="logout"),
]




