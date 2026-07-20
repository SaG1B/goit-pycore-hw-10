import os
import django
from pymongo import MongoClient
from bson.objectid import ObjectId

# 1. Налаштовуємо Django середовище, щоб працювати з моделями
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quotes_site.settings")
django.setup()

# Імпортуємо наші моделі Django після налаштування середовища
from quotes.models import Author, Tag, Quote

# 2. Твоє підключення до MongoDB Atlas
MONGO_URI = "mongodb+srv://admin:secretpass@cluster0.qoggbyc.mongodb.net/homework_08?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "homework_08"

try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    print("Успішно підключилися до MongoDB Atlas!")
except Exception as e:
    print(f"Помилка підключення до MongoDB: {e}")
    exit(1)

def migrate():
    print("Починаємо міграцію даних...")

    # --- 1. Мігруємо авторів ---
    print("Перенесення авторів...")
    authors_collection = db.authors.find()
    
    for author_data in authors_collection:
        fullname = author_data.get("fullname")
        # Перевіряємо, чи такого автора вже немає в базі Django, щоб не дублювати
        author, created = Author.objects.get_or_create(
            fullname=fullname,
            defaults={
                "born_date": author_data.get("born_date"),
                "born_location": author_data.get("born_location"),
                "description": author_data.get("description"),
            }
        )
        if created:
            print(f"Додано автора: {fullname}")
        else:
            print(f"Автор вже існує: {fullname}")

    # --- 2. Мігруємо цитати ---
    print("\nПеренесення цитат...")
    quotes_collection = db.quotes.find()

    for quote_data in quotes_collection:
        text = quote_data.get("quote")
        author_ref = quote_data.get("author")

        author_fullname = None

        # Якщо автор записаний як ID (рядок або ObjectId)
        if author_ref:
            try:
                # Шукаємо документ автора в MongoDB за його _id
                author_doc = db.authors.find_one({"_id": ObjectId(author_ref)})
                if author_doc:
                    author_fullname = author_doc.get("fullname")
                else:
                    # Якщо раптом ID є просто рядком без ObjectId в базі
                    author_doc = db.authors.find_one({"_id": author_ref})
                    if author_doc:
                        author_fullname = author_doc.get("fullname")
            except Exception:
                # Якщо це був не ID, а звичайне ім'я автора у вигляді рядка
                author_fullname = str(author_ref)

        if not author_fullname:
            print(f"Помилка: не вдалося знайти автора для цитати. Пропускаємо.")
            continue

        # Нам потрібно знайти відповідного автора в Django базі
        try:
            author = Author.objects.get(fullname=author_fullname)
        except Author.DoesNotExist:
            print(f"Помилка: автора '{author_fullname}' не знайдено в Django! Пропускаємо цитату.")
            continue

        # Перевіряємо, чи такої цитати ще немає в базі Django
        quote, created = Quote.objects.get_or_create(
            quote=text,
            author=author
        )

        if created:
            # Додаємо теги до цитати
            tags_list = quote_data.get("tags", [])
            for tag_name in tags_list:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                quote.tags.add(tag)
            print(f"Додано цитату автора: {author_fullname}")
        else:
            print(f"Цитата вже існує")

    print("\nМіграція успішно завершена! Перевір адмінку Django.")

if __name__ == "__main__":
    migrate()