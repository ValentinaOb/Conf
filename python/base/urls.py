from . import views
from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/home', views.admin_home, name='admin_home'),    #
    path('admin/to_review', views.to_review, name='to_review'), #
    path('admin/to_review/<int:id>', views.to_review, name='to_review'),    #
    
    path('admin/email_send/', views.email_send, name='email_send'), #
    path('admin/assign_role/', views.assign_role, name='assign_role'),  #

    path('admin/', admin.site.urls),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),

    path('reviewer/home', views.reviewer_home, name='reviewer_home'), #
    path('reviewer/review_status', views.review_status, name='review_status'),#
    path('reviewer/review_status/<int:id>', views.review_status, name='review_status'),#
    path('reviewer/review_file/<int:id>', views.review_file, name='review_file'),    
    #path('reviewer/status_change/<int:id>', views.status_change, name='status_change'),
    path('reviewer/view_description/', views.view_description, name='view_description'),#
    
    path('', views.base, name='base'),#
    path('about/', views.about, name='about'),#
    path('committee/', views.committee, name='committee'),#
    path('schedule/', views.schedule, name='schedule'),#
    path('contact/', views.contact, name='contact'),#
    
    path('sign/', views.sign, name='sign'),#
    path('login/', views.log, name='login'),#

    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="base/password_reset_form.html"),name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="base/password_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="base/password_reset_confirm.html"), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="base/password_reset_complete.html"), name="password_reset_complete"),



    path('logout/', views.logout, name='logout'), #

    path('home/', views.home, name='home'),  #
    path('edit_profile/', views.edit_profile, name='edit_profile'),#
    path('user_profile/', views.user_profile, name='user_profile'),#
    path('change_password/', views.change_password, name='change_password'),   #
    
    path('deactivate_account/', views.deactivate_account, name='deactivate_account'),  # 
    path('deactivate_account/<int:id>', views.deactivate_account, name='deactivate_account'),   #
        
    path('upload/', views.upload, name='upload'),   #
    
    path('update/', views.update, name='update'),   #
    path('update/<int:id>', views.update, name='update'), #
    path('update/updaterecord/<int:id>', views.update, name='update'), #

    path('delete/', views.delete, name='delete'),   #
    path('delete/<int:id>', views.delete, name='delete'),   #
    
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