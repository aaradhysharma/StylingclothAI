from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import os
from datetime import datetime
from typing import Optional, Dict, List
import uvicorn

app = FastAPI(
    title="Outfit Color Matcher API",
    description="AI-powered clothing color coordination using hashmaps for fast lookups",
    version="1.0.0"
)

# Create upload directory
os.makedirs("static/uploads", exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# HASHMAP STRUCTURES (same as Flask version but with type hints)
wardrobe_hashmap: Dict[str, Dict[str, List[Dict]]] = {}

compatible_colors_hashmap: Dict[str, List[str]] = {
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

basic_colors_hashmap: Dict[str, tuple] = {
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

category_combinations_hashmap: Dict[str, List[str]] = {
    "tops": ["bottoms", "belts", "shoes", "accessories"],
    "bottoms": ["tops", "belts", "shoes", "accessories"],
    "belts": ["tops", "bottoms"],
    "shoes": ["tops", "bottoms"],
    "accessories": ["tops", "bottoms"],
    "dresses": ["belts", "shoes", "accessories"]
}

# Pydantic models for API documentation
from pydantic import BaseModel

class ClothingItem(BaseModel):
    name: str
    color: str
    rgb: tuple
    category: str
    uploaded_at: str

class OutfitSuggestion(BaseModel):
    user_id: str
    base_item: ClothingItem
    suggestions: List[str]
    color_harmony_info: str

class SystemStats(BaseModel):
    total_users: int
    total_items: int
    color_distribution: Dict[str, int]
    available_colors: List[str]
    hashmap_info: Dict[str, int]

# Helper functions (same logic as Flask version)
def get_dominant_color(pil_img: Image.Image) -> tuple:
    """Extract dominant color using K-means clustering"""
    try:
        img = pil_img.copy().resize((50, 50))
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        pixels = np.array(img).reshape(-1, 3)
        kmeans = KMeans(n_clusters=3, n_init=10, random_state=42)
        kmeans.fit(pixels)
        
        centers = kmeans.cluster_centers_
        labels = kmeans.labels_
        counts = np.bincount(labels)
        dominant_cluster_idx = counts.argmax()
        dominant_color = centers[dominant_cluster_idx]
        
        return tuple(int(c) for c in dominant_color)
    except Exception as e:
        print(f"Color extraction error: {e}")
        return (128, 128, 128)

def map_rgb_to_color_name(rgb: tuple) -> str:
    """Map RGB to nearest color name using hashmap"""
    r, g, b = rgb
    closest_color = "gray"
    min_distance = float('inf')
    
    for color_name, (cr, cg, cb) in basic_colors_hashmap.items():
        distance = ((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2) ** 0.5
        if distance < min_distance:
            min_distance = distance
            closest_color = color_name
    
    return closest_color

def add_item_to_wardrobe(user_id: str, category: str, item_data: dict):
    """Add item to wardrobe hashmap"""
    if user_id not in wardrobe_hashmap:
        wardrobe_hashmap[user_id] = {}
    if category not in wardrobe_hashmap[user_id]:
        wardrobe_hashmap[user_id][category] = []
    wardrobe_hashmap[user_id][category].append(item_data)

def get_outfit_suggestions(user_id: str, base_category: str, base_color: str) -> List[str]:
    """Generate suggestions using color compatibility hashmap"""
    if user_id not in wardrobe_hashmap:
        return ["No wardrobe items found. Upload some clothes first!"]
    
    compatible_colors = compatible_colors_hashmap.get(base_color, [])
    if not compatible_colors:
        return [f"No color matching rules found for {base_color}"]
    
    suggestions = []
    compatible_categories = category_combinations_hashmap.get(base_category, [])
    
    for category in compatible_categories:
        if category in wardrobe_hashmap[user_id]:
            for item in wardrobe_hashmap[user_id][category]:
                if item["color"] in compatible_colors:
                    suggestions.append(f"✓ {item['name']} ({item['color']} {category[:-1]})")
    
    if not suggestions:
        for color in compatible_colors[:3]:
            suggestions.append(f"💡 Try pairing with {color} items")
    
    return suggestions

# API Routes
@app.get("/", response_class=HTMLResponse)
async def index():
    """Main page with upload form"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FastAPI Outfit Color Matcher</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .container { background: #f5f5f5; padding: 20px; border-radius: 10px; }
            .form-group { margin: 15px 0; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input, select { padding: 8px; width: 100%; max-width: 300px; }
            button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
            .info { background: #e7f3ff; padding: 15px; border-radius: 5px; margin: 20px 0; }
            .api-link { background: #f8f9fa; padding: 10px; border-radius: 5px; margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 FastAPI Outfit Color Matcher</h1>
            <div class="info">
                <h3>Features:</h3>
                <p>✅ Async image processing with FastAPI</p>
                <p>✅ Automatic API documentation</p>
                <p>✅ Type-safe hashmap operations</p>
                <p>✅ Color coordination suggestions</p>
            </div>
            
            <div class="api-link">
                <h3>🔗 API Documentation:</h3>
                <p><a href="/docs" target="_blank">Interactive API Docs (Swagger UI)</a></p>
                <p><a href="/redoc" target="_blank">Alternative API Docs (ReDoc)</a></p>
            </div>
            
            <h3>Quick Upload Form:</h3>
            <form id="uploadForm" enctype="multipart/form-data">
                <div class="form-group">
                    <label>Select clothing image:</label>
                    <input type="file" id="cloth_image" accept="image/*" required>
                </div>
                <div class="form-group">
                    <label>Category:</label>
                    <select id="category">
                        <option value="tops">Tops</option>
                        <option value="bottoms">Bottoms</option>
                        <option value="dresses">Dresses</option>
                        <option value="belts">Belts</option>
                        <option value="shoes">Shoes</option>
                        <option value="accessories">Accessories</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Item name:</label>
                    <input type="text" id="item_name" placeholder="e.g., Blue Polo Shirt">
                </div>
                <div class="form-group">
                    <label>User ID:</label>
                    <input type="text" id="user_id" value="user1">
                </div>
                <button type="submit">🔍 Analyze & Get Suggestions</button>
            </form>
            
            <div id="results" style="margin-top: 20px;"></div>
        </div>
        
        <script>
        document.getElementById('uploadForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData();
            formData.append('file', document.getElementById('cloth_image').files[0]);
            formData.append('category', document.getElementById('category').value);
            formData.append('item_name', document.getElementById('item_name').value);
            formData.append('user_id', document.getElementById('user_id').value);
            
            try {
                const response = await fetch('/api/upload', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                document.getElementById('results').innerHTML = `
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px;">
                        <h3>🎯 Analysis Complete!</h3>
                        <p><strong>Item:</strong> ${result.item.name} (${result.item.category})</p>
                        <p><strong>Color:</strong> ${result.item.color}</p>
                        <p><strong>RGB:</strong> ${result.item.rgb}</p>
                        <h4>🎨 Suggestions:</h4>
                        <ul>
                            ${result.suggestions.map(s => `<li>${s}</li>`).join('')}
                        </ul>
                    </div>
                `;
            } catch (error) {
                document.getElementById('results').innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
            }
        });
        </script>
    </body>
    </html>
    """

@app.post("/api/upload", response_model=OutfitSuggestion)
async def upload_clothing_item(
    file: UploadFile = File(...),
    category: str = Form(...),
    item_name: Optional[str] = Form("Unnamed Item"),
    user_id: str = Form("user1")
):
    """
    Upload a clothing image and get outfit suggestions
    
    - **file**: Image file of the clothing item
    - **category**: Type of clothing (tops, bottoms, etc.)
    - **item_name**: Optional name for the item
    - **user_id**: User identifier for wardrobe management
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Process image
        image_data = await file.read()
        img = Image.open(io.BytesIO(image_data))
        
        # Extract color
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
        
        # Add to wardrobe
        add_item_to_wardrobe(user_id, category, item_data)
        
        # Get suggestions
        suggestions = get_outfit_suggestions(user_id, category, color_name)
        
        return {
            "user_id": user_id,
            "base_item": item_data,
            "suggestions": suggestions,
            "color_harmony_info": f"Based on {len(compatible_colors_hashmap[color_name])} compatible colors"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@app.get("/api/wardrobe/{user_id}")
async def get_user_wardrobe(user_id: str):
    """Get complete wardrobe for a user"""
    if user_id not in wardrobe_hashmap:
        raise HTTPException(status_code=404, detail="User wardrobe not found")
    
    user_wardrobe = wardrobe_hashmap[user_id]
    total_items = sum(len(items) for items in user_wardrobe.values())
    
    return {
        "user_id": user_id,
        "wardrobe": user_wardrobe,
        "stats": {
            "total_items": total_items,
            "categories": list(user_wardrobe.keys()),
            "items_per_category": {cat: len(items) for cat, items in user_wardrobe.items()}
        }
    }

@app.get("/api/suggest-outfit/{user_id}")
async def suggest_complete_outfit(user_id: str):
    """Generate a complete outfit suggestion"""
    if user_id not in wardrobe_hashmap:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_wardrobe = wardrobe_hashmap[user_id]
    outfit = {}
    
    # Start with a top if available
    if "tops" in user_wardrobe and user_wardrobe["tops"]:
        base_item = user_wardrobe["tops"][0]
        outfit["top"] = base_item
        
        # Find matching items
        compatible_colors = compatible_colors_hashmap.get(base_item["color"], [])
        
        for category in ["bottoms", "belts", "shoes"]:
            if category in user_wardrobe:
                for item in user_wardrobe[category]:
                    if item["color"] in compatible_colors or item["color"] in ["black", "brown"]:
                        outfit[category[:-1]] = item
                        break
    
    return {
        "user_id": user_id,
        "suggested_outfit": outfit,
        "color_harmony": "Based on color compatibility hashmap rules",
        "outfit_score": len(outfit)  # Simple scoring based on completeness
    }

@app.get("/api/stats", response_model=SystemStats)
async def get_system_stats():
    """Get system statistics and hashmap information"""
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
    
    return {
        "total_users": total_users,
        "total_items": total_items,
        "color_distribution": color_distribution,
        "available_colors": list(basic_colors_hashmap.keys()),
        "hashmap_info": {
            "wardrobe_hashmap_size": len(wardrobe_hashmap),
            "color_rules_hashmap_size": len(compatible_colors_hashmap),
            "basic_colors_hashmap_size": len(basic_colors_hashmap),
            "category_combinations_hashmap_size": len(category_combinations_hashmap)
        }
    }

@app.get("/api/colors")
async def get_color_compatibility():
    """Get all color compatibility rules from hashmap"""
    return {
        "color_rules": compatible_colors_hashmap,
        "basic_colors": basic_colors_hashmap,
        "total_rules": len(compatible_colors_hashmap)
    }

# Add missing import
import io

if __name__ == "__main__":
    print("🚀 Starting FastAPI Outfit Color Matcher...")
    print("📊 Hashmap structures initialized:")
    print(f"   - Color compatibility rules: {len(compatible_colors_hashmap)} colors")
    print(f"   - Basic color references: {len(basic_colors_hashmap)} colors")
    print(f"   - Category combinations: {len(category_combinations_hashmap)} categories")
    print("🌐 API Documentation available at:")
    print("   - Swagger UI: http://127.0.0.1:8000/docs")
    print("   - ReDoc: http://127.0.0.1:8000/redoc")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 