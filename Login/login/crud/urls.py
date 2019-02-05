from django.conf.urls import url
from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from . import views
from .views import list,DetailCreate,DetailUpdate,DetailDelete,user_list,login_view,change_password,UsersListView,NameDetailView
from django.contrib.auth.views import password_reset,password_reset_done,password_reset_confirm,password_reset_complete

# app_name = "crud"

urlpatterns = [
    #path('admin/', admin.site.urls),

    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view,name='login'),
    path('logout/', auth_views.logout, name='logout'),
    path('',views.list,name='list'),
    path('create/',DetailCreate.as_view(success_url="/"),name='create'),
    path('update/<pk>',DetailUpdate.as_view(success_url='/'),name='update'),
    path('delete/<pk>',DetailDelete.as_view(success_url='/'),name='delete'),
    path('userlist/',user_list.as_view(),name='user_list'),
    path('change/',views.change_password,name='changepassword'),
    path('detail/<pk>',NameDetailView.as_view(),name='Detail'),
    path('reset-password/',password_reset,name='reset_password'),
    path('reset-password/done/',password_reset_done,{'template_name': 'registration/password_reset_done.html'},name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm,name='password_reset_confirm'),
    path('reset-password/complete/',password_reset_complete,name='password_reset_complete'),
    path('celery/', views.UsersListView.as_view(), name='users_list'),
    #url('generate/', views.forgot_password, name='generate'),
    #url('stripe/',view=stripe,name=stripe)
]



