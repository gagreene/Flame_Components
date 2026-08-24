"""
Standalone package smoke test for flame-components.

Run this against an INSTALLED package (wheel, sdist, or PyPI/TestPyPI install) in an
environment without the repository on PYTHONPATH -- it does not import anything from
this repo other than the installed `flame_components` package itself. Used in CI
(Phase 4) and for post-build/post-publish verification (Phase 5, 7, 8) of the readiness
plan; see docs/pypi-publication-readiness-plan.md.

Usage: python scripts/smoke_test.py
"""
import sys

import numpy as np

import flame_components as fc


def main():
    assert isinstance(fc.__version__, str) and fc.__version__, (
        f"__version__ missing or empty: {fc.__version__!r}"
    )

    expected_names = {
        'get_mid_flame_ws',
        'get_flame_length',
        'get_flame_height',
        'get_flame_tilt',
        'get_flame_residence_time',
        'get_flame_depth',
        'flame_component_array_multiprocessing',
    }
    assert set(fc.__all__) == expected_names, f"unexpected __all__: {fc.__all__!r}"
    for name in fc.__all__:
        assert callable(getattr(fc, name)), f"{name} in __all__ is not callable"

    # Scalar call
    mid_flame_ws = fc.get_mid_flame_ws(
        wind_speed=15, canopy_cover=50, canopy_ht=10, canopy_baseht=2, units='SI'
    )
    assert isinstance(mid_flame_ws, float) and mid_flame_ws > 0, (
        f"unexpected scalar result: {mid_flame_ws!r}"
    )

    # Array call
    fire_intensity = np.array([100.0, 500.0, 1000.0])
    flame_length = fc.get_flame_length(model='Byram_HEAD', fire_intensity=fire_intensity)
    assert isinstance(flame_length, np.ndarray) and flame_length.shape == (3,), (
        f"unexpected array result: {flame_length!r}"
    )

    # Multiprocessing call
    wind_speed = np.array([10.0, 15.0, 20.0, 25.0, 30.0, 35.0])
    canopy_cover = np.array([40, 50, 60, 40, 50, 60])
    canopy_ht = np.array([8.0, 10.0, 12.0, 8.0, 10.0, 12.0])
    canopy_baseht = np.array([2.0, 2.0, 3.0, 2.0, 2.0, 3.0])
    blocks = fc.flame_component_array_multiprocessing(
        flame_function='midflame_ws',
        num_processors=2,
        wind_speed=wind_speed,
        canopy_cover=canopy_cover,
        canopy_ht=canopy_ht,
        canopy_baseht=canopy_baseht,
        units='SI',
    )
    result = np.concatenate(blocks)
    assert result.shape == wind_speed.shape, f"unexpected multiprocessing result shape: {result.shape!r}"

    print(f"Smoke test passed: flame_components {fc.__version__}")


if __name__ == "__main__":
    # Guarded per Python's multiprocessing requirements -- flame_component_array_
    # multiprocessing spawns worker processes and must not run at import time.
    try:
        main()
    except AssertionError as exc:
        print(f"SMOKE TEST FAILED: {exc}", file=sys.stderr)
        sys.exit(1)
