import typing
import collections.abc
import typing_extensions

GenericType1 = typing.TypeVar("GenericType1")
GenericType2 = typing.TypeVar("GenericType2")

class ConsoleLogger:
    """Handler instances dispatch logging events to specific destinations.The base handler class. Acts as a placeholder which defines the Handler
    interface. Handlers can optionally use Formatter instances to format
    records as desired. By default, no formatter is specified; in this case,
    the 'raw' message as determined by record.message is logged.
    """

    name: typing.Any

    def emit(self, record):
        """Do whatever it takes to actually log the specified logging record.This version is intended to be implemented by subclasses and so
        raises a NotImplementedError.

                :param record:
        """
        ...

def setup(log_level): ...
