from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count

from .models import Quote, Author, Tag
from .forms import AuthorForm, QuoteForm

def main(request):
    """
    Головна сторінка: виводить усі цитати з пагінацією по 10 штук + ТОП-10 тегів.
    """
    quotes_list = Quote.objects.all().order_by('-id')
    paginator = Paginator(quotes_list, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Знаходимо ТОП-10 найпопулярніших тегів за кількістю цитат
    top_tags = Tag.objects.annotate(num_quotes=Count('quotes')).order_by('-num_quotes')[:10]
    
    return render(request, 'quotes/index.html', {'page_obj': page_obj, 'top_tags': top_tags})

@login_required
def add_author(request):
    """
    Додавання нового автора. Доступно тільки авторизованим користувачам.
    """
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Автора успішно додано!")
            return redirect(to='quotes:root')
    else:
        form = AuthorForm()
        
    return render(request, 'quotes/add_author.html', {'form': form})

@login_required
def add_quote(request):
    """
    Додавання нової цитати. Доступно тільки авторизованим користувачам.
    """
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Цитату успішно додано!")
            return redirect(to='quotes:root')
    else:
        form = QuoteForm()
        
    return render(request, 'quotes/add_quote.html', {'form': form})

def author_detail(request, *args, **kwargs):
    """
    Універсальна сторінка автора для перегляду його біографії.
    Приймає будь-які іменовані аргументи з urls.py і дістає ID.
    """
    author_id = list(kwargs.values())[0]  # Беремо перше значення, яке прийшло з URL (наприклад, 9)
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'quotes/author_detail.html', {'author': author})

def quotes_by_tag(request, tag_name):
    """
    Виводить цитати за конкретним тегом (перша сторінка) + ТОП-10 тегів.
    """
    tag = get_object_or_404(Tag, name=tag_name)
    quotes_list = Quote.objects.filter(tags=tag).order_by('-id')
    
    paginator = Paginator(quotes_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    top_tags = Tag.objects.annotate(num_quotes=Count('quotes')).order_by('-num_quotes')[:10]
    
    return render(request, 'quotes/index.html', {'page_obj': page_obj, 'tag': tag, 'top_tags': top_tags})

def quotes_by_tag_paginate(request, tag_name, page):
    """
    Виводить цитати за тегом для конкретної сторінки, переданої через URL-шлях.
    """
    tag = get_object_or_404(Tag, name=tag_name)
    quotes_list = Quote.objects.filter(tags=tag).order_by('-id')
    
    paginator = Paginator(quotes_list, 10)
    page_obj = paginator.get_page(page)
    
    top_tags = Tag.objects.annotate(num_quotes=Count('quotes')).order_by('-num_quotes')[:10]
    
    return render(request, 'quotes/index.html', {'page_obj': page_obj, 'tag': tag, 'top_tags': top_tags})