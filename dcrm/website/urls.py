from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name="home" ),
    path("crm/",views.crm,name="crm" ),
    path("login/",views.login_user,name="login"),
    path("logout/",views.logout_user,name="logout"),
    path("signup/",views.signup_user,name="signup"),
    path("record/<int:pk>/",views.customer_record,name="record"),
    path("delete/<int:pk>/",views.delete_record,name="delete"),
    path("add_record/",views.add_record,name="add_record"),
    path("update_record/<int:pk>/",views.update_record,name="update_record"),
]