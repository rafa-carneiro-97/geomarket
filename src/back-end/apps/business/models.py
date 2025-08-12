from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.core.exceptions import ValidationError


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

    name = models.CharField(
        verbose_name="nome",
        max_length=128,
        blank=False,
        null=False,
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
        verbose_name = "loja"
        verbose_name_plural = "lojas"

    def __str__(self):
        return f"{self.id}"


class StorePermission(models.Model):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        verbose_name="ID",
    )

    store = models.ForeignKey(
        Store,
        verbose_name="loja",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        db_index=True,
    )

    name = models.CharField(
        verbose_name="nome",
        max_length=255,
        null=False,
        blank=False,
    )

    codename = models.CharField(
        verbose_name="codinome",
        max_length=100,
        null=False,
        blank=False,
        db_index=True,
    )

    content_type = models.ForeignKey(
        ContentType,
        verbose_name="content type",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    class Meta:
        managed = True
        constraints = [
            models.UniqueConstraint(
                fields=["store", "codename"], name="unique_store_permission"
            )
        ]
        verbose_name = "lojas → permissão"
        verbose_name_plural = "lojas → permissões"

    def __str__(self):
        return f"{self.store.name} — {self.codename}"


class StoreGroup(models.Model):
    store = models.ForeignKey(
        Store,
        verbose_name="loja",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        db_index=True,
    )

    name = models.CharField(
        verbose_name="nome",
        max_length=255,
        null=False,
        blank=False,
    )

    permissions = models.ManyToManyField(
        StorePermission,
        verbose_name="permissões",
        help_text="Permissões específicas para o grupo.",
        blank=True,
    )

    class Meta:
        managed = True
        constraints = [
            models.UniqueConstraint(fields=["store", "name"], name="unique_store_group")
        ]
        verbose_name = "lojas → grupo"
        verbose_name_plural = "lojas → grupos"

    def __str__(self):
        return f"{self.store.name} — {self.name}"

    def clean(self):
        if self.pk:
            # Ensure all permissions belong to the same store
            is_invalid = self.permissions.exclude(store=self.store).exists()
            if is_invalid:
                raise ValidationError(
                    {
                        "permissions": "Todos as pemissões do grupo devem pertencer à mesma loja do mesmo."
                    }
                )

        super().clean()


class Employee(models.Model):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        verbose_name="ID",
    )

    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        verbose_name="loja",
        null=False,
        blank=False,
        db_index=True,
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="usuário",
        null=False,
        blank=False,
        db_index=True,
    )

    is_admin = models.BooleanField(
        verbose_name="é administrador geral",
        default=False,
        help_text="Designa que este funcionário tem todas as permissões da loja sem atribuí-las explicitamente",
    )

    permissions = models.ManyToManyField(
        StorePermission,
        verbose_name="permissões da loja",
        help_text="Permissões específicas para o funcionário.",
        blank=True,
        db_index=True,
    )

    groups = models.ManyToManyField(
        StoreGroup,
        verbose_name="grupos da loja",
        help_text="Grupos que o funcionário faz parte.",
        blank=True,
        db_index=True,
    )

    class Meta:
        managed = True
        constraints = [
            models.UniqueConstraint(fields=["store", "user"], name="unique_employee")
        ]
        verbose_name = "funcionário"
        verbose_name_plural = "funcionários"

    class StorePermissions:
        default = "CRUD"

    def __str__(self):
        return f"{self.store.name} — {self.user.first_name}"

    def clean(self):
        # Ensure all permissions belong to the same store
        if self.pk:
            is_invalid = self.permissions.exclude(store=self.store).exists()
            if is_invalid:
                raise ValidationError(
                    {
                        "permissions": "Todos as pemissões do fuincionário devem pertencer à mesma loja do mesmo."
                    }
                )

        if self.pk:
            is_invalid = self.groups.exclude(store=self.store).exists()
            if is_invalid:
                raise ValidationError(
                    {
                        "groups": "Todos os grupos do funcionário devem pertencer à mesma loja do mesmo."
                    }
                )

        return super().clean()

    def _get_cache_key(self) -> str:
        return f"emp-{self.pk}:store_perms:store-{self.store.id}"

    def has_permission(self, codename: str, use_cache=True):
        return codename in self.get_all_permissions(use_cache=use_cache)

    def get_all_permissions(self, use_cache=True) -> set:
        if self.is_admin:
            return True

        key = self._get_cache_key()
        if use_cache:
            cached = cache.get(key)
            if cached is not None:
                return set(cached)

        employee_perms = self.permissions.values_list("codename", flat=True).all()
        employee_groups = self.groups.values_list(
            "permissions__codename", flat=True
        ).all()

        permissions = set(employee_perms) | set(employee_groups)

        cache.set(key, list(permissions), 30 * 60)  # 30 minutes default)

        return permissions

    def has_perm(self, codename, use_cache=True):
        return codename in self.get_all_permissions(use_cache=use_cache)

    def delete_perm_cache(self):
        cache.delete(self._get_cache_key())
