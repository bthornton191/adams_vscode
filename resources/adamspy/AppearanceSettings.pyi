from DBAccess import PropertyValue as PropertyValue
from typing import Any

class AppearanceSettings:
    color_name: str
    color: str
    visibility: str
    """can be `'on'`, `'off'`, or `'inherit'`"""
    def hide(self) -> None: ...
    def show(self) -> None: ...
    size_of_icons: float
    active: str
    """can be `'on'`, `'off'`, or `'inherit'`"""
    name_visibility: str
    """can be `'on'`, `'off'`, or `'inherit'`"""

class GeometryAppearanceSettings(AppearanceSettings):
    transparencyLevel: float
    transparency_level: float
    renderStyle: str
    render_mode: str
