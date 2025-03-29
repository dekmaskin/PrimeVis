#!/usr/bin/env python3
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the main function
from prime_visualizer.run import main

if __name__ == "__main__":
    main()
