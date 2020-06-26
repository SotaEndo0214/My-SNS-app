from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'sns'
urlpatterns = [
    path('', views.timeline, name='timeline'),
    path('<int:user_id>/', views.userpage, name='userpage'),
    path('<int:user_id>/<int:message_id>/', views.detail, name='detail'),
    path('<int:user_id>/<int:message_id>/delete_confirm/', views.delete_confirm, name='delete_confirm'),
    path('<int:user_id>/<int:message_id>/delete/', views.delete, name='delete'),
    path('<int:user_id>/<int:message_id>/reply/', views.reply, name='reply'),
    path('<int:user_id>/<int:message_id>/good/', views.good, name='good'),
    path('post/', views.post, name='post'),
    path('edit/', views.edit, name='edit'),
    path('create_account/', views.create_account, name='create_account'),
    path('account_login/', views.account_login, name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)