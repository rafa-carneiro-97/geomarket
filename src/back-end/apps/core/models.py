import re
from django.db import models
from django.db.models.fields.files import ImageFieldFile
from django.core.exceptions import ValidationError
from PIL import Image
from . import widgets, utils


class CustomImageField(models.ImageField):
    _formats = ("WEBP",)

    error_messages = {
        "invalid_height": "A altura da imagem esperada é %(height)spx",
        "invalid_width": "A largura da imagem esperada é  %(width)spx",
        "invalid_format": f"Formato inválido. Formatos suportados: {', '.join(_formats)}",
        "invalid_image": "O arquivo enviado não era uma imagem ou era estava corrompido",
    }

    def __init__(self, subdir: str, width: int, height: int, *args, **kwargs):
        self.width = width
        self.height = height
        self._subdir = subdir
        kwargs["upload_to"] = utils.PathAndRename(subdir)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["subdir"] = self._subdir
        kwargs["width"] = self.width
        kwargs["height"] = self.height
        return name, path, args, kwargs

    def validate(self, value: ImageFieldFile, model_instance: models.Model):
        # Verify image
        try:
            image = Image.open(value)
            image.verify()
        except Exception:
            raise ValidationError(
                self.error_messages["invalid_image"], code="invalid_image"
            )

        # Validate format
        if image.format not in self._formats:
            raise ValidationError(
                self.error_messages["invalid_format"], code="invalid_format"
            )

        # Validate height
        if value.height != self.height:
            raise ValidationError(
                self.error_messages["invalid_height"],
                code="invalid_height",
                params={"height": self.height},
            )

        # Validate width
        if value.width != self.width:
            raise ValidationError(
                self.error_messages["invalid_width"],
                code="invalid_width",
                params={"width": self.width},
            )

        return super().validate(value, model_instance)

    def pre_save(self, model_instance: models.Model, add: bool):
        if add is False:
            old_model = model_instance.__class__.objects.filter(
                pk=model_instance.pk
            ).first()
            old_url = self._get_image_url(old_model)
            current_url = self._get_image_url(model_instance)

            if old_url != current_url:
                self.delete_file(old_model)

        return super().pre_save(model_instance, add)

    def _get_image_url(self, instance: models.Model) -> str:
        try:
            return getattr(instance, self.attname).url
        except ValueError:
            # Empty file
            return ""

    def delete_file(self, instance: models.Model):
        delete_custom = utils.DeleteCustomImageField(self.attname)
        delete_custom(instance)

    def formfield(self, **kwargs):
        kwargs["widget"] = widgets.ImageCropperInputWidget(
            attrs={
                "accept": "image/webp",
                "height": self.height,
                "width": self.width,
            }
        )
        return super().formfield(**kwargs)
