from django.contrib import admin
from .models import Post

admin.site.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted')
    list_filter = ('author', 'date_posted')
    search_fields = ('title', 'content')
    list_per_page = 20
    list_editable = ('date_posted',)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()