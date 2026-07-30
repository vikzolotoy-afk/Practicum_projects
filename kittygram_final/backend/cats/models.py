from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Achievement(models.Model):
    """Модель для хранения видов достижений котов."""
    name = models.CharField(max_length=64)

    def __str__(self):
        """Вернуть название достижения."""
        return self.name


class Cat(models.Model):
    """Модель, представляющая питомца."""
    name = models.CharField(max_length=16)
    color = models.CharField(max_length=16)
    birth_year = models.IntegerField()
    owner = models.ForeignKey(
        User, related_name='cats',
        on_delete=models.CASCADE
    )
    achievements = models.ManyToManyField(
        Achievement,
        through='AchievementCat'
    )
    image = models.ImageField(
        upload_to='cats/images/',
        null=True,
        default=None
    )

    def __str__(self):
        """Вернуть кличку кота."""
        return self.name


class AchievementCat(models.Model):
    """Промежуточная модель для связи котов и их достижений."""
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        """Вернуть строку вида 'Достижение Кот'."""
        return f'{self.achievement} {self.cat}'
