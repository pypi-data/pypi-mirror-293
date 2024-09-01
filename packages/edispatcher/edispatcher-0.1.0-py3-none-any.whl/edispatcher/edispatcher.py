from typing import Any, Protocol


class Event(Protocol):
    """An event that can be dispatched to its handlers."""

    name: str
    data: dict[str, Any]


class Handler(Protocol):
    """A handler that can process an event."""

    def handle(self, event: Event) -> None:
        """Handle an event.

        Args:
            event (Event): The event to handle.
        """


class Dispatcher(Protocol):
    """A dispatcher that can dispatch an event to its handlers."""

    def dispatch(
        self,
        event: Event,
        handlers: list[Handler],
        **kwargs,
    ) -> Any:
        """Dispatch an event to its handlers.

        Args:
            event (Event): The event to be dispatched.
            handlers (list[Handler]): The list of handlers to process the event.
            **kwargs: Additional keyword arguments that may be passed to the dispatcher.

        Returns:
            Any: The result of the dispatching process, if applicable.
        """


class EventDispatcher:
    """A simple event dispatcher that can register handlers for events and dispatch them."""

    class Error(Exception):
        """Base class for exceptions in EventDispatcher."""

    class HandlerAlreadyRegistered(Error):
        """Raised when a handler is already registered for a specific event."""

    def __init__(self, dispatcher: Dispatcher | None = None) -> None:
        """Initializes an EventDispatcher.

        Args:
            dispatcher (Dispatcher | None, optional): An optional external dispatcher to use.
            If None, the internal dispatch mechanism will be used.
        """
        self._dispatcher = dispatcher
        self._event_handlers: dict[str, list[Handler]] = {}

    def dispatch(self, event: Event, **kwargs: Any) -> Any:
        """Dispatches an event to all registered handlers.

        If an external dispatcher is provided, it will be used to dispatch the event.
        Otherwise, the event will be dispatched using the internal mechanism.

        Args:
            event (Event): The event to be dispatched.
            **kwargs: Additional keyword arguments that may be passed to the dispatcher.

        Returns:
            Any: The result of the dispatching process, if applicable.
        """
        handlers = self._event_handlers.get(event.name, [])

        if self._dispatcher is None:
            for handler in handlers:
                handler.handle(event)
        else:
            return self._dispatcher.dispatch(
                event=event,
                handlers=handlers,
                **kwargs,
            )

    def register(self, event_name: str, handler: Handler) -> None:
        """Registers a handler for a specific event.

        Args:
            event_name (str): The name of the event.
            handler (Handler): The handler to be registered.

        Raises:
            HandlerAlreadyRegistered: If the handler is already registered for the event.
        """
        handlers = self._event_handlers.get(event_name, [])
        self._raise_error_if_handler_already_registered(handler, handlers)
        handlers.append(handler)
        self._event_handlers[event_name] = handlers

    def _raise_error_if_handler_already_registered(
        self,
        handler: Handler,
        handlers: list[Handler],
    ) -> None:
        """Checks if a handler is already registered and raises an error if it is.

        Args:
            handler (Handler): The handler to be checked.
            handlers (list[Handler]): The list of already registered handlers.

        Raises:
            HandlerAlreadyRegistered: If the handler is already registered.
        """
        if handler.__class__.__name__ in [
            h.__class__.__name__ for h in handlers
        ]:
            raise self.HandlerAlreadyRegistered(
                f"Handler {handler.__class__.__name__} already registered!"
            )
