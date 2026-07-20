from django import forms
from .models import Author, Quote, Tag

class AuthorForm(forms.ModelForm):
    fullname = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ім\'я автора'})
    )
    born_date = forms.CharField(
        max_length=50, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Дата народження (наприклад: March 14, 1879)'})
    )
    born_location = forms.CharField(
        max_length=150, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Місце народження'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Біографія автора'})
    )

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


class QuoteForm(forms.ModelForm):
    quote = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Текст цитати'})
    )
    # Зв'язок з автором: випадаючий список вибору
    author = forms.ModelChoiceField(
        queryset=Author.objects.all(),
        empty_label="Оберіть автора",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    # Поле для введення тегів через кому (простий і зручний спосіб)
    tags_input = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть теги через кому (наприклад: life, love, books)'}),
        label="Теги"
    )

    class Meta:
        model = Quote
        fields = ['quote', 'author']

    def save(self, commit=True):
        # Перевизначаємо збереження, щоб автоматично розпарсити теги з рядка
        instance = super().save(commit=False)
        if commit:
            instance.save()
        
        # Обробляємо теги
        tags_data = self.cleaned_data.get('tags_input', '')
        if tags_data:
            # Розбиваємо рядок на окремі теги, прибираємо зайві пробіли
            tag_names = [t.strip() for t in tags_data.split(',') if t.strip()]
            for name in tag_names:
                # Отримуємо або створюємо тег у базі даних
                tag, created = Tag.objects.get_or_create(name=name)
                instance.tags.add(tag)
                
        return instance