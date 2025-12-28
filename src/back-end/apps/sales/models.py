import json, os
from django.db import models
from django.contrib.auth.hashers import check_password, identify_hasher, make_password
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone
from apps.core import models as core_models
from apps.business import models as business_models
from . import validators, widgets


class CustomMapField(models.JSONField):
    def formfield(self, **kwargs):
        kwargs["widget"] = widgets.GeojsonMapWidget()
        return super().formfield(**kwargs)


def _load_default_map():
    path = os.path.join(os.path.dirname(__file__), "defaults", "map.json")
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return {}


class SalesMap(models.Model):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        verbose_name="ID",
    )

    establishment = models.OneToOneField(
        business_models.Establishment,
        on_delete=models.CASCADE,
        verbose_name="loja",
        null=False,
        blank=False,
        db_index=True,
    )

    map = CustomMapField(
        verbose_name="Mapa",
        blank=False,
        null=False,
        default=_load_default_map,
    )

    def __str__(self):
        return f"Mapa - {self.establishment.name} #{self.establishment.id}"

    class Meta:
        managed = True
        verbose_name = "mapa"
        verbose_name_plural = "mapas"


def _load_default_gondola():
    path = os.path.join(os.path.dirname(__file__), "defaults", "gondola.json")
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return {}


class Gondola(models.Model):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        verbose_name="ID",
    )

    establishment = models.ForeignKey(
        business_models.Establishment,
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
        help_text="Latitude de referência para a busca de produtos no salão",
    )

    longitude = models.FloatField(
        verbose_name="longitude",
        null=False,
        blank=False,
        validators=[validators.PositiveNumberValidator()],
        help_text="Longitude de referência para a busca de produtos no salão",
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
        default=core_models.UniqueUUIDGenerator("sales", "GondolaProduct", "id"),
    )

    gondola = models.ForeignKey(
        Gondola,
        on_delete=models.CASCADE,
        verbose_name="gondola",
        null=False,
        blank=False,
        db_index=True,
    )

    product = models.ForeignKey(
        business_models.Product,
        on_delete=models.CASCADE,
        verbose_name="produto",
        null=False,
        blank=False,
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


class InformationEmissor(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        verbose_name="UUID",
        default=core_models.UniqueUUIDGenerator("sales", "InformationEmissor", "id"),
    )

    establishment = models.ForeignKey(
        business_models.Establishment,
        verbose_name="loja",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        db_index=True,
    )

    key = models.CharField(
        verbose_name="chave de acesso",
        max_length=16,
        null=False,
        blank=False,
    )

    auth = models.CharField(
        "autenticação",
        max_length=128,
        null=False,
        blank=False,
    )

    name = models.CharField(
        verbose_name="nome",
        max_length=255,
        null=False,
        blank=False,
        help_text="Identificador do emissor",
    )

    class Meta:
        managed = True
        verbose_name = "emissor de informação"
        verbose_name_plural = "emissores de informação"

    def __str__(self):
        return f"{self.establishment.name} - Emissor {self.name}"

    @property
    def is_active(self) -> bool:
        key = self.get_status_cache_key()
        status = cache.get(key)
        return status is not None

    def save(self, *args, **kwargs):
        if self.auth and not self._is_auth_hashed():
            self.auth = make_password(self.auth)
        super().save(*args, **kwargs)

    def check_auth(self, raw_auth: str) -> bool:
        return check_password(raw_auth, self.auth)

    def _is_auth_hashed(self) -> bool:
        try:
            identify_hasher(self.auth)
            return True
        except (ValueError, ImproperlyConfigured):
            return False

    def get_status_cache_key(self) -> str:
        return f"sales:information_emissor:{self.pk}"

    def update_status(self, timeout: int = 60):
        key = self.get_status_cache_key()
        cache.set(key, timezone.now(), timeout=timeout)


class CartLocator(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        verbose_name="UUID",
        default=core_models.UniqueUUIDGenerator("sales", "CartLocator", "id"),
    )

    name = models.CharField(
        verbose_name="nome",
        max_length=255,
        null=False,
        blank=False,
    )

    information_emissor = models.ForeignKey(
        InformationEmissor,
        verbose_name="emissor de informação",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        db_index=True,
    )

    class Meta:
        managed = True
        verbose_name = "Localizador de carrinho"
        verbose_name_plural = "Localizadores de carrinho"

    def __str__(self):
        return f"Localizador #{self.pk}"

    def get_location_cache_key(self) -> str:
        return f"sales:cart_location:{self.pk}"

    def get_location(self) -> dict | None:
        key = self.get_location_cache_key()
        return cache.get(key)

    def set_location(self, latitude: float, longitude: float, timeout: int = 120):
        key = self.get_location_cache_key()
        location = {
            "latitude": latitude,
            "longitude": longitude,
        }
        cache.set(key, location, timeout=timeout)

    def websocket_group_name(self) -> str:
        return f"cartlocator_{self.pk}"
