from models import Filter, Category, Feed, Post
from django.contrib import admin

class FilterAdmin(admin.ModelAdmin):
    list_display = ('title', 'filter_on', 'regex', 'ignore_case')

admin.site.register(Filter, FilterAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)

class FeedAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'category')
    list_filter = ('category',)

admin.site.register(Feed, FeedAdmin)

admin.site.register(Post)