from typing import Any, ItemsView, Iterable, KeysView, List, Union, ValuesView

import Manager
import Object

class GroupManager(Manager.AdamsManager):
    def create(self,
               objects: List[Object.Object] = None,
               object_names: List[str] = None,
               **kwargs) -> Group: ...

    def items(self) -> ItemsView[str, Group]: ...
    def values(self) -> ValuesView[Group]: ...
    def keys(self) -> KeysView[str]: ...
    def __getitem__(self, name) -> Group: ...
    def __iter__(self, *args) -> Iterable[str]: ...


class Group(Object.ObjectComment):
    comment_id: Any

    def append(self,
               objects: Union[List[Object.Object], Object.Object] = None,
               object_names: Union[List[str], str] = None,
               expand_groups: bool = False,
               type_filter: str = None) -> None:
        ...

    def replaceObjects(self,
                       objects: Union[List[Object.Object], Object.Object] = None,
                       object_names: Union[List[str], str] = None,
                       expand_groups: bool = False,
                       type_filter: str = None) -> None:
        ...

    def remove(self,
               objects: Union[List[Object.Object], Object.Object] = None,
               object_names: Union[List[str], str] = None,
               type_filter: str = None) -> None:
        ...

    def empty(self) -> None: ...

    def copyObjects(self, new_group_name: str = None, type_filter: str = None):
        ...
    objects: List[Object.Object]
    object_names: List[str]
