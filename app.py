from flask import Flask, request, render_template_string, render_template, jsonify
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import os
from werkzeug.utils import secure_filename
import json
from datetime import datetime

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# HASHMAP 1: In-memory wardrobe storage (user_id -> category -> items)
# This is the main hashmap structure for storing user wardrobes
wardrobe_hashmap = {}

# HASHMAP 2: Color compatibility rules (color -> list of compatible colors)
# This hashmap defines which colors go well together
compatible_colors_hashmap = {
    "red": ["black", "white", "navy", "gray", "beige", "cream"],
    "blue": ["white", "gray", "beige", "black", "brown", "cream"],
    "green": ["brown", "black", "white", "beige", "navy"],
    "black": ["white", "gray", "red", "blue", "green", "beige", "pink", "yellow"],
    "white": ["black", "navy", "gray", "red", "blue", "green", "brown"],
    "navy": ["white", "beige", "gray", "red", "brown"],
    "gray": ["white", "black", "red", "blue", "pink", "yellow"],
    "brown": ["beige", "white", "green", "blue", "cream"],
    "beige": ["brown", "white", "blue", "green", "navy"],
    "pink": ["gray", "black", "white", "navy"],
    "yellow": ["black", "gray", "navy", "brown"],
    "purple": ["gray", "black", "white"],
    "orange": ["black", "brown", "navy", "white"],
    "cream": ["brown", "navy", "black", "red"]
}

