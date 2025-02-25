from django.contrib import admin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.detail import DetailView
from django.urls import path, reverse
from django.utils.html import format_html

from .models import User, Work, User_Data


@admin.action(description="Accept_Work")
def accept_work(ModelAdmin, request, queryset):
    work_to_ship = queryset.exclude(status=Work.WorkStatus.Accept)
    works = list(work_to_ship)

    work_to_ship.update(status=Work.WorkStatus.Accept)

    for work in works:
        user=work.user
        user.email_user(
            'Your Work has been Accepted',
            f'Dear {user.username}, \n\n Your work "{work.title}" has been accepted.',
            'admin@example.com',
            fail_silently=False
        )
        ModelAdmin.message_user(
            request,
            "Selected work have been marked as Accept and user have been notified."
        )

@admin.action(description="Refuse_Work")
def refuse_work(ModelAdmin, request, queryset):
    work_to_ship = queryset.exclude(status=Work.WorkStatus.Refuse)
    works = list(work_to_ship)

    work_to_ship.update(status=Work.WorkStatus.Refuse)

    for work in works:
        user=work.user
        user.email_user(
            'Your Work has been Refused',
            f'Dear {user.username}, \n\n Your work "{work.title}" has been refused.',
            'admin@example.com',
            fail_silently=False
        )
        ModelAdmin.message_user(
            request,
            "Selected work have been marked as Refuse and user have been notified."
        )

@admin.action(description="Review_Work")
def review_work(ModelAdmin, request, queryset):
    work_to_ship = queryset.exclude(status=Work.WorkStatus.Review)
    works = list(work_to_ship)

    work_to_ship.update(status=Work.WorkStatus.Review)

    for work in works:
        user=work.user
        user.email_user(
            'Your Work has been Reviewed',
            f'Dear {user.username}, \n\n Your work "{work.title}" has been Reviewed.',
            'admin@example.com',
            fail_silently=False
        )
        ModelAdmin.message_user(
            request,
            "Selected work have been marked as Review and user have been notified."
        )

@admin.action(description="Direct to expert")
def direct_to_expert(ModelAdmin, request, queryset):
    User.groups.filter(name="expert").exists()


    queryset.update(status=Work.WorkStatus.Review)



@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ['title', 'category','user','uploaded_at', 'status']
    ordering = ["uploaded_at"]
    actions = [accept_work, refuse_work, review_work, direct_to_expert]




'''@admin.register(User_Data)
class UserAdmin(admin.ModelAdmin):
    list_display = ['user']


class WorkItemInline(admin.TabularInline):
    model = Work
    
@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'user', 'detail']
    inlines = [WorkItemInline]
      def get_urls(self):
        return [
            path(
                "<pk>/detail",
                self.admin_site.admin_view(WorkDetailView.as_view()),
                name=f"products_order_detail",
            ),
            *super().get_urls(),
        ]

    def detail(self, obj: Work) -> str:
        url = reverse("admin:user_work_detail", args=[obj.pk])
        return format_html(f'<a href="{url}">📝</a>')


class WorkDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "user.view_work"
    template_name = "admin/python/work/detail.html"
    model = Work.user
   
class WorkAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'user', 'detail']
    inlines = [WorkItemInline]

    def get_urls(self):
        return [
            path(
                "<pk>/detail",
                self.admin_site.admin_view(WorkDetailView.as_view()),
                name=f"products_work_detail",
            ),
            *super().get_urls(),
        ]

    def detail(self, obj: Work) -> str:
        url = reverse("admin:work_detail", args=[obj.pk])
        return format_html(f'<a href="{url}">📝</a>')

class WorkItemInline(admin.TabularInline):
    model = Work

class WorkDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "work.view_work"
    template_name = "admin/work/detail.html"
    model = Work
'''
   

    