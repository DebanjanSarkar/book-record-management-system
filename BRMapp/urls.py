from django.urls import re_path
from BRMapp import views

urlpatterns = [
    re_path('new-book',views.newBook),
    re_path('view-books',views.viewBooks),
    re_path('edit-book',views.editBook),
    re_path('delete-book',views.deleteBook),
    re_path('search-book',views.searchBook),
    re_path('add',views.add),
    re_path('edit',views.edit),
    re_path('search',views.search),
    re_path('login',views.userLogin),
    re_path('logout',views.userLogout)
]
