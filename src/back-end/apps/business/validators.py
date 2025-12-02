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


@deconstructible
class CoordinateListValidator:
    """
    Validate that the value is a list of [x, y] coordinate pairs.
    Optionally enforces a fixed length (e.g., 4 points).
    """

    error_messages = {
        "not_list": "O valor deve ser uma lista de coordenadas.",
        "wrong_length": "A lista deve conter exatamente %(required_length)d pares de coordenadas.",
        "invalid_pair": "Cada item deve ser uma lista de dois números, por exemplo [x, y].",
        "not_numeric": "As coordenadas devem conter apenas valores numéricos.",
    }

    def __init__(self, required_length=None):
        self.required_length = required_length

    def __call__(self, value):
        if not isinstance(value, list):
            raise ValidationError(
                self.error_messages["not_list"],
                code="not_list",
                params={"value": value},
            )

        if self.required_length is not None and len(value) != self.required_length:
            raise ValidationError(
                self.error_messages["wrong_length"],
                code="wrong_length",
                params={"required_length": self.required_length, "value": value},
            )

        for item in value:
            if not (isinstance(item, list) and len(item) == 2):
                raise ValidationError(
                    self.error_messages["invalid_pair"],
                    code="invalid_pair",
                    params={"value": item},
                )

            x, y = item
            if not (isinstance(x, (int, float)) and isinstance(y, (int, float))):
                raise ValidationError(
                    self.error_messages["not_numeric"],
                    code="not_numeric",
                    params={"value": item},
                )

    def __repr__(self):
        return f"<CoordinateListValidator(required_length={self.required_length})>"
