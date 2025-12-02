import json, os, uuid, hashlib
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from apps.core import models as core_models, utils as core_utils
from . import widgets, validators


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


class ProductKeyword(models.Model):
    keyword = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="palavra-chave",
    )

    class Meta:
        managed = True
        verbose_name = "produto → palavra-chave"
        verbose_name_plural = "produtos → palavras-chave"

    def __str__(self):
        return self.keyword


class Product(models.Model):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        verbose_name="ID",
    )

    photo = core_models.CustomImageField(
        verbose_name="Foto",
        subdir="uploads/images/products/photo/",
        width=256,
        height=256,
        null=True,
        blank=True,
    )

    name = models.CharField(
        verbose_name="nome",
        max_length=255,
        null=False,
        blank=False,
        db_index=True,
    )

    barcode = models.CharField(
        verbose_name="código de barra",
        max_length=80,
        null=False,
        blank=False,
        unique=True,
        db_index=True,
    )

    keywords = models.ManyToManyField(
        ProductKeyword,
        verbose_name="palavras-chave",
        blank=True,
    )

    is_active = models.BooleanField(
        verbose_name="está ativo",
        default=False,
    )

    class Meta:
        managed = True
        verbose_name = "produto"
        verbose_name_plural = "produtos"

    def __str__(self):
        return f"{self.name} #{self.barcode}"


models.signals.pre_delete.connect(
    receiver=core_utils.DeleteCustomImageField("photo"), sender=Product
)


class CustomGeojsonMap(models.JSONField):
    def formfield(self, **kwargs):
        kwargs["widget"] = widgets.GeojsonMapWidget()
        return super().formfield(**kwargs)


def _load_default_map():
    path = os.path.join(os.path.dirname(__file__), "defaults", "map.json")
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return {}


class Establishment(models.Model):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        verbose_name="ID",
    )

    address = models.TextField(
        verbose_name="Endereço",
        max_length=256,
        blank=False,
        null=False,
    )

    map = CustomGeojsonMap(
        verbose_name="Mapa",
        blank=False,
        null=False,
        default=_load_default_map,
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

    is_active = models.BooleanField(
        verbose_name="está ativo",
        default=True,
    )

    class Meta:
        managed = True
        verbose_name = "loja"
        verbose_name_plural = "lojas"

    def __str__(self):
        return f"{self.name} ({self.id})"


class EstablishmentPermission(models.Model):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        verbose_name="ID",
    )

    establishment = models.ForeignKey(
        Establishment,
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
        unique=True,
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
                fields=["establishment", "codename"],
                name="unique_establishment_permission",
            )
        ]
        verbose_name = "lojas → permissão"
        verbose_name_plural = "lojas → permissões"

    def __str__(self):
        return f"{self.establishment.name} — {self.codename}"


class EstablishmentGroup(models.Model):
    establishment = models.ForeignKey(
        Establishment,
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
        EstablishmentPermission,
        verbose_name="permissões",
        help_text="Permissões específicas para o grupo.",
        blank=True,
    )

    class Meta:
        managed = True
        constraints = [
            models.UniqueConstraint(
                fields=["establishment", "name"], name="unique_establishment_group"
            )
        ]
        verbose_name = "lojas → grupo"
        verbose_name_plural = "lojas → grupos"

    def __str__(self):
        return f"{self.establishment.name} — {self.name}"


