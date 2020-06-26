from django.contrib import admin

from .models import User, Message


class MessageInline(admin.StackedInline):
    model = Message
    extra = 3


class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['username']}),
        (None,               {'fields': ['email']}),
        ('Date information', {'fields': ['date_joined'], 'classes': ['collapse']}),
    ]
    inlines = [MessageInline]
    list_display = ('username', 'email', 'date_joined')


admin.site.register(User, UserAdmin)

