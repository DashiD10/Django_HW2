from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default='BRUTAL Barbershop')
    phone = models.CharField(max_length=20, default='+7 (999) 123-45-67')
    
    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'

class Order(models.Model):
    STATUS_CHOICES = (
        ("new", "Новый"),
        ("confirmed", "Подтвержден"),
        ("completed", "Завершен"),
        ("canceled", "Отменен"),
    )

    name = models.CharField(max_length=100, verbose_name="Имя клиента")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="new", verbose_name="Статус")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    master = models.ForeignKey("Master", on_delete=models.SET_NULL, null=True, verbose_name="Мастер")
    appointment_date = models.DateTimeField(verbose_name="Дата и время записи")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"{self.name} - {self.phone}"

class Master(models.Model):
    name = models.CharField(max_length=150, verbose_name="Имя")
    photo = models.ImageField(upload_to="masters/", blank=True, verbose_name="Фотография")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    addres = models.CharField(max_length=255, verbose_name="Адрес")
    experience = models.PositiveIntegerField(verbose_name="Стаж работы", help_text="Опыт работы в годах")
    services = models.ManyToManyField("Service", related_name="masters", verbose_name="Услуги")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    duration = models.PositiveIntegerField(verbose_name="Длительность", help_text="Время выполнения в минутах")
    is_popular = models.BooleanField(default=False, verbose_name="Популярная услуга")
    image = models.ImageField(upload_to="services/", blank=True, verbose_name="Изображение")

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.name


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1 звезда'),
        (2, '2 звезды'),
        (3, '3 звезды'),
        (4, '4 звезды'),
        (5, '5 звезд'),
    )

    text = models.TextField(verbose_name="Текст отзыва")
    client_name = models.CharField(max_length=100, blank=True, verbose_name="Имя клиента")
    master = models.ForeignKey("Master", on_delete=models.CASCADE, verbose_name="Мастер")
    photo = models.ImageField(upload_to="reviews/", blank=True, null=True, verbose_name="Фотография")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Оценка"
    )
    is_published = models.BooleanField(default=True, verbose_name="Опубликован")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Отзыв от {self.client_name or 'Аноним'} на {self.master.name}"
