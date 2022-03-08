import Manager
import Object
from typing import Any

class MaterialManager(Manager.AdamsManager): ...

class Material(Object.Object):
    youngs_modulus: Any
    poissons_ratio: Any
    density: Any
    orthotropic_constants: Any
    anisotropic_constants: Any
