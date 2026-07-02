# tests/unit/test_get_flame_tilt.py
"""Unit tests for get_flame_tilt."""
import pytest
import numpy as np
from flame_components import get_flame_tilt


class TestGetFlameTiltStandardModel:
    def test_vertical_flame_zero_tilt(self):
        """Vertical flame (height == length) → tilt = 0 degrees."""
        result = get_flame_tilt('Standard', flame_length=10.0, flame_height=10.0)
        assert result == pytest.approx(0.0, abs=1e-6)

    def test_horizontal_flame_90_degrees(self):
        """Fully horizontal flame (height = 0) → tilt = 90 degrees."""
        result = get_flame_tilt('Standard', flame_length=10.0, flame_height=0.0)
        assert result == pytest.approx(90.0, rel=1e-4)

    def test_arccos_half_equals_60_degrees(self):
        """height/length = 0.5 → arccos(0.5) = 60 degrees."""
        result = get_flame_tilt('Standard', flame_length=10.0, flame_height=5.0)
        assert result == pytest.approx(60.0, rel=1e-4)

    def test_returns_float_not_array(self):
        result = get_flame_tilt('Standard', flame_length=10.0, flame_height=7.0)
        assert isinstance(result, (float, np.floating))

    def test_non_negative(self):
        result = get_flame_tilt('Standard', flame_length=10.0, flame_height=7.0)
        assert result >= 0.0


class TestGetFlameTiltFinneyModel:
    def test_flat_ground_returns_non_negative(self):
        result = get_flame_tilt(
            'Finney', flame_length=10.0, flame_height=8.0,
            slope_angle=0.0, slope_units='degrees'
        )
        assert result >= 0.0

    def test_percent_slope_accepted(self):
        result = get_flame_tilt(
            'Finney', flame_length=10.0, flame_height=8.0,
            slope_angle=20.0, slope_units='percent'
        )
        assert result >= 0.0


class TestGetFlameTiltButlerModel:
    def test_butler_returns_positive_tilt(self):
        """Crown fire with wind → positive tilt angle."""
        result = get_flame_tilt(
            'Butler', wind_speed=50.0, wind_speed_units='kph', canopy_ht=20.0
        )
        assert result > 0.0

    def test_higher_wind_produces_more_tilt(self):
        """Stronger wind → greater tilt angle."""
        tilt_low = get_flame_tilt('Butler', wind_speed=20.0, wind_speed_units='kph', canopy_ht=20.0)
        tilt_high = get_flame_tilt('Butler', wind_speed=80.0, wind_speed_units='kph', canopy_ht=20.0)
        assert tilt_high > tilt_low

    def test_mph_units_accepted(self):
        result = get_flame_tilt('Butler', wind_speed=30.0, wind_speed_units='mph', canopy_ht=20.0)
        assert result >= 0.0

    def test_mps_units_accepted(self):
        result = get_flame_tilt('Butler', wind_speed=10.0, wind_speed_units='mps', canopy_ht=20.0)
        assert result >= 0.0


class TestGetFlameTiltArray:
    def test_array_output_shape(self):
        result = get_flame_tilt(
            'Standard',
            flame_length=np.array([10.0, 20.0]),
            flame_height=np.array([5.0, 10.0])
        )
        assert result.shape == (2,)

    def test_nan_propagates(self):
        result = get_flame_tilt(
            'Standard',
            flame_length=np.array([10.0, np.nan]),
            flame_height=np.array([5.0, 5.0])
        )
        assert np.isnan(result[1])
        assert not np.isnan(result[0])


class TestGetFlameTiltErrors:
    def test_invalid_model_raises(self):
        with pytest.raises(ValueError):
            get_flame_tilt('NotAModel', flame_length=10.0, flame_height=5.0)

    def test_standard_missing_flame_height_raises(self):
        with pytest.raises(ValueError):
            get_flame_tilt('Standard', flame_length=10.0)

    def test_butler_missing_canopy_ht_raises(self):
        with pytest.raises(ValueError):
            get_flame_tilt('Butler', wind_speed=50.0, wind_speed_units='kph')
