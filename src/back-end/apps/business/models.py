from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Company(models.Model):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        verbose_name="ID",
    )

    CNPJ = models.CharField(
        verbose_name="CNPJ",
        max_length=40,
        blank=False,
        null=False,
        unique=True,
        db_index=True,
    )

    name = models.CharField(
        verbose_name="nome comercial",
        max_length=255,
        null=False,
        blank=False,
    )

    class Meta:
        managed = True
        db_table = "company"
        verbose_name = "empresa"
        verbose_name_plural = "empresas"

    def __str__(self):
        return f"{self.name}"


class Store(models.Model):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        verbose_name="ID",
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="empresa",
        null=False,
        blank=False,
        db_index=True,
    )

    class Meta:
        managed = True
        db_table = "store"
        verbose_name = "loja"
        verbose_name_plural = "lojas"

    def __str__(self):
        return f"{self.id}"


class Emplyee(models.Model):
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        verbose_name="Loja",
        null=False,
        blank=False,
        db_index=True,
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Usuário",
        null=False,
        blank=False,
        db_index=True,
    )

    class Meta:
        managed = True
        constraints = [
            models.UniqueConstraint(fields=["store", "user"], name="unique_store_user")
        ]
        db_table = "user_store_permission"
        verbose_name = "funcionário"
        verbose_name_plural = "funcionários"