# HASHMAP 3: Basic color references for RGB mapping
basic_colors_hashmap = {
    "red": (255, 0, 0),
    "green": (0, 128, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "orange": (255, 165, 0),
    "brown": (165, 42, 42),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "gray": (128, 128, 128),
    "beige": (245, 245, 220),
    "pink": (255, 192, 203),
    "purple": (128, 0, 128),
    "navy": (0, 0, 128),
    "cream": (255, 253, 208)
}

# HASHMAP 4: Category compatibility (what goes with what)
category_combinations_hashmap = {
    "tops": ["bottoms", "belts", "shoes", "accessories"],
    "bottoms": ["tops", "belts", "shoes", "accessories"],
    "belts": ["tops", "bottoms"],
    "shoes": ["tops", "bottoms"],
    "accessories": ["tops", "bottoms"],
    "dresses": ["belts", "shoes", "accessories"]
}

def get_dominant_color(pil_img):
    """Extract dominant color from image using K-means clustering"""
    try:
        # Resize image for faster processing
        img = pil_img.copy()
        img = img.resize((50, 50))
        
        # Convert to RGB if not already
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        # Convert to numpy array and reshape
        pixels = np.array(img).reshape(-1, 3)
        
        # Use K-means to find dominant colors
        kmeans = KMeans(n_clusters=3, n_init=10, random_state=42)
        kmeans.fit(pixels)
        
        # Get cluster centers and labels
        centers = kmeans.cluster_centers_
        labels = kmeans.labels_
        
        # Find the most frequent cluster
        counts = np.bincount(labels)
        dominant_cluster_idx = counts.argmax()
        dominant_color = centers[dominant_cluster_idx]
        
        # Convert to integer tuple
        return tuple(int(c) for c in dominant_color)
    except Exception as e:
        print(f"Error in color extraction: {e}")
        return (128, 128, 128)  # Default to gray

def map_rgb_to_color_name(rgb):
    """Map RGB values to nearest basic color name using hashmap lookup"""
    r, g, b = rgb
    closest_color = "gray"  # default
    min_distance = float('inf')
    
    # Use hashmap to find nearest color
    for color_name, (cr, cg, cb) in basic_colors_hashmap.items():
        # Calculate Euclidean distance in RGB space
        distance = ((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2) ** 0.5
        if distance < min_distance:
            min_distance = distance
            closest_color = color_name
    
    return closest_color

def add_item_to_wardrobe(user_id, category, item_data):
    """Add item to user's wardrobe using hashmap structure"""
    # Initialize user wardrobe if doesn't exist
    if user_id not in wardrobe_hashmap:
        wardrobe_hashmap[user_id] = {}
    
    # Initialize category if doesn't exist
    if category not in wardrobe_hashmap[user_id]:
        wardrobe_hashmap[user_id][category] = []
    
    # Add item to the category list
    wardrobe_hashmap[user_id][category].append(item_data)

def get_outfit_suggestions(user_id, base_category, base_color):
    """Generate outfit suggestions using color compatibility hashmap"""
    suggestions = []
    
    if user_id not in wardrobe_hashmap:
        return ["No wardrobe items found. Upload some clothes first!"]
    
    # Get compatible colors from hashmap
    compatible_colors = compatible_colors_hashmap.get(base_color, [])
    
    if not compatible_colors:
        return [f"No color matching rules found for {base_color}"]
    
    # Check each compatible category
    compatible_categories = category_combinations_hashmap.get(base_category, [])
    
    for category in compatible_categories:
        if category in wardrobe_hashmap[user_id]:
            # Find items in this category with compatible colors
            matching_items = []
            for item in wardrobe_hashmap[user_id][category]:
                if item["color"] in compatible_colors:
                    matching_items.append(item)
            
            if matching_items:
                for item in matching_items:
                    suggestions.append(f"✓ {item['name']} ({item['color']} {category[:-1]})")
    
    # If no specific items found, give general color suggestions
    if not suggestions:
        for color in compatible_colors[:3]:  # Top 3 compatible colors
            suggestions.append(f"💡 Try pairing with {color} items")
    
    return suggestions

@app.route('/')
def index():
    """Main page with upload form"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_and_analyze():
    """Handle file upload and provide outfit suggestions"""
    try:
        # Validate file upload
        if 'cloth_image' not in request.files:
            return "No file uploaded", 400
        
        file = request.files['cloth_image']
        if file.filename == '':
            return "No file selected", 400
        
        # Get form data
        category = request.form.get('category', 'tops')
        item_name = request.form.get('item_name', 'Unnamed Item')
        user_id = request.form.get('user_id', 'user1')
        
        # Process the image
        img = Image.open(file.stream)
        dominant_rgb = get_dominant_color(img)
        color_name = map_rgb_to_color_name(dominant_rgb)
        
        # Create item data
        item_data = {
            "name": item_name,
            "color": color_name,
            "rgb": dominant_rgb,
            "category": category,
            "uploaded_at": datetime.now().isoformat()
        }
        
        # Add to wardrobe hashmap
        add_item_to_wardrobe(user_id, category, item_data)
        
        # Get outfit suggestions
        suggestions = get_outfit_suggestions(user_id, category, color_name)
        
        # Return results using the new template
        return render_template('results.html',
                             item_name=item_name, 
                             category=category, 
                             color_name=color_name, 
                             rgb=dominant_rgb,
                             suggestions=suggestions,
                             user_id=user_id)
        
    except Exception as e:
        return f"Error processing image: {str(e)}", 500

@app.route('/wardrobe/<user_id>')
def view_wardrobe(user_id):
    """Display user's complete wardrobe"""
    if user_id not in wardrobe_hashmap:
        return f"No wardrobe found for user {user_id}"
    
    user_wardrobe = wardrobe_hashmap[user_id]
    total_items = sum(len(items) for items in user_wardrobe.values())
    
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>My Wardrobe</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 1000px; margin: 0 auto; padding: 20px; }
            .category { background: #f8f9fa; margin: 20px 0; padding: 15px; border-radius: 8px; }
            .item { background: white; margin: 10px 0; padding: 10px; border-radius: 5px; border-left: 4px solid #007bff; }
            .color-indicator { width: 20px; height: 20px; display: inline-block; border: 1px solid #333; margin-right: 10px; vertical-align: middle; }
            .stats { background: #e7f3ff; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <h1>👔 {{ user_id }}'s Wardrobe</h1>
        
        <div class="stats">
            <h3>📊 Wardrobe Stats:</h3>
            <p>Total items: <strong>{{ total_items }}</strong></p>
            <p>Categories: <strong>{{ categories|length }}</strong></p>
        </div>
        
        {% for category, items in wardrobe.items() %}
            <div class="category">
                <h3>{{ category.title() }} ({{ items|length }} items)</h3>
                {% for item in items %}
                    <div class="item">
                        <span class="color-indicator" style="background-color: rgb{{ item.rgb }}"></span>
                        <strong>{{ item.name }}</strong> - {{ item.color }} 
                        <small>(added {{ item.uploaded_at[:10] }})</small>
                    </div>
                {% endfor %}
            </div>
        {% endfor %}
        
        <div style="margin-top: 30px;">
            <a href="/">⬅️ Add More Items</a> | 
            <a href="/api/suggest/{{ user_id }}">🎨 Get Random Outfit</a>
        </div>
    </body>
    </html>
    """, 
    user_id=user_id, 
    wardrobe=user_wardrobe, 
    total_items=total_items,
    categories=list(user_wardrobe.keys()))

@app.route('/api/suggest/<user_id>')
def api_suggest_outfit(user_id):
    """API endpoint to get a complete outfit suggestion"""
    if user_id not in wardrobe_hashmap:
        return jsonify({"error": "User not found"})
    
    user_wardrobe = wardrobe_hashmap[user_id]
    
    # Try to build a complete outfit
    outfit = {}
    
    # Start with a top if available
    if "tops" in user_wardrobe and user_wardrobe["tops"]:
        base_item = user_wardrobe["tops"][0]  # Take first top
        outfit["top"] = base_item
        
        # Find matching bottom
        compatible_colors = compatible_colors_hashmap.get(base_item["color"], [])
        if "bottoms" in user_wardrobe:
            for bottom in user_wardrobe["bottoms"]:
                if bottom["color"] in compatible_colors:
                    outfit["bottom"] = bottom
                    break
        
        # Find matching accessories
        for category in ["belts", "shoes"]:
            if category in user_wardrobe:
                for item in user_wardrobe[category]:
                    if item["color"] in compatible_colors or item["color"] in ["black", "brown"]:
                        outfit[category[:-1]] = item
                        break
    
    return jsonify({
        "user_id": user_id,
        "suggested_outfit": outfit,
        "color_harmony": "Based on color compatibility hashmap rules"
    })

@app.route('/api/stats')
def api_stats():
    """API endpoint showing system statistics"""
    total_users = len(wardrobe_hashmap)
    total_items = sum(
        sum(len(items) for items in user_wardrobe.values()) 
        for user_wardrobe in wardrobe_hashmap.values()
    )
    
    color_distribution = {}
    for user_wardrobe in wardrobe_hashmap.values():
        for category_items in user_wardrobe.values():
            for item in category_items:
                color = item["color"]
                color_distribution[color] = color_distribution.get(color, 0) + 1
    
    return jsonify({
        "system_stats": {
            "total_users": total_users,
            "total_items": total_items,
            "color_distribution": color_distribution,
            "available_colors": list(basic_colors_hashmap.keys()),
            "color_rules": len(compatible_colors_hashmap),
            "hashmap_info": {
                "wardrobe_hashmap_size": len(wardrobe_hashmap),
                "color_rules_hashmap_size": len(compatible_colors_hashmap),
                "basic_colors_hashmap_size": len(basic_colors_hashmap),
                "category_combinations_hashmap_size": len(category_combinations_hashmap)
            }
        }
    })

if __name__ == '__main__':
    print("🎨 Starting Outfit Color Matcher...")
    print("📊 Hashmap structures initialized:")
    print(f"   - Color compatibility rules: {len(compatible_colors_hashmap)} colors")
    print(f"   - Basic color references: {len(basic_colors_hashmap)} colors")
    print(f"   - Category combinations: {len(category_combinations_hashmap)} categories")
    print("🚀 Server starting on http://127.0.0.1:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 