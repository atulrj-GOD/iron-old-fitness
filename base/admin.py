from django.contrib import admin
from django.utils import timezone
from .models import GymPlan, Member, SupportMessage, Trainer


@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'admin_reply', 'created_at', 'replied_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'message', 'admin_reply')

    def save_model(self, request, obj, form, change):
        """Automatically update replied_at when admin_reply is changed."""
        if 'admin_reply' in form.changed_data and obj.admin_reply:
            obj.replied_at = timezone.now()
        super().save_model(request, obj, form, change)


@admin.register(GymPlan)
class GymPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration')
    search_fields = ('name',)
    ordering = ('price',)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'membership', 'preferred_time', 'payment_confirmed')
    list_filter = ('membership', 'payment_confirmed', 'preferred_time')
    search_fields = ('name', 'email', 'phone')
    ordering = ('name',)


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'specialization', 'experience', 'phone')
    list_filter = ('is_approved', 'specialization')
    search_fields = ('name', 'email', 'specialization')
    ordering = ('name',)

