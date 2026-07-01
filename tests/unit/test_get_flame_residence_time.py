# tests/unit/test_get_flame_residence_time.py
"""Unit tests for get_flame_residence_time."""
import pytest
import numpy as np
from flame_components import get_flame_residence_time


class TestGetFlameResidenceTimeScalar:
    def test_known_value_seconds(self):
        """
        Formula: 0.39 * W^0.25 * u^1.51 / (ros/60)
        W=1, u=1, ros=1: 0.39 * 1 * 1 / (1/60) = 23.4 sec
        """
        result = get_flame_residence_time(ros=1.0, fuel_consumption=1.0,
                                          midflame_ws=1.0, units='sec')
        assert result == pytest.approx(23.4, rel=1e-4)

    def test_known_value_minutes(self):
        """Same inputs with units='min': 23.4 / 60 = 0.39 min."""
        result = get_flame_residence_time(ros=1.0, fuel_consumption=1.0,
                                          midflame_ws=1.0, units='min')
        assert result == pytest.approx(0.39, rel=1e-4)

    def test_returns_float_not_array(self):
        result = get_flame_residence_time(1.0, 1.0, 1.0, 'sec')
        assert isinstance(result, (float, np.floating))

    def test_non_negative(self):
        result = get_flame_residence_time(1.0, 1.0, 1.0, 'sec')
        assert result >= 0.0


class TestGetFlameResidenceTimeArray:
    def test_array_output_shape(self):
        result = get_flame_residence_time(
            np.array([1.0, 2.0]),
            np.array([0.5, 1.0]),
            np.array([1.0, 1.5]),
            'sec'
        )
        assert result.shape == (2,)

    def test_array_all_non_negative(self):
        result = get_flame_residence_time(
            np.array([1.0, 2.0, 3.0]),
            np.array([0.5, 0.75, 1.0]),
            np.array([1.0, 1.5, 2.0]),
            'sec'
        )
        assert np.all(result >= 0.0)

    def test_nan_propagates(self):
        result = get_flame_residence_time(
            np.array([1.0, np.nan]),
            np.array([1.0, 1.0]),
            np.array([1.0, 1.0]),
            'sec'
        )
        assert np.isnan(result[1])
        assert not np.isnan(result[0])


class TestGetFlameResidenceTimeErrors:
    def test_string_ros_raises(self):
        with pytest.raises(TypeError):
            get_flame_residence_time('fast', 1.0, 1.0, 'sec')
