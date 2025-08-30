from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import Q
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from . import models


DEFAULT_PERMISSIONS_MAP = {
    "C": ("add", "Pode adicionar"),
    "R": ("view", "Pode visualizar"),
    "U": ("change", "Pode alterar"),
    "D": ("delete", "Pode excluir"),
}


def _is_valid_default(value) -> bool:
    letters = [key for key in DEFAULT_PERMISSIONS_MAP]
    return set(value).issubset(letters)


def _is_valid_custom(value) -> bool:
    if not isinstance(value, list):
        return False

    for item in value:
        if not isinstance(item, tuple) or len(item) != 2:
            return False
        if not all(isinstance(elem, str) for elem in item):
            return False

    return True


def _get_models_perms(content_type: ContentType) -> list:
    model = content_type.model_class()
    establishment_permissions = getattr(model, "EstablishmentPermissions", None)
    default = getattr(establishment_permissions, "default", [])
    custom = getattr(establishment_permissions, "custom", [])

    if default and not _is_valid_default(default):
        raise TypeError(
            f'The only allowed values for "permissions" in Model {model.__name__}.EstablishmentPermissions  are "CRUD"'
        )

    if custom and not _is_valid_custom(custom):
        raise TypeError(
            f'Expected a list of (str, str) tuples for "custom" in Model {model.__name__}.EstablishmentPermissions'
        )

    permissions = []
    for letter in default:
        if letter in DEFAULT_PERMISSIONS_MAP:
            codename_prefix, name_prefix = DEFAULT_PERMISSIONS_MAP[letter]
            codename = f"{codename_prefix}_{model.__name__}".lower()
            name = f"{name_prefix} {model._meta.verbose_name_plural}"
            permissions.append((codename, name))

    for codename, name in custom:
        permissions.append((codename, name))

    return permissions


@receiver(post_save, sender=models.Establishment)
def create_establishment_permissions(
    sender, instance: models.Establishment, created, **kwargs
):
    if not created:
        return

    to_create = []
    content_types = ContentType.objects.all()
    for content in content_types:
        permissions = _get_models_perms(content)
        for codename, name in permissions:
            to_create.append(
                models.EstablishmentPermission(
                    establishment=instance,
                    content_type=content,
                    codename=codename,
                    name=name,
                )
            )
    if to_create:
        with transaction.atomic():
            models.EstablishmentPermission.objects.bulk_create(
                to_create, ignore_conflicts=False
            )


@receiver(post_migrate, sender=apps.get_app_config("business"))
def update_establishment_permissions(sender, **kwargs):
    """
    Update EstablishmentPermissions for all models with establishment_permissions in Meta
    """
    establishments = models.Establishment.objects.order_by("id").all()
    content_types = ContentType.objects.all()

    for content in content_types:
        permissions = _get_models_perms(content)

        if not permissions:
            continue

        existing_permissions = models.EstablishmentPermission.objects.filter(
            content_type=content
        ).values_list("establishment__id", "codename")
        q_objects = Q()
        to_create = []

        for item in establishments:
            for codename, name in permissions:
                q_objects |= Q(
                    codename=codename,
                    name=name,
                    establishment=item,
                    content_type=content,
                )

                if (item.id, codename) not in existing_permissions:
                    to_create.append(
                        models.EstablishmentPermission(
                            establishment=item,
                            content_type=content,
                            codename=codename,
                            name=name,
                        )
                    )
        if to_create:
            with transaction.atomic():
                models.EstablishmentPermission.objects.bulk_create(
                    to_create, ignore_conflicts=False
                )

        # Remove unset permissions
        models.EstablishmentPermission.objects.exclude(q_objects).delete()
