# Installation Guide for Prime Visualizer

This guide provides detailed instructions for installing and running the Prime Visualizer application on different operating systems.

## Requirements

- Python 3.7 or higher
- Pip (Python package installer)

## macOS Installation

### Option 1: Using the launcher script (recommended)

1. Open Terminal
2. Navigate to the project directory:
   ```bash
   cd /path/to/prime-visualizer
   ```
3. Make the launcher script executable:
   ```bash
   chmod +x scripts/macos_launcher.sh
   ```
4. Run the launcher:
   ```bash
   ./scripts/macos_launcher.sh
   ```
   The launcher will automatically check and install dependencies before starting the application.

### Option 2: Manual installation

1. Open Terminal
2. Install required packages:
   ```bash
   pip3 install numpy Pillow PyYAML matplotlib
   ```
3. Run the application:
   ```bash
   python3 run.py
   ```

## Windows Installation

1. Open Command Prompt (or PowerShell)
2. Navigate to the project directory:
   ```
   cd \path\to\prime-visualizer
   ```
3. Install required packages:
   ```
   pip install numpy Pillow PyYAML matplotlib
   ```
4. Run the application:
   ```
   python run.py
   ```

## Linux Installation

1. Open Terminal
2. Navigate to the project directory:
   ```bash
   cd /path/to/prime-visualizer
   ```
3. Install required packages:
   ```bash
   pip3 install numpy Pillow PyYAML matplotlib
   ```
4. Run the application:
   ```bash
   python3 run.py
   ```

## Installation as a Package

You can also install Prime Visualizer as a Python package:

```bash
# Install directly from the directory
pip install /path/to/prime-visualizer

# Or install from GitHub
pip install git+https://github.com/yourusername/prime-visualizer.git
```

After installation, you can run the application from anywhere:

```bash
prime-visualizer
```

## Troubleshooting

### Package Installation Issues

If you have trouble installing the dependencies, try:

```bash
pip install --upgrade pip
pip install --upgrade -r requirements.txt
```

### Tkinter Errors

If you get Tkinter-related errors:

- **macOS**: Ensure you're using Python from python.org, not the system Python
- **Linux**: Install Tkinter using your package manager:
  ```bash
  # Debian/Ubuntu
  sudo apt-get install python3-tk

  # Fedora
  sudo dnf install python3-tkinter

  # Arch
  sudo pacman -S tk
  ```

### Permission Errors

If you get permission errors when installing packages:

- **Option 1**: Use a virtual environment:
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  pip install -r requirements.txt
  ```

- **Option 2**: Use `--user` flag:
  ```bash
  pip install --user -r requirements.txt
  ```