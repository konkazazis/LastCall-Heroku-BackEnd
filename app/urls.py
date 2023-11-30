from django.urls import path
from .views import  UserRegister, UserLogin, UserLogout, UserView, home,  ExpenseCreateView, ExpenseDeleteView, ExpenseListView, UserProfileUpdate


urlpatterns = [

    path('', home, name='home'),
    
    path('api/expense-get/', ExpenseListView.as_view(), name='expense-list'),
    path('api/expense-post/', ExpenseCreateView.as_view(), name='expense-create'),
    path('api/expense-delete/<int:pk>', ExpenseDeleteView.as_view(), name='expense-delete'),
    
    path('register', UserRegister.as_view(), name='register'),
    path('login', UserLogin.as_view(), name='login'),
    path('logout', UserLogout.as_view(), name='logout'),
    path('user', UserView.as_view(), name='user view'),

    path('api/user/profile/update/', UserProfileUpdate.as_view(), name='user-profile-update'),
    
]
