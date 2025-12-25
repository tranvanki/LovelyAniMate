from typing import Dict, Optional, Tuple
import asyncio
from loguru import logger
from collections import defaultdict


class MessageHandler:
    """
    Manages asynchronous message handling with request-response correlation.
    Enables async tasks to wait for specific responses from WebSocket clients by type and ID.
    """

    def __init__(self):
        # Dictionary mapping client UID -> (response_type, request_id) -> asyncio.Event
        self._response_events: Dict[
            str, Dict[Tuple[str, Optional[str]], asyncio.Event]
        ] = defaultdict(dict)
        # Dictionary mapping client UID -> (response_type, request_id) -> response_data
        self._response_data: Dict[str, Dict[Tuple[str, Optional[str]], dict]] = (
            defaultdict(dict)
        )

    async def wait_for_response(
        self,
        client_uid: str,
        response_type: str,
        request_id: str | None = None,
        timeout: float | None = None,
    ) -> Optional[dict]:
        """
        Asynchronously wait for a specific response from a client.
        Blocks until the response arrives or timeout occurs.

        Args:
            client_uid: Unique identifier of the client to wait for
            response_type: Type of response message expected
            request_id: Optional ID to match specific requests with responses
            timeout: Maximum seconds to wait (None for indefinite)

        Returns:
            Response data dictionary if received before timeout, None otherwise
        """
        event = asyncio.Event()
        response_key = (response_type, request_id)
        self._response_events[client_uid][response_key] = event

        try:
            if timeout is not None:
                # Wait with timeout - raises asyncio.TimeoutError if exceeded
                await asyncio.wait_for(event.wait(), timeout)
            else:
                # Wait indefinitely for the response
                await event.wait()

            return self._response_data[client_uid].pop(response_key, None)
        except asyncio.TimeoutError:
            logger.warning(
                f"Timeout waiting for {response_type} (ID: {request_id}) from {client_uid}"
            )
            return None
        finally:
            # Clean up the event even if timeout occurred
            self._response_events[client_uid].pop(response_key, None)

    def handle_message(self, client_uid: str, message: dict) -> None:
        """
        Process incoming message and trigger any waiting response handlers.
        Matches messages to pending requests using type and request_id.

        Args:
            client_uid: Identifier of the client sending the message
            message: Message dictionary with 'type' and optional 'request_id' keys
        """
        # Extract message routing information
        msg_type = message.get("type")
        request_id = message.get("request_id")
        if not msg_type:
            return

        response_key = (msg_type, request_id)

        # Trigger the waiting event if one exists for this message type/ID
        if (
            client_uid in self._response_events
            and response_key in self._response_events[client_uid]
        ):
            self._response_data[client_uid][response_key] = message
            self._response_events[client_uid][response_key].set()

    def cleanup_client(self, client_uid: str) -> None:
        """
        Release all pending resources for a disconnected client.
        Signals all waiting tasks to unblock and removes stored event data.

        Args:
            client_uid: Identifier of the client to clean up
        """
        if client_uid in self._response_events:
            # Unblock all waiting async tasks for this client
            for event in self._response_events[client_uid].values():
                event.set()
            # Remove all stored events and responses
            self._response_events.pop(client_uid)
            self._response_data.pop(client_uid, None)


message_handler = MessageHandler()
