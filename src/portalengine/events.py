import functools
from typing import Callable
from . import pygame

EventType = int
PyGameEvent = pygame.event.Event
EventHandler = Callable[[PyGameEvent], None]
EventHandlerId = int

class EventHandlingDelegator:
	def __init__(self) -> None:
		self.handlers: dict[EventType, dict[EventHandlerId, EventHandler]] = {}
		self.last_id = 0

	def on(self, event_type: EventType):
		"""
		Decorator version of EventHandler.register. Example usage:
		```
		@event_handler.on(pg.KEYDOWN)
		def handle(event: PyGameEvent):
			...
		```

		In the above example, referencing `handle` will not return a function object, rather,
		`handle` will contain the ID of the handler so that it can be deregistered like so:

		```
		event_handler.remove(handle)
		```
		"""
		return functools.partial(self.register, event_type)
	
	def register(self, event_type: EventType, callback: EventHandler) -> EventHandlerId:
		if event_type not in self.handlers: self.handlers[event_type] = {}

		self.handlers[event_type][self.last_id] = callback

		self.last_id+=1

		return self.last_id-1

	def remove(self, handler_id: EventHandlerId, event_type_hint: EventType=None) -> None:
		if event_type_hint:
			if handler_id in self.handlers.get(event_type_hint, {}):
				del handler_container[handler_id]
				return
			
			raise ValueError(f"Handler with ID {handler_id} could not be found for specified event type")
		
		for handler_container in self.handlers.values():
			if handler_id in handler_container:
				del handler_container[handler_id]
				return
			
		raise ValueError(f"Handler with ID {handler_id} could not be found for any event type")

	def send(self, event: PyGameEvent):
		for handler in self.handlers.get(event.type, {}).values():
			handler(event)


	def handle_pg_events(self):
		for event in pygame.event.get():
			self.send(event)
