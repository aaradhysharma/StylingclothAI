"""
Color processing utilities for the outfit matching application.
This module contains hashmap-based color operations and image processing functions.
"""

import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from typing import Tuple, Dict, List
import colorsys

# HASHMAP: Extended color database with more precise color definitions
EXTENDED_COLORS_HASHMAP: Dict[str, Tuple[int, int, int]] = {
    # Basic colors
    "red": (255, 0, 0),
    "green": (0, 128, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "orange": (255, 165, 0),
    "purple": (128, 0, 128),
    "pink": (255, 192, 203),
    
    # Neutrals
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "gray": (128, 128, 128),
    "light_gray": (211, 211, 211),
    "dark_gray": (64, 64, 64),
    
    # Earth tones
    "brown": (165, 42, 42),
    "tan": (210, 180, 140),
    "beige": (245, 245, 220),
    "cream": (255, 253, 208),
    "khaki": (240, 230, 140),
    
    # Blues
    "navy": (0, 0, 128),
    "royal_blue": (65, 105, 225),
    "sky_blue": (135, 206, 235),
    "teal": (0, 128, 128),
    
    # Greens
    "forest_green": (34, 139, 34),
    "olive": (128, 128, 0),
    "mint": (189, 252, 201),
    
    # Reds
    "maroon": (128, 0, 0),
    "burgundy": (128, 0, 32),
    "coral": (255, 127, 80),
    
    # Others
    "gold": (255, 215, 0),
    "silver": (192, 192, 192),
    "lavender": (230, 230, 250)
}

# HASHMAP: Color harmony rules based on color theory
COLOR_HARMONY_HASHMAP: Dict[str, Dict[str, List[str]]] = {
    "complementary": {
        "red": ["green", "teal"],
        "blue": ["orange", "coral"],
        "yellow": ["purple", "lavender"],
        "green": ["red", "pink"],
        "orange": ["blue", "navy"],
        "purple": ["yellow", "gold"]
    },
    "analogous": {
        "red": ["orange", "pink", "burgundy"],
        "blue": ["teal", "purple", "navy"],
        "yellow": ["orange", "gold", "cream"],
        "green": ["teal", "olive", "mint"],
        "orange": ["red", "yellow", "coral"],
        "purple": ["blue", "pink", "lavender"]
    },
    "triadic": {
        "red": ["blue", "yellow"],
        "blue": ["red", "yellow"],
        "yellow": ["red", "blue"],
        "green": ["orange", "purple"],
        "orange": ["green", "purple"],
        "purple": ["green", "orange"]
    }
}

# HASHMAP: Seasonal color palettes
SEASONAL_COLORS_HASHMAP: Dict[str, List[str]] = {
    "spring": ["coral", "mint", "sky_blue", "lavender", "cream", "light_gray"],
    "summer": ["navy", "white", "sky_blue", "pink", "silver", "light_gray"],
    "autumn": ["burgundy", "forest_green", "gold", "brown", "orange", "cream"],
    "winter": ["black", "white", "navy", "red", "royal_blue", "silver"]
}

def extract_dominant_color_advanced(image: Image.Image, k_clusters: int = 5) -> Tuple[int, int, int]:
    """
    Advanced color extraction using K-means clustering with background removal.
    
    Args:
        image: PIL Image object
        k_clusters: Number of color clusters to find
        
    Returns:
        RGB tuple of the dominant color
    """
    try:
        # Resize for performance
        img = image.copy()
        img = img.resize((100, 100))
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Convert to numpy array
        pixels = np.array(img).reshape(-1, 3)
        
        # Remove potential background colors (very light or very dark)
        # This is a simple heuristic - in production, you might use more sophisticated methods
        brightness = np.mean(pixels, axis=1)
        mask = (brightness > 30) & (brightness < 225)  # Remove very dark/light pixels
        
        if np.sum(mask) > 0:
            pixels = pixels[mask]
        
        # Perform K-means clustering
        kmeans = KMeans(n_clusters=min(k_clusters, len(pixels)), n_init=10, random_state=42)
        kmeans.fit(pixels)
        
        # Get cluster centers and their frequencies
        centers = kmeans.cluster_centers_
        labels = kmeans.labels_
        counts = np.bincount(labels)
        
        # Find the most frequent cluster (dominant color)
        dominant_cluster_idx = counts.argmax()
        dominant_color = centers[dominant_cluster_idx]
        
        return tuple(int(c) for c in dominant_color)
        
    except Exception as e:
        print(f"Advanced color extraction error: {e}")
        return (128, 128, 128)  # Default gray

def map_rgb_to_color_name_advanced(rgb: Tuple[int, int, int]) -> str:
    """
    Map RGB values to color names using the extended color hashmap.
    Uses both RGB distance and HSV analysis for better accuracy.
    
    Args:
        rgb: RGB tuple
        
    Returns:
        Color name string
    """
    r, g, b = rgb
    
    # Method 1: Direct RGB distance
    closest_color = "gray"
    min_distance = float('inf')
    
    for color_name, (cr, cg, cb) in EXTENDED_COLORS_HASHMAP.items():
        # Euclidean distance in RGB space
        distance = ((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2) ** 0.5
        if distance < min_distance:
            min_distance = distance
            closest_color = color_name
    
    # Method 2: HSV-based refinement for better color perception
    try:
        h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
        
        # If saturation is very low, it's likely a neutral color
        if s < 0.2:
            if v < 0.3:
                return "black"
            elif v > 0.8:
                return "white"
            else:
                return "gray"
        
        # If saturation is high, use hue to determine base color
        if s > 0.5:
            hue_degrees = h * 360
            if 0 <= hue_degrees < 30 or 330 <= hue_degrees <= 360:
                base_color = "red"
            elif 30 <= hue_degrees < 90:
                base_color = "yellow"
            elif 90 <= hue_degrees < 150:
                base_color = "green"
            elif 150 <= hue_degrees < 210:
                base_color = "blue"
            elif 210 <= hue_degrees < 270:
                base_color = "blue"  # Blue-purple range
            elif 270 <= hue_degrees < 330:
                base_color = "purple"
            else:
                base_color = closest_color
            
            # Refine based on value (brightness)
            if base_color in EXTENDED_COLORS_HASHMAP:
                return base_color
    
    except Exception:
        pass
    
    return closest_color

def get_color_harmony_suggestions(base_color: str, harmony_type: str = "complementary") -> List[str]:
    """
    Get color suggestions based on color harmony theory using hashmaps.
    
    Args:
        base_color: The base color name
        harmony_type: Type of harmony ("complementary", "analogous", "triadic")
        
    Returns:
        List of suggested color names
    """
    if harmony_type not in COLOR_HARMONY_HASHMAP:
        harmony_type = "complementary"
    
    harmony_rules = COLOR_HARMONY_HASHMAP[harmony_type]
    
    # Direct lookup in hashmap
    if base_color in harmony_rules:
        return harmony_rules[base_color]
    
    # If exact color not found, try to find similar colors
    similar_colors = []
    for color_name in harmony_rules.keys():
        if color_name in base_color or base_color in color_name:
            similar_colors.extend(harmony_rules[color_name])
    
    return similar_colors if similar_colors else ["black", "white", "gray"]

def get_seasonal_color_suggestions(season: str) -> List[str]:
    """
    Get color suggestions based on seasonal palettes using hashmap lookup.
    
    Args:
        season: Season name ("spring", "summer", "autumn", "winter")
        
    Returns:
        List of seasonal color names
    """
    return SEASONAL_COLORS_HASHMAP.get(season.lower(), SEASONAL_COLORS_HASHMAP["summer"])

def analyze_color_temperature(rgb: Tuple[int, int, int]) -> str:
    """
    Analyze if a color is warm or cool using color theory.
    
    Args:
        rgb: RGB tuple
        
    Returns:
        "warm", "cool", or "neutral"
    """
    r, g, b = rgb
    
    # Convert to HSV for better analysis
    try:
        h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
        hue_degrees = h * 360
        
        # Low saturation = neutral
        if s < 0.3:
            return "neutral"
        
        # Warm colors: red, orange, yellow (0-60 and 300-360 degrees)
        if (0 <= hue_degrees <= 60) or (300 <= hue_degrees <= 360):
            return "warm"
        # Cool colors: blue, green, purple (120-300 degrees)
        elif 120 <= hue_degrees <= 300:
            return "cool"
        else:
            return "neutral"
            
    except Exception:
        return "neutral"

def get_color_palette_from_image(image: Image.Image, num_colors: int = 5) -> List[Tuple[int, int, int]]:
    """
    Extract a color palette from an image using K-means clustering.
    
    Args:
        image: PIL Image object
        num_colors: Number of colors to extract
        
    Returns:
        List of RGB tuples representing the color palette
    """
    try:
        # Resize for performance
        img = image.copy().resize((100, 100))
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        pixels = np.array(img).reshape(-1, 3)
        
        # Perform clustering
        kmeans = KMeans(n_clusters=num_colors, n_init=10, random_state=42)
        kmeans.fit(pixels)
        
        # Get cluster centers
        centers = kmeans.cluster_centers_
        
        # Sort by frequency
        labels = kmeans.labels_
        counts = np.bincount(labels)
        sorted_indices = np.argsort(counts)[::-1]
        
        palette = []
        for idx in sorted_indices:
            color = tuple(int(c) for c in centers[idx])
            palette.append(color)
        
        return palette
        
    except Exception as e:
        print(f"Palette extraction error: {e}")
        return [(128, 128, 128)] * num_colors

# HASHMAP: Color emotion associations for advanced matching
COLOR_EMOTION_HASHMAP: Dict[str, List[str]] = {
    "professional": ["navy", "black", "white", "gray", "dark_gray"],
    "casual": ["blue", "green", "brown", "beige", "khaki"],
    "elegant": ["black", "white", "navy", "burgundy", "silver"],
    "playful": ["yellow", "orange", "pink", "sky_blue", "mint"],
    "romantic": ["pink", "lavender", "cream", "coral", "white"],
    "bold": ["red", "orange", "royal_blue", "purple", "gold"],
    "earthy": ["brown", "olive", "forest_green", "tan", "cream"],
    "minimalist": ["white", "black", "gray", "beige", "cream"]
}

def get_style_based_colors(style: str) -> List[str]:
    """
    Get color suggestions based on style/mood using emotion hashmap.
    
    Args:
        style: Style name (e.g., "professional", "casual", "elegant")
        
    Returns:
        List of color names that match the style
    """
    return COLOR_EMOTION_HASHMAP.get(style.lower(), COLOR_EMOTION_HASHMAP["casual"])

def calculate_color_contrast(color1: Tuple[int, int, int], color2: Tuple[int, int, int]) -> float:
    """
    Calculate contrast ratio between two colors for accessibility.
    
    Args:
        color1: First RGB color
        color2: Second RGB color
        
    Returns:
        Contrast ratio (1-21, higher is better contrast)
    """
    def luminance(rgb):
        r, g, b = [x/255.0 for x in rgb]
        r = r/12.92 if r <= 0.03928 else ((r + 0.055)/1.055) ** 2.4
        g = g/12.92 if g <= 0.03928 else ((g + 0.055)/1.055) ** 2.4
        b = b/12.92 if b <= 0.03928 else ((b + 0.055)/1.055) ** 2.4
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    
    l1 = luminance(color1)
    l2 = luminance(color2)
    
    lighter = max(l1, l2)
    darker = min(l1, l2)
    
    return (lighter + 0.05) / (darker + 0.05) 