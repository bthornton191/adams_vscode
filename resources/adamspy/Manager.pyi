import collections
from collections.abc import Generator
from typing import Any
from Part import Part

class DuplicateNameError(AttributeError): ...
class ObjectCreationFailure(Exception): ...
class InvalidNameError(AttributeError): ...

class AdamsManager(collections.Mapping):
    parent: Any
    managedClass: Any
    def __init__(self, managed_class, parent) -> None: ...
    def __getitem__(self, name): ...
    def set(self, name, **properties): ...
    def iterDBKeys(self) -> Generator[Any, None, None]: ...
    def values(self, *args): ...
    def keys(self, *args): ...
    def items(self, *args): ...
    def values_full(self, *args): ...
    def keys_full(self, *args): ...
    def items_full(self, *args): ...
    def iterkeys(self, *args) -> None: ...
    def iteritems(self, *args) -> None: ...
    def itervalues(self, *args) -> None: ...
    def __iter__(self, *args): ...
    def __len__(self, *args): ...
    def __dir__(self, all: bool = ...): ...
    def create(self, **kwargs)->Part: ...

class SubclassManager(AdamsManager):
    def __init__(self, managedClass, parent) -> None: ...
    def set(self, name, cls, **kwargs): ...
