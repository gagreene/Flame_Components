# tests/unit/test_deprecated_aliases.py
"""
Unit tests for the camelCase backward-compatibility aliases (deprecated since 0.1.0).
Each alias must remain importable, emit DeprecationWarning, and return results
identical to its snake_case counterpart -- but must not be part of the public
`__all__` surface.
"""
import numpy as np
import pytest
import flame_components
from flame_components import (
    get_mid_flame_ws,
    get_flame_length,
    get_flame_height,
    get_flame_tilt,
    get_flame_residence_time,
    get_flame_depth,
    flame_component_array_multiprocessing,
    getMidFlameWS,
    getFlameLength,
    getFlameHeight,
    getFlameTilt,
    getFlameResidenceTime,
    getFlameDepth,
    flameComponent_ArrayMultiprocessing,
)


class TestDeprecatedAliasesWarnAndMatch:
    def test_get_mid_flame_ws_alias(self):
        with pytest.warns(DeprecationWarning, match="Use .* instead"):
            alias_result = getMidFlameWS(
                wind_speed=20.0, canopy_cover=50, canopy_ht=20.0,
                canopy_baseht=5.0, units='SI'
            )
        direct_result = get_mid_flame_ws(
            wind_speed=20.0, canopy_cover=50, canopy_ht=20.0,
            canopy_baseht=5.0, units='SI'
        )
        assert alias_result == pytest.approx(direct_result)

    def test_get_flame_length_alias(self):
        with pytest.warns(DeprecationWarning, match="Use .* instead"):
            alias_result = getFlameLength('Byram_HEAD', 100.0)
        direct_result = get_flame_length('Byram_HEAD', 100.0)
        assert alias_result == pytest.approx(direct_result)

    def test_get_flame_height_alias(self):
        with pytest.warns(DeprecationWarning, match="Use .* instead"):
            alias_result = getFlameHeight(
                'Nelson', 5.0, fire_type=1, fire_intensity=1000.0, midflame_ws=2.0
            )
        direct_result = get_flame_height(
            'Nelson', 5.0, fire_type=1, fire_intensity=1000.0, midflame_ws=2.0
        )
        assert alias_result == pytest.approx(direct_result)

    def test_get_flame_tilt_alias(self):
        with pytest.warns(DeprecationWarning, match="Use .* instead"):
            alias_result = getFlameTilt('Standard', flame_length=10.0, flame_height=5.0)
        direct_result = get_flame_tilt('Standard', flame_length=10.0, flame_height=5.0)
        assert alias_result == pytest.approx(direct_result)

    def test_get_flame_residence_time_alias(self):
        with pytest.warns(DeprecationWarning, match="Use .* instead"):
            alias_result = getFlameResidenceTime(1.0, 1.0, 1.0, 'sec')
        direct_result = get_flame_residence_time(1.0, 1.0, 1.0, 'sec')
        assert alias_result == pytest.approx(direct_result)

    def test_get_flame_depth_alias(self):
        with pytest.warns(DeprecationWarning, match="Use .* instead"):
            alias_result = getFlameDepth(2.0, 3.0)
        direct_result = get_flame_depth(2.0, 3.0)
        assert alias_result == pytest.approx(direct_result)

    def test_flame_component_array_multiprocessing_alias(self):
        ros = np.array([1.0, 2.0, 3.0, 4.0])
        res_time = np.array([1.0, 1.0, 1.0, 1.0])
        with pytest.warns(DeprecationWarning, match="Use .* instead"):
            alias_blocks = flameComponent_ArrayMultiprocessing(
                'flame_depth', num_processors=2, block_size=None, ros=ros, res_time=res_time
            )
        direct_blocks = flame_component_array_multiprocessing(
            'flame_depth', num_processors=2, block_size=None, ros=ros, res_time=res_time
        )
        np.testing.assert_allclose(
            np.concatenate(alias_blocks), np.concatenate(direct_blocks)
        )


class TestDeprecatedAliasesExcludedFromAll:
    def test_all_contains_only_snake_case_names(self):
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

    def test_aliases_not_in_all(self):
        aliases = {
            'getMidFlameWS',
            'getFlameLength',
            'getFlameHeight',
            'getFlameTilt',
            'getFlameResidenceTime',
            'getFlameDepth',
            'flameComponent_ArrayMultiprocessing',
        }
        assert aliases.isdisjoint(set(flame_components.__all__))
