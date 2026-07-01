# -*- coding: utf-8 -*-
"""
Flame Components — fire behavior calculations for surface and crown fires.

Public API is implemented in :mod:`flame_components.core`; this module
re-exports it.
"""

from flame_components.core import (
    get_mid_flame_ws,
    get_flame_length,
    get_flame_height,
    get_flame_tilt,
    get_flame_residence_time,
    get_flame_depth,
    flame_component_array_multiprocessing,
    # Deprecated camelCase aliases — kept importable for backward compatibility
    getMidFlameWS,
    getFlameLength,
    getFlameHeight,
    getFlameTilt,
    getFlameResidenceTime,
    getFlameDepth,
    flameComponent_ArrayMultiprocessing,
)

__all__ = [
    'get_mid_flame_ws',
    'get_flame_length',
    'get_flame_height',
    'get_flame_tilt',
    'get_flame_residence_time',
    'get_flame_depth',
    'flame_component_array_multiprocessing',
]
