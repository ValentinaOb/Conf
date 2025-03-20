from . import views
from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    
    path('', views.base, name='base'),
    path('about/', views.about, name='about'),
    path('committee/', views.committee, name='committee'),
    path('schedule/', views.schedule, name='schedule'),
    path('contact/', views.contact, name='contact'),
    
    path('sign/', views.sign, name='sign'),

    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="base/password_reset_form.html"),name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="base/password_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="base/password_reset_confirm.html"), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="base/password_reset_complete.html"), name="password_reset_complete"),



    path('logout/', views.logout, name='logout'),

    path('home/', views.home, name='home'),  
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('change_password/', views.change_password, name='change_password'),   
    
    path('deactivate_account/', views.deactivate_account, name='deactivate_account'),   
        
    path('upload/', views.upload, name='upload'),
    
    path('update/', views.update, name='update'),
    path('update/<int:id>', views.update, name='update'),
    path('update/updaterecord/<int:id>', views.update, name='update'),

    path('delete/', views.delete, name='delete'),
    path('delete/<int:id>', views.delete, name='delete'), 
    
]

'''path('upload/update/', views.update, name='update'),
    path('upload/update/<int:id>', views.update, name='update'),
    path('upload/update/updaterecord/<int:id>', views.update, name='update'),
    
    path('upload/delete/', views.delete, name='delete'),
    path('upload/delete/<int:id>', views.delete, name='delete'), '''

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)