# tests/test_gotchas.py
"""Regression tests for bugs identified in docs/CODEBASE.md."""
import pytest
import numpy as np
from flame_components import (
    getFlameHeight,
    flameComponent_ArrayMultiprocessing,
)


class TestFireTypeBugs:
    """
    Two bugs in getFlameHeight fire_type validation:
      Bug 1 (line 295): str not in permitted isinstance types → TypeError for string fire_type
      Bug 2 (line 305): isinstance checks midflame_ws not fire_type → AttributeError when
                        midflame_ws is ndarray and fire_type is scalar
    """

    def test_string_fire_type_surface_does_not_raise_type_error(self):
        """Bug 1: fire_type='surface' must not raise TypeError."""
        result = getFlameHeight(
            model='Nelson',
            flame_length=5.0,
            fire_type='surface',
            fire_intensity=1000.0,
            midflame_ws=2.0,
        )
        assert result >= 0

    def test_string_fire_type_active_crown_does_not_raise_type_error(self):
        """Bug 1: fire_type='active crown' must not raise TypeError."""
        result = getFlameHeight(
            model='Nelson',
            flame_length=10.0,
            fire_type='active crown',
            fire_intensity=5000.0,
            midflame_ws=3.0,
        )
        assert result >= 0

    def test_string_fire_type_with_array_midflame_ws(self):
        """Both bugs: string fire_type with ndarray midflame_ws (requires both fixes)."""
        result = getFlameHeight(
            model='Nelson',
            flame_length=np.array([5.0, 6.0]),
            fire_type='surface',
            fire_intensity=np.array([1000.0, 1500.0]),
            midflame_ws=np.array([2.0, 2.5]),
        )
        assert result.shape == (2,)
        assert np.all(result >= 0)


class TestMultiprocessingBugs:
    """
    Two bugs in flameComponent_ArrayMultiprocessing:
      Bug 3 (line 679): *kwargs (tuple) should be **kwargs (dict)
      Bug 4 (line 702): 'getFlameResidence' should be 'getFlameResidenceTime'
    """

    def test_kwargs_signature_accepts_keyword_arguments(self):
        """
        Bug 3: passing keyword args must not raise TypeError.
        After fix, the function accepts **kwargs and can call .items().
        We expect it to proceed past argument parsing; any subsequent error is acceptable.
        """
        ros = np.array([1.0, 1.5, 2.0, 2.5])
        fc_arr = np.array([0.5, 0.6, 0.7, 0.8])
        ws = np.array([1.0, 1.2, 1.4, 1.6])
        try:
            flameComponent_ArrayMultiprocessing(
                'flame_residence', 2, None,
                ros=ros, fuel_consumption=fc_arr, midflame_ws=ws, units='sec'
            )
        except TypeError as e:
            pytest.fail(f"Bug 3 still present — *kwargs signature rejected keyword args: {e}")

    def test_flame_residence_key_resolves_to_valid_function(self):
        """
        Bug 4: 'flame_residence' must not raise ValueError('does not exist').
        After fix, globals().get('getFlameResidenceTime') returns the actual function.
        """
        ros = np.array([1.0, 1.5, 2.0, 2.5])
        fc_arr = np.array([0.5, 0.6, 0.7, 0.8])
        ws = np.array([1.0, 1.2, 1.4, 1.6])
        try:
            flameComponent_ArrayMultiprocessing(
                'flame_residence', 2, None,
                ros=ros, fuel_consumption=fc_arr, midflame_ws=ws, units='sec'
            )
        except ValueError as e:
            assert 'does not exist' not in str(e), (
                f"Bug 4 still present — 'flame_residence' resolved to None: {e}"
            )
