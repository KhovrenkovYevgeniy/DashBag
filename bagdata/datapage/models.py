from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва")
    code = models.CharField(max_length=50, verbose_name="Код")
    quantity = models.IntegerField(verbose_name="Кількість")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    provider_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна закупки")
    arrived_date = models.DateField(verbose_name="Дата")
    expiration_date = models.DateField(verbose_name="Тер. придатності")

    class Meta:
        ordering = ('-arrived_date', 'name')



class Story(models.Model):
    name = models.CharField(verbose_name="Назва", max_length=255)
    code = models.CharField(max_length=50, verbose_name="Код")
    quantity_of_sold = models.IntegerField(verbose_name="Кількість")
    sold_date = models.DateField(auto_now_add=True, verbose_name="Дата")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")