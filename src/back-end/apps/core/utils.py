import os, logging
from uuid import uuid1
from django.conf import settings
from django.db import models
from django.forms import ImageField
from django.utils.deconstruct import deconstructible


@deconstructible
class PathAndRename:
    def __init__(self, subdir):
        self._subdir = subdir

    def __call__(self, instance: models.Model, filename: str):
        extension = filename.split(".")[-1]
        filename = self._create_unique_filename(extension)

        return os.path.join(self._subdir, filename)

    def _create_unique_filename(self, extension: str) -> str:
        while True:
            filename = f"{uuid1().hex}.{extension}"
            path = os.path.join(settings.MEDIA_ROOT, self._subdir, filename)

            if not os.path.isfile(path):
                break

        return filename


@deconstructible
class DeleteCustomImageField:
    def __init__(self, field_name):
        self.field_name = field_name

    def __call__(self, instance: models.Model, *args, **kwargs):
        image_field: ImageField = getattr(instance, self.field_name, {})

        try:
            path = image_field.path
        except ValueError:
            logging.warning(
                f'Could not find path of "{instance.__class__}" primary key "{instance.pk}"'
            )
            return

        if os.path.isfile(path):
            os.remove(path)
