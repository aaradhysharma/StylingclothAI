import os
import requests
from PIL import Image
from io import BytesIO

# Create sample_data directory if it doesn't exist
os.makedirs('sample_data', exist_ok=True)

# Sample clothing images from Unsplash (free to use)
sample_images = {
    'tops': [
        'https://images.unsplash.com/photo-1576566588028-4147f3842f27',  # White t-shirt
        'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab',  # Blue shirt
        'https://images.unsplash.com/photo-1598033129183-c4f50c736f10',  # Red sweater
    ],
    'bottoms': [
        'https://images.unsplash.com/photo-1541099649105-f69ad21f3246',  # Blue jeans
        'https://images.unsplash.com/photo-1552902865-b72c031ac5ea',    # Black pants
        'https://images.unsplash.com/photo-1584370848010-d7fe6bc767ec',  # Khaki pants
    ],
    'dresses': [
        'https://images.unsplash.com/photo-1572804013309-59a88b7e92f1',  # Black dress
        'https://images.unsplash.com/photo-1595777457583-95e059d581b8',  # Summer dress
        'https://images.unsplash.com/photo-1591369822096-ffd140ec948f',  # Formal dress
    ],
    'outerwear': [
        'https://images.unsplash.com/photo-1591047139829-d91aecb6caea',  # Leather jacket
        'https://images.unsplash.com/photo-1591047139829-d91aecb6caea',  # Denim jacket
        'https://images.unsplash.com/photo-1544923246-77307dd654cb',    # Winter coat
    ],
    'shoes': [
        'https://images.unsplash.com/photo-1543163521-1bf539c55dd2',    # Sneakers
        'https://images.unsplash.com/photo-1549298916-b41d501d3772',    # Running shoes
        'https://images.unsplash.com/photo-1543163521-1bf539c55dd2',    # Casual shoes
    ],
    'accessories': [
        'https://images.unsplash.com/photo-1584917865442-de89df76afd3',  # Watch
        'https://images.unsplash.com/photo-1584917865442-de89df76afd3',  # Belt
        'https://images.unsplash.com/photo-1584917865442-de89df76afd3',  # Sunglasses
    ]
}

def download_image(url, category, index):
    try:
        # Add parameters to get a smaller image
        url = f"{url}?w=800&q=80"
        response = requests.get(url)
        if response.status_code == 200:
            # Open and save the image
            img = Image.open(BytesIO(response.content))
            filename = f"sample_data/{category}_{index+1}.jpg"
            img.save(filename)
            print(f"✓ Downloaded {filename}")
            return True
    except Exception as e:
        print(f"✗ Error downloading {url}: {str(e)}")
    return False

def main():
    print("📥 Downloading sample clothing images...")
    
    total_downloaded = 0
    for category, urls in sample_images.items():
        print(f"\n📁 Category: {category}")
        for i, url in enumerate(urls):
            if download_image(url, category, i):
                total_downloaded += 1
    
    print(f"\n✨ Download complete! Downloaded {total_downloaded} images.")
    print("📍 Images are saved in the 'sample_data' directory")

if __name__ == "__main__":
    main() 