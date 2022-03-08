from DBAccess import PropertyValue as PropertyValue
from typing import Any

class AppearanceSettings:
    color_name: Any
    color: Any
    visibility: Any
    def hide(self) -> None: ...
    def show(self) -> None: ...
    size_of_icons: Any
    active: Any
    name_visibility: Any

class GeometryAppearanceSettings(AppearanceSettings):
    transparencyLevel: Any
    transparency_level: Any
    renderStyle: Any
    render_mode: Any
