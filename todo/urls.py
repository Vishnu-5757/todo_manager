from django.urls import path
from . import views

app_name='todo'


urlpatterns = [
    path('home',views.home,name="home"),
    # path('register',views.register,name="register"),
    # path('',views.loginPage,name="login"),
    path('logout',views.LogoutPage,name="logout"),
    path('my_project/<int:project_id>/', views.my_project, name='my_project'),
    path('delete_todo/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('update_todo_status/<int:todo_id>/', views.update_todo_status, name='update_todo_status'),
    path('edit_todo/<int:todo_id>/', views.edit_todo, name='edit_todo'),
    path('edit_project/<int:project_id>/', views.edit_project, name='edit_project'),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),
    path('export_gist/<int:project_id>/', views.export_as_gist, name='export_gist'),
]