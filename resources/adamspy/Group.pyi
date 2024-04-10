import Manager
import Object
from typing import Any, List, Union


class GroupManager(Manager.AdamsManager):
    def create(self,
               objects: List[Object.Object] = None,
               object_names: List[str] = None,
               **kwargs) -> Group: ...


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
    objects: Any
    object_names: Any
