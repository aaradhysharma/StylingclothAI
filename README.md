<<<<<<< HEAD
# clothstyle
Testapp forAI and hashmap
=======
# 🎨 Outfit Color Matcher

An AI-powered clothing color coordination web application built with Python, featuring hashmap-based fast lookups for outfit suggestions.

## 🌟 Features

- **Image Upload & Color Analysis**: Upload photos of clothing items and get dominant color extraction using K-means clustering
- **Hashmap-Based Matching**: Lightning-fast color compatibility lookups using multiple hashmap structures
- **Color Harmony Theory**: Suggestions based on complementary, analogous, and triadic color relationships
- **Wardrobe Management**: Store and organize your clothing items by category
- **Multiple Frameworks**: Both Flask and FastAPI implementations available
- **Easy Deployment**: Docker support for platforms like Fly.io, Render, and Vercel

## 🗂️ Hashmap Structures

This application extensively uses Python dictionaries (hashmaps) for efficient data operations:

1. **Wardrobe Hashmap**: `user_id → category → [items]` for O(1) user wardrobe access
2. **Color Compatibility Hashmap**: `color → [compatible_colors]` for instant matching rules
3. **Basic Colors Hashmap**: `color_name → RGB_tuple` for color name mapping
4. **Category Combinations Hashmap**: `category → [compatible_categories]` for outfit building
5. **Seasonal Colors Hashmap**: `season → [color_palette]` for seasonal suggestions
6. **Color Emotion Hashmap**: `style → [colors]` for mood-based recommendations

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip package manager

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd cache-service
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run tests** (optional but recommended):
   ```bash
   python test_app.py
   ```

4. **Start the Flask application**:
   ```bash
   python app.py
   ```
   
   Or start the FastAPI application:
   ```bash
   python fastapi_app.py
   ```

5. **Open your browser**:
   - Flask: http://127.0.0.1:5000
   - FastAPI: http://127.0.0.1:8000 (includes auto-generated API docs at `/docs`)

## 📖 Usage

### Basic Workflow

1. **Upload a clothing image** - Select a photo of a shirt, pants, dress, etc.
2. **Choose category** - Specify if it's tops, bottoms, belts, shoes, or accessories
3. **Get suggestions** - Receive color-coordinated outfit recommendations
4. **Build wardrobe** - Add multiple items to create a complete digital wardrobe
5. **Generate outfits** - Get complete outfit suggestions from your wardrobe

### API Endpoints (FastAPI)

- `POST /api/upload` - Upload clothing image and get suggestions
- `GET /api/wardrobe/{user_id}` - View user's complete wardrobe
- `GET /api/suggest-outfit/{user_id}` - Get complete outfit suggestion
- `GET /api/stats` - System statistics and hashmap information
- `GET /api/colors` - View all color compatibility rules
- `GET /docs` - Interactive API documentation

## 🎨 Color Matching Logic

The application uses several color theory principles:

### Color Harmony Types
- **Complementary**: Colors opposite on the color wheel (red ↔ green)
- **Analogous**: Colors adjacent on the color wheel (red → orange → yellow)
- **Triadic**: Colors evenly spaced on the color wheel (red, blue, yellow)

### Color Temperature Analysis
- **Warm colors**: Reds, oranges, yellows (0-60° and 300-360° hue)
- **Cool colors**: Blues, greens, purples (120-300° hue)
- **Neutral colors**: Low saturation colors (grays, beiges, etc.)

### Style-Based Suggestions
- **Professional**: Navy, black, white, gray
- **Casual**: Blue, green, brown, beige
- **Elegant**: Black, white, navy, burgundy
- **Playful**: Yellow, orange, pink, sky blue

## 🏗️ Architecture

```
cache-service/
├── app.py                 # Flask web application
├── fastapi_app.py         # FastAPI alternative
├── color_utils.py         # Color processing utilities
├── test_app.py           # Comprehensive test suite
├── requirements.txt       # Python dependencies
├── Dockerfile            # Flask deployment
├── Dockerfile.fastapi    # FastAPI deployment
├── static/               # Static files and uploads
└── README.md            # This file
```

### Key Components

- **Image Processing**: PIL + scikit-learn for color extraction
- **Web Framework**: Flask or FastAPI for HTTP handling
- **Color Analysis**: K-means clustering for dominant color detection
- **Data Storage**: In-memory hashmaps (easily extensible to databases)
- **Frontend**: Simple HTML with JavaScript for file uploads

## 🐳 Deployment

### Docker Deployment

**Flask version**:
```bash
docker build -t outfit-matcher .
docker run -p 5000:5000 outfit-matcher
```

**FastAPI version**:
```bash
docker build -f Dockerfile.fastapi -t outfit-matcher-api .
docker run -p 8000:8000 outfit-matcher-api
```

### Cloud Platforms

#### Fly.io
```bash
flyctl launch
flyctl deploy
```

#### Render
1. Connect your GitHub repository
2. Select "Web Service"
3. Use build command: `pip install -r requirements.txt`
4. Use start command: `gunicorn app:app`

#### Vercel (FastAPI)
```bash
vercel --prod
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
python test_app.py
```

Tests include:
- Hashmap structure validation
- Color mapping accuracy
- Color harmony suggestions
- Performance benchmarks
- Image processing functionality
- Wardrobe simulation

## 🔧 Configuration

### Environment Variables

- `FLASK_ENV`: Set to `production` for deployment
- `PORT`: Server port (default: 5000 for Flask, 8000 for FastAPI)
- `MAX_CONTENT_LENGTH`: Maximum file upload size (default: 16MB)

### Customization

- **Add new colors**: Extend `basic_colors_hashmap` in `color_utils.py`
- **Modify compatibility rules**: Update `compatible_colors_hashmap` in main app files
- **Add new categories**: Extend `category_combinations_hashmap`
- **Custom styles**: Add to `COLOR_EMOTION_HASHMAP` in `color_utils.py`

## 📊 Performance

The hashmap-based approach provides:
- **O(1) average lookup time** for color compatibility
- **Sub-millisecond response times** for most operations
- **Efficient memory usage** with in-memory data structures
- **Scalable architecture** ready for database integration

Benchmark results (from test suite):
- 10,000 color lookups: ~0.1-0.3 seconds
- 1,000 harmony suggestions: ~0.01-0.05 seconds

## 🛠️ Development

### Adding New Features

1. **New color harmony types**: Add to `COLOR_HARMONY_HASHMAP`
2. **Additional image processing**: Extend functions in `color_utils.py`
3. **Database integration**: Replace in-memory hashmaps with database queries
4. **Machine learning**: Add ML models for automatic categorization
5. **User authentication**: Implement user sessions and persistent storage

### Code Structure

- **Separation of concerns**: Color logic in `color_utils.py`, web logic in app files
- **Type hints**: FastAPI version includes comprehensive type annotations
- **Error handling**: Graceful fallbacks for image processing errors
- **Modular design**: Easy to swap components or add new features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🎯 Future Enhancements

- [ ] Machine learning for automatic clothing categorization
- [ ] Advanced pattern recognition (stripes, polka dots, etc.)
- [ ] Seasonal outfit suggestions
- [ ] Social features (sharing outfits, ratings)
- [ ] Mobile app development
- [ ] Integration with fashion APIs
- [ ] Virtual try-on features
- [ ] Outfit history and analytics

## 📞 Support

For questions, issues, or contributions, please open an issue on GitHub or contact the development team.

---

**Built with ❤️ using Python, hashmaps, and color theory**
>>>>>>> 556431f (Initial commit after reset)
