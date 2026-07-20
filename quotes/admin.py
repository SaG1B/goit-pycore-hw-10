from django.contrib import admin
from .models import Author, Tag, Quote

# Реєструємо моделі в адмінці Django
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Quote)