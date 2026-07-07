
# Flame Components

This repository provides several functions for calculating various fire behavior metrics such as mid-flame wind speed, flame length, flame height, flame tilt, flame residence time, and flame depth. It also includes utility functions for multiprocessing these calculations across blocks of data, which can be useful for high-performance fire modeling.

## Features

- **Mid-Flame Wind Speed Calculation** (`get_mid_flame_ws`): Calculates mid-flame wind speed based on parameters such as wind speed, canopy cover, and canopy height.
- **Flame Length Estimation** (`get_flame_length`): Estimates flame length using different published models.
- **Flame Height Calculation** (`get_flame_height`): Calculates flame height based on flame length and model-specific parameters.
- **Flame Tilt Angle Calculation** (`get_flame_tilt`): Calculates the angle of flame tilt relative to vertical.
- **Flame Residence Time** (`get_flame_residence_time`): Computes flame residence time based on rate of spread, fuel consumption, and wind speed.
- **Flame Depth Calculation** (`get_flame_depth`): Calculates flame depth using flame residence time and rate of spread.
- **Array Multiprocessing** (`flame_component_array_multiprocessing`): Enables multiprocessing of flame component calculations across blocks of data, making large-scale processing efficient.

## Requirements

- Python 3.9+
- **Libraries**: `numpy`

## Installation

```bash
pip install flame-components
```

## Development

This project uses [uv](https://docs.astral.sh/uv/) for dependency management and
packaging.

```bash
uv sync              # create .venv and install runtime + dev dependencies
uv run pytest tests/ -v   # run the test suite
uv build             # build the wheel and sdist into dist/
```

## Usage

### Key Functions

- **`get_mid_flame_ws`**: Calculates mid-flame wind speed.
- **`get_flame_length`**: Estimates flame length based on specified models.
- **`get_flame_height`**: Calculates flame height for a given flame length.
- **`get_flame_tilt`**: Computes flame tilt angle using various models.
- **`get_flame_residence_time`**: Estimates flame residence time for a given rate of spread.
- **`get_flame_depth`**: Computes flame depth from flame residence time and rate of spread.

### Example

```python
from flame_components import get_mid_flame_ws, get_flame_length

# Example calculation for mid-flame wind speed
mid_flame_ws = get_mid_flame_ws(
    wind_speed=15,
    canopy_cover=50,
    canopy_ht=10,
    canopy_baseht=2,
    units='SI'
)

# Example calculation for flame length
flame_length = get_flame_length(
    model='Byram_HEAD',
    fire_intensity=500
)
```

### Array Multiprocessing Example

To perform calculations across blocks of data using multiple processors:

```python
from flame_components import flame_component_array_multiprocessing

# Example multiprocessing calculation
results = flame_component_array_multiprocessing(
    flame_function='midflame_ws',
    num_processors=4,
    wind_speed=array_of_wind_speed,
    canopy_cover=array_of_canopy_cover,
    canopy_ht=array_of_canopy_ht,
    canopy_baseht=array_of_canopy_baseht,
    units='SI'
)
```

## Contributing

Contributions are welcome. If you have ideas for new features or improvements, please submit a pull request or open an issue.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
