import Manager
import Object
from typing import Any

class FeatureManager(Manager.SubclassManager):
    def createThinShell(self, **kwargs): ...
    def createHole(self, **kwargs): ...
    def createBlend(self, **kwargs): ...

class Feature(Object.Object): ...

class FeatureThinShell(Feature):
    subids: Any
    thickness: Any
    locations: Any

class FeatureHole(Feature):
    subid: Any
    center: Any
    countersink: Any
    radius: Any
    depth: Any

class FeatureBlend(Feature):
    subtype: Any
    subids: Any
    locations: Any
    chamfer: Any
    radius1: Any
    radius2: Any
    reference_marker: Any
