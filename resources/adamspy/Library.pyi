import Manager
import Object
from typing import Any

class LibraryManager(Manager.AdamsManager): ...

class Library(Object.ObjectBase):
    Libraries: Any
    Materials: Any
    UserDefinedElements: Any
    def __init__(self, _DBKey) -> None: ...

class AttributesLibraryManager(Manager.AdamsManager): ...

class Attributes_Library(Object.ObjectBase):
    Colors: Any
    def __init__(self, _DBKey) -> None: ...
