from django.contrib import admin

# Register your models here.
from .models import Question, Choice
from .role_models import Role

class choiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [(None, {"fields": ['pub_date']}), ("DateInformation", {"fields": ['question_text']})]
    inlines = [choiceInline]
    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]

class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['users']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Role, RoleAdmin)