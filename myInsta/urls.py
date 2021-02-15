from django.urls import path
from . import views

urlpatterns = [
    path('profile/',views.profile_page,name="profile_page"),   
    path('postPage/',views.post_page,name="post_page"),
    path('UpdateProfile/<int:UID>/',views.UpdateProfile,name='UpdateProfile'),
    path('explore/',views.explore,name="explore"),
    path('follow/<int:UID>/',views.follow,name="follow"),
    path('liked/',views.liked,name="liked"),
    path('comments/',views.comments_section,name="comments_section"),
    path('delPost/<int:PID>/',views.delPost,name='delPost'),
]
