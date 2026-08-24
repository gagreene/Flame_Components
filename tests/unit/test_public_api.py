# tests/unit/test_public_api.py
"""
Verifies flame_components.__all__ is exactly the 7 snake_case public functions --
`from flame_components import *` must not surface private helpers or anything else.
"""
import flame_components


def test_all_contains_only_snake_case_names():
    expected = {
        'get_mid_flame_ws',
        'get_flame_length',
        'get_flame_height',
        'get_flame_tilt',
        'get_flame_residence_time',
        'get_flame_depth',
        'flame_component_array_multiprocessing',
    }
    assert set(flame_components.__all__) == expected