class EstablishmentEmployee(models.Model):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        verbose_name="ID",
    )

    establishment = models.ForeignKey(
        Establishment,
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
        EstablishmentPermission,
        verbose_name="permissões da loja",
        help_text="Permissões específicas para o funcionário.",
        blank=True,
        db_index=True,
    )

    groups = models.ManyToManyField(
        EstablishmentGroup,
        verbose_name="grupos da loja",
        help_text="Grupos que o funcionário faz parte.",
        blank=True,
        db_index=True,
    )

    class Meta:
        managed = True
        constraints = [
            models.UniqueConstraint(
                fields=["establishment", "user"], name="unique_employee"
            )
        ]
        verbose_name = "funcionário"
        verbose_name_plural = "funcionários"

    class EstablishmentPermissions:
        default = "CRUD"

    def __str__(self):
        return f"{self.establishment.name} — {self.user.first_name}"

    def _get_cache_key(self) -> str:
        return f"business:employee_{self.pk}_{self.establishment.id}:permissions"

    def has_permission(self, codename: str, use_cache=True):
        return codename in self.get_all_permissions(use_cache=use_cache)

    def get_all_permissions(self, use_cache=True) -> list:
        key = self._get_cache_key()
        cached = cache.get(key)
        if use_cache and cached is not None:
            return cached

        employee_perms = self.permissions.values("codename", "name").all()
        employee_groups = (
            self.groups.values("permissions__codename", "permissions__name")
            .annotate(
                codename=models.F("permissions__codename"),
                name=models.F("permissions__name"),
            )
            .values("name", "codename")
            .all()
        )

        permissions = list(employee_perms) + list(employee_groups)
        unique = [
            dict(item) for item in {frozenset(perm.items()) for perm in permissions}
        ]

        cache.set(key, tuple(unique), 10 * 60)  # 10 minutes
        return unique

    def has_perm(self, codename, use_cache=True):
        if self.is_admin:
            return True

        permissions = self.get_all_permissions(use_cache=use_cache)

        return any(item["codename"] == codename for item in permissions)

    def has_any_perms(self, codenames: list, use_cache=True) -> bool:
        if self.is_admin:
            return True

        permissions = self.get_all_permissions()
        return any(item in permissions for item in codenames)

    def delete_perm_cache(self):
        cache.delete(self._get_cache_key())


def _load_default_gondola():
    path = os.path.join(os.path.dirname(__file__), "defaults", "gondola.json")
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return {}


class EstablishmentGondola(models.Model):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        verbose_name="ID",
    )

    establishment = models.ForeignKey(
        Establishment,
        on_delete=models.CASCADE,
        verbose_name="loja",
        null=False,
        blank=False,
        db_index=True,
    )

    name = models.CharField(
        verbose_name="nome",
        max_length=255,
        null=False,
        blank=False,
        db_index=True,
    )

    coordinates = models.JSONField(
        name="coordenadas",
        null=False,
        blank=False,
        validators=[validators.CoordinateListValidator(required_length=4)],
        default=_load_default_gondola,
        help_text="Coordenadas do objeto no mapa (polígono)",
    )

    latitude = models.FloatField(
        verbose_name="latitude",
        null=False,
        blank=False,
        validators=[validators.PositiveNumberValidator()],
        help_text="Latitude de referência para busca de produtos no mapa",
    )

    longitude = models.FloatField(
        verbose_name="longitude",
        null=False,
        blank=False,
        validators=[validators.PositiveNumberValidator()],
        help_text="Longitude de referência para busca de produtos no mapa",
    )

    class Meta:
        managed = True
        constraints = [
            models.UniqueConstraint(
                fields=["establishment", "name"],
                name="unique_establishment_gondola",
            )
        ]
        verbose_name = "gôndola"
        verbose_name_plural = "gôndolas"

    def __str__(self):
        return f"{self.establishment} - {self.name}"


class GondolaProduct(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        verbose_name="UUID",
        default=uuid.uuid1,
    )

    gondola = models.ForeignKey(
        EstablishmentGondola,
        on_delete=models.CASCADE,
        verbose_name="gondola",
        null=False,
        blank=False,
        db_index=True,
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="produto",
        null=False,
        blank=False,
        default=uuid.uuid4,
    )

    gondola_x_position = models.IntegerField(
        verbose_name="posição na gondola - eixo X",
        null=False,
        blank=False,
        validators=[validators.PositiveNumberValidator()],
    )

    gondola_y_position = models.IntegerField(
        verbose_name="posição na gondola - eixo Y",
        null=False,
        blank=False,
        validators=[validators.PositiveNumberValidator()],
    )

    class Meta:
        managed = True
        constraints = [
            models.UniqueConstraint(
                fields=["gondola", "gondola_x_position", "gondola_y_position"],
                name="unique_gondola_product_position",
            )
        ]
        verbose_name = "gôndola → produto"
        verbose_name_plural = "gôndolas → produtos"

    class EstablishmentPermissions:
        default = "CRUD"

    def __str__(self):
        return f"{self.gondola.name}. X: {self.gondola_x_position} - Y: {self.gondola_y_position}]"

    def generate_uuid(self):
        raw = f"{self.gondola.pk}-{uuid.uuid1()}"
        hashed = hashlib.sha256(raw.encode()).hexdigest()
        return uuid.UUID(hashed)
