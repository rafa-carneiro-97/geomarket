import logging
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import Q, QuerySet
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from . import models


@receiver(post_save, sender=models.Establishment)
def create_establishment_permissions(
    sender, instance: models.Establishment, created, **kwargs
):
    if not created:
        return

    EstablishmentPermissionsUpdater().create(instance)


@receiver(post_migrate, sender=apps.get_app_config("business"))
def update_establishment_permissions(sender, **kwargs):
    EstablishmentPermissionsUpdater().update()


class EstablishmentPermissionsUpdater:
    DEFAULT_PERMISSIONS_MAP = {
        "C": ("add", "Pode adicionar"),
        "R": ("view", "Pode visualizar"),
        "U": ("change", "Pode alterar"),
        "D": ("delete", "Pode excluir"),
    }
    permissions = []

    def __init__(self) -> list:
        contents = ContentType.objects.all()
        for content in contents:
            model = content.model_class()

            establishment_permissions = getattr(model, "EstablishmentPermissions", None)
            default = getattr(establishment_permissions, "default", [])
            custom = getattr(establishment_permissions, "custom", [])

            if default and not self._is_valid_default(default):
                raise TypeError(
                    f'The only allowed values for "permissions" in Model {model.__name__}.EstablishmentPermissions  are "CRUD"'
                )

            if custom and not self._is_valid_custom(custom):
                raise TypeError(
                    f'Expected a list of (str, str) tuples for "custom" in Model {model.__name__}.EstablishmentPermissions'
                )

            for letter in default:
                if letter in self.DEFAULT_PERMISSIONS_MAP:
                    codename_prefix, name_prefix = self.DEFAULT_PERMISSIONS_MAP[letter]
                    codename = f"{codename_prefix}_{model.__name__}".lower()
                    name = f"{name_prefix} {model._meta.verbose_name_plural}"
                    self.permissions.append(
                        {"codename": codename, "name": name, "content": content}
                    )

            for codename, name in custom:
                self.permissions.append(
                    {"codename": codename, "name": name, "content": content}
                )

        self._check_repeated()

    def _is_valid_default(self, value) -> bool:
        letters = [key for key in self.DEFAULT_PERMISSIONS_MAP]
        return set(value).issubset(letters)

    def _is_valid_custom(self, value) -> bool:
        if not isinstance(value, list):
            return False

        for item in value:
            if not isinstance(item, tuple) or len(item) != 2:
                return False
            if not all(isinstance(elem, str) for elem in item):
                return False

        return True

    def _check_repeated(self):
        seen_codename = set()
        seen_name = set()

        for item in self.permissions:
            codename = item["codename"]
            name = item["name"]

            if codename in seen_codename:
                raise ValueError(f"Reapeated permission codename: { codename }")

            if name in seen_name:
                raise ValueError(f"Reapeated permission name: { name }")

            seen_codename.add(codename)
            seen_name.add(name)

    def create(self, instance: models.Establishment):
        to_create = []
        for item in self.permissions:
            to_create.append(
                models.EstablishmentPermission(
                    establishment=instance,
                    content_type=item["content"],
                    codename=item["codename"],
                    name=item["name"],
                )
            )

        if not to_create:
            return

        with transaction.atomic():
            models.EstablishmentPermission.objects.bulk_create(
                to_create, ignore_conflicts=False
            )

    def _to_create(self, establishment: models.Establishment) -> list:
        to_create = []

        perms_keys = set(
            models.EstablishmentPermission.objects.filter(
                establishment=establishment
            ).values_list("codename", "content_type__id")
        )

        for item in self.permissions:
            key = (item["codename"], item["content"].id)

            if key not in perms_keys:
                logging.info(
                    f'Preparing to create the establishment permission  "{item["codename"]}" of {establishment.name} #{establishment.id}.'
                )

                perm = models.EstablishmentPermission(
                    establishment=establishment,
                    content_type=item["content"],
                    codename=item["codename"],
                    name=item["name"],
                )

                to_create.append(perm)

        return to_create

    def _to_delete_queryset(self) -> QuerySet:
        q_objects = Q()
        for item in self.permissions:
            q_objects |= Q(
                codename=item["codename"],
                name=item["name"],
                content_type=item["content"],
            )

        to_delete = models.EstablishmentPermission.objects.exclude(q_objects)

        for item in to_delete:
            logging.info(
                f'Preparing to delete the establishment permission  "{item.codename}" of {item.establishment.name} #{item.establishment.id}.'
            )

        return to_delete

    def update(self):
        all_establishments = models.Establishment.objects.all()
        to_create = []

        for establishment in all_establishments:
            to_create += self._to_create(establishment)

        with transaction.atomic():
            if to_create:
                models.EstablishmentPermission.objects.bulk_create(
                    to_create, ignore_conflicts=False
                )

                logging.info(f"Created {to_create.count()} establishment permissions")

            to_delete = self._to_delete_queryset()
            if to_delete:
                logging.info(f"Removed {to_delete.count()} establishment permissions")
                to_delete.delete()
