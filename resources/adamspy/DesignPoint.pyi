import Manager
import Object
from typing import Any

class DesignPointManager(Manager.AdamsManager): ...

class DesignPoint(Object.Object):
    def __init__(self, _DBKey) -> None: ...
    location: Any
    comments: Any
