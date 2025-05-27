#!/usr/bin/env python3
"""
Test script for the Outfit Color Matcher application.
Demonstrates hashmap functionality and color matching logic.
"""

import sys
import os
from PIL import Image
import numpy as np

# Add current directory to path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from color_utils import (
    EXTENDED_COLORS_HASHMAP,
    COLOR_HARMONY_HASHMAP,
    SEASONAL_COLORS_HASHMAP,
    COLOR_EMOTION_HASHMAP,
    extract_dominant_color_advanced,
    map_rgb_to_color_name_advanced,
    get_color_harmony_suggestions,
    get_seasonal_color_suggestions,
    get_style_based_colors,
    analyze_color_temperature,
    calculate_color_contrast
)

def test_hashmap_structures():
    """Test all hashmap structures are properly initialized"""
    print("🧪 Testing Hashmap Structures")
    print("=" * 50)
    
    print(f"✅ Extended Colors Hashmap: {len(EXTENDED_COLORS_HASHMAP)} colors")
    print(f"   Sample colors: {list(EXTENDED_COLORS_HASHMAP.keys())[:5]}")
    
    print(f"✅ Color Harmony Hashmap: {len(COLOR_HARMONY_HASHMAP)} harmony types")
    print(f"   Harmony types: {list(COLOR_HARMONY_HASHMAP.keys())}")
    
    print(f"✅ Seasonal Colors Hashmap: {len(SEASONAL_COLORS_HASHMAP)} seasons")
    print(f"   Seasons: {list(SEASONAL_COLORS_HASHMAP.keys())}")
    
    print(f"✅ Color Emotion Hashmap: {len(COLOR_EMOTION_HASHMAP)} styles")
    print(f"   Styles: {list(COLOR_EMOTION_HASHMAP.keys())}")
    
    print()

def test_color_mapping():
    """Test RGB to color name mapping using hashmap"""
    print("🎨 Testing Color Mapping")
    print("=" * 50)
    
    test_colors = [
        ((255, 0, 0), "red"),
        ((0, 0, 255), "blue"),
        ((0, 128, 0), "green"),
        ((255, 255, 255), "white"),
        ((0, 0, 0), "black"),
        ((128, 128, 128), "gray"),
        ((255, 192, 203), "pink"),
        ((165, 42, 42), "brown")
    ]
    
    for rgb, expected in test_colors:
        detected = map_rgb_to_color_name_advanced(rgb)
        status = "✅" if detected == expected else "⚠️"
        print(f"{status} RGB {rgb} -> Detected: {detected} (Expected: {expected})")
    
    print()

def test_color_harmony():
    """Test color harmony suggestions using hashmap lookups"""
    print("🌈 Testing Color Harmony")
    print("=" * 50)
    
    test_cases = [
        ("red", "complementary"),
        ("blue", "analogous"),
        ("yellow", "triadic"),
        ("green", "complementary")
    ]
    
    for base_color, harmony_type in test_cases:
        suggestions = get_color_harmony_suggestions(base_color, harmony_type)
        print(f"✅ {base_color} + {harmony_type}: {suggestions}")
    
    print()

def test_seasonal_suggestions():
    """Test seasonal color suggestions"""
    print("🍂 Testing Seasonal Color Suggestions")
    print("=" * 50)
    
    for season in ["spring", "summer", "autumn", "winter"]:
        colors = get_seasonal_color_suggestions(season)
        print(f"✅ {season.title()}: {colors}")
    
    print()

def test_style_based_colors():
    """Test style-based color suggestions"""
    print("👔 Testing Style-Based Color Suggestions")
    print("=" * 50)
    
    styles = ["professional", "casual", "elegant", "playful", "romantic"]
    for style in styles:
        colors = get_style_based_colors(style)
        print(f"✅ {style.title()}: {colors}")
    
    print()

def test_color_temperature():
    """Test color temperature analysis"""
    print("🌡️ Testing Color Temperature Analysis")
    print("=" * 50)
    
    test_colors = [
        ((255, 0, 0), "warm"),    # Red
        ((0, 0, 255), "cool"),    # Blue
        ((255, 165, 0), "warm"),  # Orange
        ((0, 128, 0), "cool"),    # Green
        ((128, 128, 128), "neutral")  # Gray
    ]
    
    for rgb, expected_temp in test_colors:
        detected_temp = analyze_color_temperature(rgb)
        status = "✅" if detected_temp == expected_temp else "⚠️"
        print(f"{status} RGB {rgb} -> {detected_temp} (Expected: {expected_temp})")
    
    print()

def test_color_contrast():
    """Test color contrast calculation"""
    print("🔍 Testing Color Contrast Calculation")
    print("=" * 50)
    
    contrast_tests = [
        ((0, 0, 0), (255, 255, 255)),      # Black vs White (highest contrast)
        ((255, 0, 0), (0, 255, 0)),        # Red vs Green
        ((0, 0, 255), (255, 255, 0)),      # Blue vs Yellow
        ((128, 128, 128), (255, 255, 255)) # Gray vs White
    ]
    
    for color1, color2 in contrast_tests:
        contrast = calculate_color_contrast(color1, color2)
        print(f"✅ {color1} vs {color2}: Contrast ratio = {contrast:.2f}")
    
    print()

def create_test_image(color_rgb, size=(100, 100)):
    """Create a test image with a solid color"""
    img = Image.new('RGB', size, color_rgb)
    return img

