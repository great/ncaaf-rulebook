from rule.models import Meta, Title, Article
from django.contrib import admin


class TitleAdmin(admin.ModelAdmin):
	#search_fields = ['lang']
	list_filter = ['lang']
	list_display = ('index', 'text')


class ArticleAdmin(admin.ModelAdmin):
	list_filter = ['lang']
	list_display = ('index', 'title', 'content')


admin.site.register(Meta)
admin.site.register(Title, TitleAdmin)
admin.site.register(Article, ArticleAdmin)
