from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quotes.urls')),        # Твої цитати
    path('users/', include('users.urls')),    # ПІДКЛЮЧАЄМО НАШ НОВИЙ ФАЙЛ СЮДИ!
]