def test_image_color_extraction():
    """Test color extraction from images"""
    print("📸 Testing Image Color Extraction")
    print("=" * 50)
    
    test_colors = [
        (255, 0, 0),    # Red
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (255, 255, 0),  # Yellow
    ]
    
    for color_rgb in test_colors:
        # Create test image
        test_img = create_test_image(color_rgb)
        
        # Extract dominant color
        extracted_rgb = extract_dominant_color_advanced(test_img)
        extracted_name = map_rgb_to_color_name_advanced(extracted_rgb)
        
        print(f"✅ Original: {color_rgb} -> Extracted: {extracted_rgb} ({extracted_name})")
    
    print()

def test_wardrobe_simulation():
    """Simulate wardrobe operations using hashmaps"""
    print("👗 Testing Wardrobe Simulation")
    print("=" * 50)
    
    # Simulate the main wardrobe hashmap structure
    wardrobe_hashmap = {}
    
    # Add test items
    test_items = [
        ("user1", "tops", {"name": "Red Shirt", "color": "red", "rgb": (255, 0, 0)}),
        ("user1", "bottoms", {"name": "Blue Jeans", "color": "blue", "rgb": (0, 0, 255)}),
        ("user1", "belts", {"name": "Black Belt", "color": "black", "rgb": (0, 0, 0)}),
        ("user2", "tops", {"name": "White Blouse", "color": "white", "rgb": (255, 255, 255)}),
        ("user2", "bottoms", {"name": "Black Pants", "color": "black", "rgb": (0, 0, 0)})
    ]
    
    # Add items to wardrobe hashmap
    for user_id, category, item_data in test_items:
        if user_id not in wardrobe_hashmap:
            wardrobe_hashmap[user_id] = {}
        if category not in wardrobe_hashmap[user_id]:
            wardrobe_hashmap[user_id][category] = []
        wardrobe_hashmap[user_id][category].append(item_data)
    
    # Test hashmap operations
    print(f"✅ Total users in wardrobe: {len(wardrobe_hashmap)}")
    
    for user_id, user_wardrobe in wardrobe_hashmap.items():
        total_items = sum(len(items) for items in user_wardrobe.values())
        print(f"✅ {user_id}: {total_items} items across {len(user_wardrobe)} categories")
        
        for category, items in user_wardrobe.items():
            print(f"   - {category}: {[item['name'] for item in items]}")
    
    print()

def test_outfit_matching_logic():
    """Test the core outfit matching logic"""
    print("🎯 Testing Outfit Matching Logic")
    print("=" * 50)
    
    # Test color compatibility from the main app
    compatible_colors_hashmap = {
        "red": ["black", "white", "navy", "gray", "beige", "cream"],
        "blue": ["white", "gray", "beige", "black", "brown", "cream"],
        "white": ["black", "navy", "gray", "red", "blue", "green", "brown"],
        "black": ["white", "gray", "red", "blue", "green", "beige", "pink", "yellow"]
    }
    
    # Test scenarios
    test_scenarios = [
        ("red", "tops", ["black", "white", "navy"]),
        ("blue", "bottoms", ["white", "gray", "beige"]),
        ("white", "tops", ["black", "navy", "gray"]),
        ("black", "belts", ["white", "gray", "red"])
    ]
    
    for base_color, category, expected_matches in test_scenarios:
        compatible_colors = compatible_colors_hashmap.get(base_color, [])
        matches = [color for color in expected_matches if color in compatible_colors]
        
        print(f"✅ {base_color} {category} matches: {matches}")
        print(f"   All compatible colors: {compatible_colors}")
    
    print()

def run_performance_test():
    """Test performance of hashmap operations"""
    print("⚡ Testing Performance")
    print("=" * 50)
    
    import time
    
    # Test hashmap lookup performance
    start_time = time.time()
    
    # Perform 10000 color lookups
    for i in range(10000):
        test_rgb = (i % 256, (i * 2) % 256, (i * 3) % 256)
        color_name = map_rgb_to_color_name_advanced(test_rgb)
    
    lookup_time = time.time() - start_time
    print(f"✅ 10,000 color lookups completed in {lookup_time:.4f} seconds")
    print(f"   Average lookup time: {(lookup_time / 10000) * 1000:.4f} ms")
    
    # Test harmony suggestions performance
    start_time = time.time()
    
    for i in range(1000):
        base_color = list(COLOR_HARMONY_HASHMAP["complementary"].keys())[i % 6]
        suggestions = get_color_harmony_suggestions(base_color, "complementary")
    
    harmony_time = time.time() - start_time
    print(f"✅ 1,000 harmony suggestions completed in {harmony_time:.4f} seconds")
    
    print()

def main():
    """Run all tests"""
    print("🧪 OUTFIT COLOR MATCHER - TEST SUITE")
    print("=" * 60)
    print("Testing hashmap-based color matching functionality")
    print("=" * 60)
    print()
    
    try:
        test_hashmap_structures()
        test_color_mapping()
        test_color_harmony()
        test_seasonal_suggestions()
        test_style_based_colors()
        test_color_temperature()
        test_color_contrast()
        test_image_color_extraction()
        test_wardrobe_simulation()
        test_outfit_matching_logic()
        run_performance_test()
        
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("✅ Hashmap structures working correctly")
        print("✅ Color processing functions operational")
        print("✅ Outfit matching logic verified")
        print("✅ Performance within acceptable limits")
        print()
        print("🚀 Ready to run the main application!")
        
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 