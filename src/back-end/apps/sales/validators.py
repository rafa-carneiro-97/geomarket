from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class PositiveNumberValidator:
    """
    Validate that the value is a positive number (greater than zero).
    """

    error_messages = {
        "not_positive": "O valor deve ser um número positivo maior que zero.",
    }

    def __call__(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValidationError(
                self.error_messages["not_positive"],
                code="not_positive",
                params={"value": value},
            )

    def __repr__(self):
        return "<PositiveNumberValidator()>"
