from .ProducerTest import source as ModuleEventSource

# Define symbols to be exported when the package is imported
# Only needs to produce events for now, will deal with input later
__all__ = ["ModuleEventSource"]
