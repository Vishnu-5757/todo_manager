from django.urls import path
from . import views



urlpatterns = [
    path('home',views.home,name="home"),
    path('register',views.register,name="register"),
    path('login',views.loginPage,name="login"),
    path('logout',views.LogoutPage,name="logout"),
    path('my_project/<int:project_id>/', views.my_project, name='my_project'),
    path('delete_todo/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('update_todo_status/<int:todo_id>/', views.update_todo_status, name='update_todo_status'),
    path('edit_todo/<int:todo_id>', views.edit_todo, name='edit_todo'),
    path('update_project_name/', views.update_project_name, name='update_project_name'),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),
    path('export_gist/<int:project_id>/', views.export_as_gist, name='export_gist'),
]