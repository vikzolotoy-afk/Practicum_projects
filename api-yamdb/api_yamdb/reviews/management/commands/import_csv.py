"""Импорт всех CSV файлов."""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import Category, Genre, Title, Review, Comment
from .utils import import_csv, import_title_genres


# import_csv.py:20:10: N806 variable 'User' in function should be lowercase
# Вынес из класса Command
User = get_user_model()


class Command(BaseCommand):
    """Реализация команды для импорта."""

    help = "Импорт всех CSV."

    def handle(self, *args, **options):
        """
        Импорт реализован с помощью цикла.

        genre_title реализован отдельно из-за связи Many To Many
        """
        Comment.objects.all().delete()
        Review.objects.all().delete()
        Title.objects.all().delete()
        Genre.objects.all().delete()
        Category.objects.all().delete()
        User.objects.all().delete()

        csv_models = [
            ('static/data/category.csv', Category),
            ('static/data/genre.csv', Genre),
            ('static/data/users.csv', User),
            ('static/data/titles.csv', Title),
            ('static/data/review.csv', Review),
            ('static/data/comments.csv', Comment),
        ]

        for file_path, model_class in csv_models:
            import_csv(file_path, model_class)

        import_title_genres('static/data/genre_title.csv')

        self.stdout.write(self.style.SUCCESS("Импорт всех CSV завершен!"))
        self.stdout.write(f"Category   : {Category.objects.count()}")
        self.stdout.write(f"Genre      : {Genre.objects.count()}")
        self.stdout.write(f"User       : {User.objects.count()}")
        self.stdout.write(f"Title      : {Title.objects.count()}")
        self.stdout.write(f"Review     : {Review.objects.count()}")
        self.stdout.write(f"Comment    : {Comment.objects.count()}")
