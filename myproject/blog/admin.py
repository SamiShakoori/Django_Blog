from django.contrib import admin
from .models import Article, Category
from django.contrib import messages
from django.utils.translation import ngettext

# Register your models here.
def make_published(modeladmin, request, queryset):
    updated = queryset.update(status='p')
    modeladmin.message_user(request, ngettext(
        '%d مقاله منتشر شد.',
        '%d مقاله منتشر شدند.',
        updated,
    ) % updated, messages.SUCCESS)
make_published.short_description = 'انتشار مقالات انتخاب شده'

def make_draft(modeladmin, request, queryset):
    updated = queryset.update(status='d')
    modeladmin.message_user(request, ngettext(
        '%d مقاله پیش نویس شد',
        '%d مقاله پیش نویس شدند',
        updated,
    ) % updated, messages.SUCCESS)
make_draft.short_description = 'پیش نویس شدن مقالات انتخاب شده'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position', 'title', 'slug', 'parent', 'status')
    list_filter = (['status'])
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category, CategoryAdmin)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'jpublish', 'status', 'category_to_str')
    list_filter = ('publish', 'status')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-status', '-publish']
    actions = [make_published, make_draft]

    def category_to_str(self, obj):
        return ", ".join([category.title for category in obj.category_published()])
    category_to_str.short_description = 'زمان انتشار'

admin.site.register(Article, ArticleAdmin)
