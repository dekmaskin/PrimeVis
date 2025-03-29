# Prime Visualizer

A Python application for visualizing prime numbers in a grid pattern, with advanced color-coding for different prime types.

## Features

- Visualize prime numbers as a color-coded grid
- Identify and color 15 different types of primes:
  - Regular primes
  - Twin primes
  - Mersenne primes
  - Safe primes
  - Palindromic primes
  - Circular primes
  - Sophie Germain primes
  - Factorial primes
  - Fibonacci primes
  - Sexy primes
  - Cuban primes
  - Happy primes
  - Chen primes
  - Wieferich primes
  - Isolated primes
- Configurable grid dimensions and visualization parameters
- Intuitive graphical user interface
- Detailed statistics about prime distribution
- Export visualizations as PNG images

## Installation

### Requirements

- Python 3.7+
- Required packages (automatically installed with pip):
  - numpy
  - Pillow (PIL)
  - PyYAML
  - matplotlib

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/prime-visualizer.git
cd prime-visualizer

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

### Installation using pip

```bash
# Install directly from repository
pip install git+https://github.com/yourusername/prime-visualizer.git

# Run the application
prime-visualizer
```

## Usage

### GUI Mode

Simply run the application:

```bash
python run.py
```

The GUI provides:
- Controls for grid size, dot size, and spacing
- Quick visualization generation
- Detailed prime statistics
- Image saving functionality
- Configuration options

### Command-Line Interface

Generate visualizations directly from the command line:

```bash
python run.py --cols 200 --rows 200 --dot-size 6 --spacing 2 --output output.png
```

Options:
- `--cols`: Number of columns in the grid
- `--rows`: Number of rows in the grid
- `--dot-size`: Size of each dot in pixels
- `--spacing`: Spacing between dots in pixels
- `--output`: Output file path
- `--config`: Path to custom configuration file
- `--no-gui`: Run in headless mode (CLI only)

## Configuration

The application uses a YAML configuration file. A default configuration is included, but you can create custom configurations.

Example `config.yaml`:

```yaml
grid:
  columns: 100
  rows: 100
  dot_size: 8
  spacing: 2
  background_color: [255, 255, 255]  # White

colors:
  regular_prime: [0, 0, 0]           # Black
  twin_prime: [255, 0, 0]            # Red
  mersenne_prime: [0, 255, 0]        # Green
  # ...additional prime types...
```

## Development

### Project Structure

The project follows a modular architecture:
- `core/`: Core prime generation and image creation functionality
- `config/`: Configuration handling
- `gui/`: User interface components
- `utils/`: Helper utilities

### Extending Prime Types

To add a new prime type:

1. Add the classifier function in `prime_classifier.py`
2. Update the `classify_prime` function
3. Add the color to your configuration file

## License

MIT License

## Acknowledgments

- Number theory resources and mathematical principles
- Python and its amazing ecosystem