import logging, uuid
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import DenyConnection
from django.core.cache import cache
from . import models


class InformationEmissorConsumer(WebsocketConsumer):
    def dispatch(self, message):
        self.emissor_id = self.scope["url_route"]["kwargs"]["id"]
        return super().dispatch(message)

    def emissor_queryset(self) -> models.InformationEmissor | None:
        return models.InformationEmissor.objects.filter(id=self.emissor_id).first()

    def connect(self):
        logging.info(
            f'Emissor websocket connection attempt with id "{self.emissor_id}".'
        )
        self.emissor = self.emissor_queryset()

        if not self.emissor:
            logging.warning(
                f'Error on websocket connection attempt: Emissor with id "{self.emissor_id}" not found.'
            )
            raise DenyConnection("Emissor not found")

        self.accept()

    def disconnect(self, code):
        if self.emissor:
            logging.info(
                f'Emissor websocket "{self.emissor_id}" disconnected with code "{code}". Channel name "{self.channel_name}".'
            )

    def receive(self, text_data=None, bytes_data=None):
        data = self._prepare_text_data(text_data or "")

        if not data:
            return

        locator = self.locator_queryset(data["locator_id"])

        if not locator:
            logging.warning(
                f'Cart locator "{data["locator_id"]}" not found for Emissor "{self.emissor_id}".'
            )
            return

        group_name = locator.websocket_group_name()
        sync_group_send = async_to_sync(self.channel_layer.group_send)

        sync_group_send(
            group_name,
            {
                "type": "update_location",
                "latitude": data["latitude"],
                "longitude": data["longitude"],
            },
        )

    def locator_queryset(self, locator_id) -> models.CartLocator | None:
        key = f"information_emissor_consummer:locator:{locator_id}:emissor:{self.emissor_id}"
        cached_locator = cache.get(key, None)

        if cached_locator:
            return cached_locator

        locator = models.CartLocator.objects.filter(
            id=locator_id, information_emissor=self.emissor
        ).first()

        if not locator:
            logging.warning(
                f'Locator with id "{locator_id}" not found for Emissor "{self.emissor_id}".'
            )
            return None

        cache.set(key, locator, timeout=300)
        return locator

    def _prepare_text_data(self, text_data: str) -> dict | None:
        data = text_data.split(",")
        if len(data) != 3:
            logging.warning(
                f'Invalid message format received on Emissor "{self.emissor_id}". Received data: "{text_data}".'
            )
            return None

        try:
            identifier = uuid.UUID(data[0])
            latitude = float(data[1])
            longitude = float(data[2])
        except ValueError:
            logging.warning(
                f'Invalid values received on Emissor "{self.emissor_id}". Received data: "{text_data}".'
            )
            return None

        return {
            "locator_id": str(identifier),
            "latitude": latitude,
            "longitude": longitude,
        }


class CartLocatorConsumer(WebsocketConsumer):
    def dispatch(self, message):
        self.locator_id = self.scope["url_route"]["kwargs"]["id"]
        return super().dispatch(message)

    def connect(self):
        logging.info(
            f'CartLocator websocket connection attempt with channel name "{self.channel_name}" and cart locator id "{self.locator_id}".'
        )
        self.locator = self.locator_queryset()

        if not self.locator:
            logging.warning(
                f'Error on websocket connection attempt: CartLocator with id "{self.locator_id}" not found.'
            )
            raise DenyConnection("CartLocator not found")

        group_name = self.locator.websocket_group_name()
        sync_group_add = async_to_sync(self.channel_layer.group_add)
        sync_group_add(group_name, self.channel_name)
        logging.info(
            f'CartLocator added to group "{group_name}" [{self.channel_name}]"'
        )

        self.accept()

    def locator_queryset(self) -> models.CartLocator | None:
        key = f"cart_locator_consummer:locator:{self.locator_id}"
        cached_locator = cache.get(key, None)

        if cached_locator:
            return cached_locator

        locator = models.CartLocator.objects.filter(id=self.locator_id).first()

        if not locator:
            logging.warning(f'Locator with id "{self.locator_id}" not found.')
            return None

        cache.set(key, locator, timeout=300)
        return locator

    def disconnect(self, code):
        logging.info(
            f'CartLocator "{self.locator_id}" disconnected with code "{code}". Channel name "{self.channel_name}".'
        )

        if not self.locator:
            return

        group_name = self.locator.websocket_group_name()
        sync_group_discard = async_to_sync(self.channel_layer.group_discard)
        sync_group_discard(group_name, self.channel_name)

    def update_location(self, event):
        latitude = event["latitude"]
        longitude = event["longitude"]
        self.send(text_data=f"{latitude},{longitude}")
