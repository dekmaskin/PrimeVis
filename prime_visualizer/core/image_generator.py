"""
Image generation for prime number visualization.
"""

import os
import math
from typing import Dict, Tuple, List, Set, Any
from PIL import Image, ImageDraw
import logging

from prime_visualizer.core.prime_generator import generate_primes, generate_primes_set
from prime_visualizer.core.prime_classifier import classify_prime


def calculate_dimensions(
        columns: int,
        rows: int,
        dot_size: int,
        spacing: int
    ) -> Tuple[int, int, int]:
    """
    Calculate image dimensions based on grid specifications.

    Args:
        columns (int): Number of dots in the x-axis
        rows (int): Number of dots in the y-axis
        dot_size (int): Size of each dot in pixels
        spacing (int): Spacing between dots in pixels

    Returns:
        Tuple[int, int, int]: Image width, image height, and total number of positions
    """
    # Calculate image dimensions
    image_width = columns * (dot_size + spacing) - spacing
    image_height = rows * (dot_size + spacing) - spacing
    total_positions = columns * rows

    return image_width, image_height, total_positions


def create_prime_grid(
        total_positions: int,
        columns: int,
        rows: int
    ) -> List[Tuple[int, int, str]]:
    """
    Create a grid with prime positions and their classifications.

    Args:
        total_positions (int): Total number of positions in the grid
        columns (int): Number of columns in the grid
        rows (int): Number of rows in the grid

    Returns:
        List[Tuple[int, int, str]]: List of (x, y, prime_type) tuples
    """
    # Generate primes up to the total number of positions
    primes_set = generate_primes_set(total_positions)

    # For each position in the grid, check if it's prime
    prime_points = []
    for pos in range(total_positions):
        # Convert position to 2D coordinates
        x = pos % columns
        y = pos // columns

        if pos in primes_set:
            prime_type = classify_prime(pos, primes_set)
            prime_points.append((x, y, prime_type))

    return prime_points


def draw_visualization(
        prime_points: List[Tuple[int, int, str]],
        columns: int,
        rows: int,
        dot_size: int,
        spacing: int,
        colors: Dict[str, List[int]],
        background_color: List[int],
        output_path: str
    ) -> None:
    """
    Draw the prime visualization to an image.

    Args:
        prime_points (List[Tuple[int, int, str]]): List of (x, y, prime_type) tuples
        columns (int): Number of columns in the grid
        rows (int): Number of rows in the grid
        dot_size (int): Size of each dot in pixels
        spacing (int): Spacing between dots in pixels
        colors (Dict[str, List[int]]): Color mapping for prime types
        background_color (List[int]): Background color [R, G, B]
        output_path (str): Path to save the output image
    """
    # Calculate image dimensions
    width, height, _ = calculate_dimensions(columns, rows, dot_size, spacing)

    # Create image
    img = Image.new('RGB', (width, height), tuple(background_color))
    draw = ImageDraw.Draw(img)

    # Draw dots
    for x, y, prime_type in prime_points:
        color = tuple(colors.get(prime_type, (0, 0, 0)))
        pixel_x = x * (dot_size + spacing)
        pixel_y = y * (dot_size + spacing)

        draw.ellipse(
            [(pixel_x, pixel_y), (pixel_x + dot_size, pixel_y + dot_size)],
            fill=color
        )

    # Ensure output directory exists
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    # Save the image
    img.save(output_path)
    logging.info(f"Image saved to {output_path}")


def generate_statistics(
        prime_points: List[Tuple[int, int, str]],
        columns: int,
        rows: int,
        dot_size: int,
        spacing: int
    ) -> Dict[str, Any]:
    """
    Generate statistics about the prime visualization.

    Args:
        prime_points (List[Tuple[int, int, str]]): List of (x, y, prime_type) tuples
        columns (int): Number of columns in the grid
        rows (int): Number of rows in the grid
        dot_size (int): Size of each dot in pixels
        spacing (int): Spacing between dots in pixels

    Returns:
        Dict[str, Any]: Dictionary of statistics
    """
    # Calculate image dimensions
    width, height, total_positions = calculate_dimensions(columns, rows, dot_size, spacing)

    # Count prime types
    prime_types = {}
    for _, _, prime_type in prime_points:
        prime_types[prime_type] = prime_types.get(prime_type, 0) + 1

    # Calculate additional statistics
    stats = {
        "width": width,
        "height": height,
        "grid_columns": columns,
        "grid_rows": rows,
        "total_positions": total_positions,
        "total_primes": len(prime_points),
        "density": (len(prime_points) / total_positions) * 100,
        "prime_types": prime_types
    }

    return stats


def generate_visualization(
        columns: int,
        rows: int,
        dot_size: int,
        spacing: int,
        colors: Dict[str, List[int]],
        background_color: List[int],
        output_path: str
    ) -> Dict[str, Any]:
    """
    Generate a prime number visualization.

    Args:
        columns (int): Number of columns in the grid
        rows (int): Number of rows in the grid
        dot_size (int): Size of each dot in pixels
        spacing (int): Spacing between dots in pixels
        colors (Dict[str, List[int]]): Color mapping for prime types
        background_color (List[int]): Background color [R, G, B]
        output_path (str): Path to save the output image

    Returns:
        Dict[str, Any]: Dictionary of statistics about the visualization
    """
    # Calculate total positions
    _, _, total_positions = calculate_dimensions(columns, rows, dot_size, spacing)

    # Generate prime positions
    prime_points = create_prime_grid(total_positions, columns, rows)

    # Draw the visualization
    draw_visualization(
        prime_points=prime_points,
        columns=columns,
        rows=rows,
        dot_size=dot_size,
        spacing=spacing,
        colors=colors,
        background_color=background_color,
        output_path=output_path
    )

    # Generate and return statistics
    return generate_statistics(prime_points, columns, rows, dot_size, spacing)
