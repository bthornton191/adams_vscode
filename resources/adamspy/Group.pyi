import Manager
import Object
from typing import Any

class GroupManager(Manager.AdamsManager): ...

class Group(Object.ObjectComment):
    comment_id: Any
    def append(self, objects: Any | None = ..., object_names: Any | None = ..., expand_groups: bool = ..., type_filter: Any | None = ...) -> None: ...
    def replaceObjects(self, objects: Any | None = ..., object_names: Any | None = ..., expand_groups: bool = ..., type_filter: Any | None = ...) -> None: ...
    def remove(self, objects: Any | None = ..., object_names: Any | None = ..., type_filter: Any | None = ...) -> None: ...
    def empty(self) -> None: ...
    def copyObjects(self, new_group_name: Any | None = ..., type_filter: Any | None = ...): ...
    objects: Any
    object_names: Any
