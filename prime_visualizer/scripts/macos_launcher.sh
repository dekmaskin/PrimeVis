#!/bin/bash
# macOS launcher script for Prime Visualizer

# Set up colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Prime Visualizer Launcher${NC}"
echo -e "${BLUE}==========================${NC}"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Find the best Python command to use
find_python_command() {
    if command_exists python3; then
        echo "python3"
    elif command_exists python; then
        # Check if it's Python 3.x
        if [[ $(python --version 2>&1) == *"Python 3"* ]]; then
            echo "python"
        else
            echo ""
        fi
    else
        echo ""
    fi
}

# Install dependencies
install_dependencies() {
    local python_cmd=$1

    echo -e "\n${YELLOW}Checking and installing required packages...${NC}"

    # Check for pip
    if ! $python_cmd -m pip --version >/dev/null 2>&1; then
        echo -e "${RED}Error: pip not found for $python_cmd.${NC}"
        echo "Please install pip by running:"
        echo "  $python_cmd -m ensurepip --upgrade"
        echo "or visit https://pip.pypa.io/en/stable/installation/ for instructions."
        exit 1
    fi

    # Install required packages
    required_packages=("numpy" "pillow" "pyyaml" "matplotlib")

    for package in "${required_packages[@]}"; do
        if ! $python_cmd -c "import ${package//-/_}" >/dev/null 2>&1; then
            echo -e "Installing ${package}..."
            $python_cmd -m pip install $package
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}✓ $package installed successfully${NC}"
            else
                echo -e "${RED}Error installing $package. Please install it manually:${NC}"
                echo "  $python_cmd -m pip install $package"
                exit 1
            fi
        else
            echo -e "${GREEN}✓ $package already installed${NC}"
        fi
    done
}

# Launch the application
launch_app() {
    local python_cmd=$1

    # Get the directory of this script
    script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

    # Go to the parent directory (project root)
    cd "$script_dir/.."

    echo -e "\n${YELLOW}Launching Prime Visualizer...${NC}"

    # Launch the application
    if [ -f "run.py" ]; then
        $python_cmd run.py
    else
        echo -e "${RED}Error: run.py not found in $(pwd)${NC}"
        echo "Make sure you're running this script from the correct directory."
        exit 1
    fi
}

# Main script execution

# Find Python command
PYTHON_CMD=$(find_python_command)

if [ -z "$PYTHON_CMD" ]; then
    echo -e "${RED}Error: Python 3 is required but not found.${NC}"
    echo "Please install Python 3 from https://www.python.org/downloads/"
    exit 1
fi

# Check Python version
python_version=$($PYTHON_CMD --version 2>&1)
echo -e "Using ${BLUE}$python_version${NC}"

# Install dependencies
install_dependencies "$PYTHON_CMD"

# Launch the application
launch_app "$PYTHON_CMD"